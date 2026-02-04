#!/usr/bin/env python3
"""
Simple Gmail Email Fetcher - Uses existing credentials
Works with the credentials.json you already have!
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

def fetch_with_gmail_api():
    """Fetch emails using Gmail API with existing credentials."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("✗ Gmail API libraries not installed")
        print("  Run: pip install --break-system-packages google-auth google-auth-oauthlib google-api-python-client")
        return None

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    creds = None
    skill_dir = Path('/home/node/.claude/skills/morning-routine')
    token_file = skill_dir / 'token.json'
    creds_file = skill_dir / 'credentials.json'

    # Check if credentials.json exists
    if not creds_file.exists():
        print(f"✗ credentials.json not found at {creds_file}")
        return None

    # Load token if it exists
    if token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
        except Exception as e:
            print(f"⚠️  Could not load token: {e}")
            creds = None

    # Refresh or get new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            try:
                creds.refresh(Request())
                print("✓ Token refreshed successfully")
            except Exception as e:
                print(f"✗ Token refresh failed: {e}")
                creds = None

        if not creds:
            print("\n" + "="*60)
            print("🔐 Gmail Authorization Required (One Time Only)")
            print("="*60)
            print("\nAttempting to authorize Gmail...")
            print("If a browser doesn't open, you'll see a URL to visit.")

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(creds_file), SCOPES)

                # Try to run local server for OAuth
                # This will open browser or print URL
                creds = flow.run_local_server(port=0, open_browser=True)

                # Save token
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
                print(f"\n✓ Authorization saved to: {token_file}")
                print("✓ You won't need to authorize again!")

            except Exception as e:
                print(f"\n✗ Authorization failed: {e}")
                print("\nTo authorize manually:")
                print("1. Run this script in an environment with browser access")
                print("2. Or use manual mode: create morning_email_input.json")
                return None

    # Build Gmail service
    try:
        service = build('gmail', 'v1', credentials=creds)
    except Exception as e:
        print(f"✗ Could not build Gmail service: {e}")
        return None

    # Fetch recent emails (last 24 hours)
    try:
        yesterday = datetime.now() - timedelta(days=1)
        query = f'after:{int(yesterday.timestamp())}'

        print("📧 Fetching recent emails...")
        results = service.users().messages().list(
            userId='me',
            maxResults=10,
            q=query
        ).execute()

        messages = results.get('messages', [])

        # Get profile
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile.get('emailAddress', 'Unknown')

        # Fetch message details
        emails = []
        for msg in messages[:10]:
            msg_detail = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()

            headers = {h['name']: h['value'] for h in msg_detail.get('payload', {}).get('headers', [])}

            emails.append({
                'id': msg['id'],
                'from': headers.get('From', 'Unknown'),
                'subject': headers.get('Subject', '(No Subject)'),
                'date': headers.get('Date', ''),
                'snippet': msg_detail.get('snippet', '')
            })

        # Get unread count
        unread_results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=1
        ).execute()

        unread_count = unread_results.get('resultSizeEstimate', 0)

        return {
            'email_address': email_address,
            'unread_count': unread_count,
            'total_fetched': len(emails),
            'emails': emails,
            'source': 'gmail_api'
        }

    except Exception as e:
        print(f"✗ Error fetching emails: {e}")
        return None

def main():
    """Main function."""
    print("=" * 60)
    print("📧 Simple Gmail Fetcher")
    print("=" * 60)

    result = fetch_with_gmail_api()

    if result:
        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print("=" * 60)
        print(f"📧 Email: {result['email_address']}")
        print(f"📊 Unread: {result['unread_count']}")
        print(f"📥 Fetched: {result['total_fetched']} recent emails")
        print("=" * 60)

        # Print emails
        print("\nRecent Emails:")
        for i, email in enumerate(result['emails'], 1):
            print(f"\n{i}. From: {email['from']}")
            print(f"   Subject: {email['subject']}")
            print(f"   Snippet: {email['snippet'][:80]}...")

        # Output JSON for other scripts to use
        print("\n" + "=" * 60)
        print("JSON Output:")
        print("=" * 60)
        print(json.dumps(result, indent=2))

        return 0
    else:
        print("\n✗ Failed to fetch emails")
        print("\nTroubleshooting:")
        print("1. Make sure credentials.json exists")
        print("2. Run authorization when prompted")
        print("3. Check your internet connection")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
