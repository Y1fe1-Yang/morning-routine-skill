#!/usr/bin/env python3
"""
Email Fetcher for Morning Routine
Fetches emails from Gmail/Capymail using IMAP
"""

import os
import sys
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import json

def get_email_credentials():
    """Get email credentials from environment variables."""
    email_address = os.getenv('CAPY_USER_EMAIL') or os.getenv('USER_EMAIL')
    email_password = os.getenv('EMAIL_PASSWORD') or os.getenv('GMAIL_APP_PASSWORD')

    if not email_address:
        print("Error: No email address found in environment variables")
        print("Please set CAPY_USER_EMAIL or USER_EMAIL")
        return None, None

    if not email_password:
        print("Warning: No email password found")
        print("Please set EMAIL_PASSWORD or GMAIL_APP_PASSWORD")
        print("For Gmail, use an App Password: https://myaccount.google.com/apppasswords")
        return email_address, None

    return email_address, email_password


def connect_to_imap(email_address, password, imap_server=None):
    """Connect to IMAP server."""
    if not imap_server:
        # Determine IMAP server from email domain
        domain = email_address.split('@')[1]
        if 'gmail' in domain:
            imap_server = 'imap.gmail.com'
        elif 'outlook' in domain or 'hotmail' in domain:
            imap_server = 'outlook.office365.com'
        else:
            imap_server = f'imap.{domain}'

    print(f"Connecting to {imap_server}...")

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        return mail
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None


def decode_mime_words(s):
    """Decode MIME encoded-words in string."""
    if not s:
        return ""
    decoded_fragments = decode_header(s)
    return ''.join([
        fragment.decode(encoding or 'utf-8') if isinstance(fragment, bytes) else fragment
        for fragment, encoding in decoded_fragments
    ])


def fetch_recent_emails(mail, hours=24, max_emails=20):
    """Fetch recent emails from inbox."""
    mail.select('INBOX')

    # Search for emails from the last N hours
    date_since = (datetime.now() - timedelta(hours=hours)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'(SINCE {date_since})')

    if status != 'OK':
        print("Failed to search emails")
        return []

    email_ids = messages[0].split()
    email_ids = email_ids[-max_emails:]  # Get last N emails

    emails = []
    for email_id in reversed(email_ids):  # Newest first
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        if status != 'OK':
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Extract email details
                subject = decode_mime_words(msg['Subject'])
                from_addr = decode_mime_words(msg['From'])
                date = msg['Date']

                # Get email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            try:
                                body = part.get_payload(decode=True).decode()
                                break
                            except:
                                pass
                else:
                    try:
                        body = msg.get_payload(decode=True).decode()
                    except:
                        body = str(msg.get_payload())

                # Check if email is unread
                status, flags = mail.fetch(email_id, '(FLAGS)')
                is_unread = b'\\Seen' not in flags[0]

                emails.append({
                    'subject': subject,
                    'from': from_addr,
                    'date': date,
                    'body': body[:500],  # First 500 chars
                    'unread': is_unread
                })

    return emails


def main():
    """Main function to fetch and display emails."""
    email_address, password = get_email_credentials()

    if not email_address:
        sys.exit(1)

    if not password:
        print("\n--- DEMO MODE ---")
        print("No password provided. Returning mock email data for demonstration.")
        print("\nTo connect to real email:")
        print("1. For Gmail: Create an App Password at https://myaccount.google.com/apppasswords")
        print("2. Set environment variable: export EMAIL_PASSWORD='your-app-password'")
        print("3. Run this script again")

        # Return mock data
        mock_emails = [
            {
                'subject': 'Morning Routine Skill - Testing Request',
                'from': 'user@example.com',
                'date': datetime.now().strftime("%a, %d %b %Y %H:%M:%S"),
                'body': 'Please test the morning routine skill with real email data and provide feedback on the workflow.',
                'unread': True
            },
            {
                'subject': 'Feature Request: Calendar Integration',
                'from': 'product@example.com',
                'date': (datetime.now() - timedelta(hours=2)).strftime("%a, %d %b %Y %H:%M:%S"),
                'body': 'It would be great to integrate calendar events into the morning routine to show upcoming meetings.',
                'unread': True
            },
            {
                'subject': 'System Update: Deployment Completed',
                'from': 'noreply@system.com',
                'date': (datetime.now() - timedelta(hours=5)).strftime("%a, %d %b %Y %H:%M:%S"),
                'body': 'The morning-routine skill has been successfully deployed to production environment.',
                'unread': False
            }
        ]

        print(json.dumps(mock_emails, indent=2))
        return

    # Connect to real email
    mail = connect_to_imap(email_address, password)
    if not mail:
        sys.exit(1)

    print("Fetching recent emails...")
    emails = fetch_recent_emails(mail, hours=24, max_emails=20)

    print(f"\nFound {len(emails)} emails")
    print(f"Unread: {sum(1 for e in emails if e['unread'])}")

    # Output as JSON
    print(json.dumps(emails, indent=2))

    mail.close()
    mail.logout()


if __name__ == "__main__":
    main()
