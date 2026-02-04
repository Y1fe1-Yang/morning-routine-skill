#!/usr/bin/env python3
"""
Gmail API Email Fetcher - Manual Authorization Mode
For environments without browser access (like sandboxes)
"""

import os
import sys
import json
import base64
from datetime import datetime, timedelta
from pathlib import Path

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Required packages not installed")
    print("\nPlease install Gmail API dependencies:")
    print("  pip install --break-system-packages --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_credentials():
    """Get or refresh Gmail API credentials with manual auth flow."""
    creds = None
    token_path = Path.home() / '.claude' / 'skills' / 'morning-routine' / 'token.json'
    credentials_path = Path.home() / '.claude' / 'skills' / 'morning-routine' / 'credentials.json'

    # Load existing token
    if token_path.exists():
        print("Loading existing token...")
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
            print("✓ Token refreshed successfully!")
        else:
            if not credentials_path.exists():
                print("\nError: credentials.json not found!")
                print(f"Expected location: {credentials_path}")
                print("\nPlease ensure credentials.json is in the correct location")
                sys.exit(1)

            print("\n" + "="*60)
            print("MANUAL AUTHORIZATION REQUIRED")
            print("="*60)
            print("\nStarting OAuth authorization flow...")
            print("Since we're in a sandbox, you'll need to manually authorize.\n")

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)

            # Use console-based auth flow instead of local server
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

            auth_url, _ = flow.authorization_url(prompt='consent')

            print("STEP 1: Open this URL in your browser:")
            print("-" * 60)
            print(auth_url)
            print("-" * 60)
            print("\nSTEP 2: After authorizing, you'll see an authorization code.")
            print("STEP 3: Copy the code and paste it here.\n")

            code = input("Enter the authorization code: ").strip()

            print("\nFetching token...")
            flow.fetch_token(code=code)
            creds = flow.credentials

        # Save the credentials for next run
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print(f"✓ Token saved to: {token_path}")

    return creds


def decode_message_part(part):
    """Decode email message part."""
    if 'data' in part['body']:
        data = part['body']['data']
    elif 'attachmentId' in part['body']:
        return None
    else:
        return None

    data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return data


def get_message_body(payload):
    """Extract plain text body from message payload."""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return decode_message_part(part)
            elif part['mimeType'] == 'multipart/alternative':
                for subpart in part.get('parts', []):
                    if subpart['mimeType'] == 'text/plain':
                        return decode_message_part(subpart)
    elif payload['mimeType'] == 'text/plain':
        return decode_message_part(payload)

    return None


def get_header_value(headers, name):
    """Get header value by name."""
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return None


def fetch_recent_emails(max_results=10):
    """Fetch recent emails using Gmail API."""
    print("\n" + "="*60)
    print("FETCHING EMAILS FROM GMAIL")
    print("="*60)

    creds = get_credentials()

    try:
        service = build('gmail', 'v1', credentials=creds)

        # Get user profile
        print("\nConnecting to Gmail...")
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile['emailAddress']
        total_messages = profile['messagesTotal']

        print(f"✓ Connected to: {email_address}")
        print(f"✓ Total messages: {total_messages}")

        # Query for recent messages
        print(f"\nFetching {max_results} most recent emails...")

        results = service.users().messages().list(
            userId='me',
            maxResults=max_results,
            labelIds=['INBOX']
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
            return {
                'email_address': email_address,
                'total_count': total_messages,
                'unread_count': 0,
                'emails': []
            }

        print(f"Found {len(messages)} messages. Fetching details...")

        # Count unread messages
        unread_results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=1
        ).execute()
        unread_count = unread_results.get('resultSizeEstimate', 0)

        # Fetch full message details
        emails = []
        for i, message in enumerate(messages, 1):
            try:
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()

                payload = msg['payload']
                headers = payload['headers']

                subject = get_header_value(headers, 'Subject') or '(No subject)'
                from_addr = get_header_value(headers, 'From') or '(Unknown sender)'
                date_str = get_header_value(headers, 'Date') or ''

                # Get message body
                body = get_message_body(payload)
                if body:
                    body = body[:800]
                else:
                    body = '(No plain text content)'

                # Check if unread
                labels = msg.get('labelIds', [])
                is_unread = 'UNREAD' in labels

                # Check if automated
                is_automated = any(pattern in from_addr.lower() for pattern in [
                    'no-reply@', 'noreply@', 'do-not-reply@'
                ])

                emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'from': from_addr,
                    'body': body.strip(),
                    'date': date_str,
                    'unread': is_unread,
                    'automated': is_automated,
                    'labels': labels
                })

                print(f"  [{i}/{len(messages)}] {subject[:60]}...")

            except HttpError as error:
                print(f"  Error fetching message {message['id']}: {error}")
                continue

        return {
            'email_address': email_address,
            'total_count': total_messages,
            'unread_count': unread_count,
            'emails': emails,
            'actionable_emails': [e for e in emails if not e['automated'] and e['unread']]
        }

    except HttpError as error:
        print(f"Gmail API error: {error}")
        return None


def main():
    """Main function."""
    print("="*60)
    print("GMAIL API EMAIL FETCHER - MANUAL AUTH MODE")
    print("="*60)

    result = fetch_recent_emails(max_results=10)

    if result:
        print("\n" + "="*60)
        print("FETCH COMPLETE")
        print("="*60)
        print(f"Email: {result['email_address']}")
        print(f"Total messages: {result['total_count']}")
        print(f"Unread: {result['unread_count']}")
        print(f"Fetched: {len(result['emails'])}")
        print(f"Actionable: {len(result['actionable_emails'])}")
        print("="*60)

        # Output JSON
        print("\nJSON OUTPUT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        return 0
    else:
        print("\nFailed to fetch emails")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
