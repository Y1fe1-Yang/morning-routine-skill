#!/usr/bin/env python3
"""
Optimized Email Fetcher for Large Inboxes
Avoids slow date-based searches, directly fetches most recent emails
"""

import os
import sys
import imaplib
import email
from email.header import decode_header
import json
import re


def decode_mime(s):
    """Decode MIME encoded-words in string."""
    if not s:
        return ""
    try:
        decoded = decode_header(s)
        return ''.join([
            frag.decode(enc or 'utf-8', errors='ignore') if isinstance(frag, bytes) else str(frag)
            for frag, enc in decoded
        ])
    except:
        return str(s)


def is_automated_notification(subject, from_addr, body):
    """Check if email is an automated notification that should be filtered."""
    automated_patterns = [
        'no-reply@',
        'noreply@',
        'do-not-reply@',
        'donotreply@',
        'notifications@',
        'alert@',
        'security@accounts',
    ]

    # Check sender
    for pattern in automated_patterns:
        if pattern in from_addr.lower():
            return True

    # Check if it's a security alert with no actionable content
    security_keywords = ['安全提醒', 'security alert', 'security notification', '登录活动']
    if any(kw in subject for kw in security_keywords):
        # Security alerts are usually informational only
        return True

    return False


def extract_actionable_content(subject, body):
    """Extract potentially actionable content from email body."""
    # Remove HTML tags
    body_text = re.sub(r'<[^>]+>', '', body)

    # Look for action keywords
    action_keywords = [
        'please', 'review', 'respond', 'complete', 'approve', 'confirm',
        'action required', 'deadline', 'due', 'meeting', 'schedule',
        '请', '需要', '完成', '审批', '确认', '会议', '截止'
    ]

    # Extract sentences with action keywords
    sentences = re.split(r'[.!?\n]+', body_text)
    actionable_sentences = []

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in action_keywords):
            clean_sentence = sentence.strip()
            if len(clean_sentence) > 20 and len(clean_sentence) < 200:
                actionable_sentences.append(clean_sentence)

    return actionable_sentences[:3]  # Return top 3


def connect_and_fetch(email_addr, password, max_emails=10):
    """Connect to Gmail and fetch most recent emails efficiently."""
    print(f"Connecting to Gmail IMAP for {email_addr}...", flush=True)

    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993, timeout=10)
        mail.login(email_addr, password)
        mail.select('INBOX')

        print("Connected! Fetching email metadata...", flush=True)

        # Get total count and unread count efficiently
        status, unread_msgs = mail.search(None, 'UNSEEN')
        unread_ids = unread_msgs[0].split() if unread_msgs[0] else []
        unread_count = len(unread_ids)

        # Get all message IDs (just the count, fast operation)
        status, all_msgs = mail.search(None, 'ALL')
        all_ids = all_msgs[0].split() if all_msgs[0] else []
        total_count = len(all_ids)

        print(f"Found {total_count} total emails, {unread_count} unread", flush=True)

        # Get the most recent N emails directly (no date filtering)
        recent_ids = all_ids[-max_emails:] if len(all_ids) > max_emails else all_ids

        print(f"Fetching {len(recent_ids)} most recent emails...", flush=True)

        emails = []
        for i, eid in enumerate(reversed(recent_ids)):
            try:
                # Fetch email with timeout protection
                status, data = mail.fetch(eid, '(RFC822)')

                if status != 'OK':
                    continue

                for part in data:
                    if isinstance(part, tuple):
                        msg = email.message_from_bytes(part[1])

                        subject = decode_mime(msg.get('Subject', ''))
                        from_addr = decode_mime(msg.get('From', ''))
                        date_str = msg.get('Date', '')

                        # Get plain text body
                        body = ""
                        if msg.is_multipart():
                            for p in msg.walk():
                                if p.get_content_type() == "text/plain":
                                    try:
                                        payload = p.get_payload(decode=True)
                                        if payload:
                                            body = payload.decode('utf-8', errors='ignore')[:1000]
                                            break
                                    except:
                                        pass
                        else:
                            try:
                                payload = msg.get_payload(decode=True)
                                if payload:
                                    body = payload.decode('utf-8', errors='ignore')[:1000]
                            except:
                                pass

                        # Check if unread
                        is_unread = eid in unread_ids

                        # Filter automated notifications
                        is_automated = is_automated_notification(subject, from_addr, body)

                        # Extract actionable content
                        actionable = extract_actionable_content(subject, body) if not is_automated else []

                        emails.append({
                            'subject': subject or '(No subject)',
                            'from': from_addr,
                            'body': body.strip()[:500] if body else '(No text content)',
                            'date': date_str,
                            'unread': is_unread,
                            'automated': is_automated,
                            'actionable_content': actionable
                        })

                        print(f"  [{i+1}/{len(recent_ids)}] {subject[:50]}...", flush=True)

            except Exception as e:
                print(f"  Error fetching email: {e}", flush=True)
                continue

        mail.close()
        mail.logout()

        return {
            'unread_count': unread_count,
            'total_count': total_count,
            'emails': emails,
            'actionable_emails': [e for e in emails if not e['automated'] and e['actionable_content']]
        }

    except Exception as e:
        print(f"Error: {e}", flush=True)
        return None


def main():
    """Main function."""
    email_addr = os.getenv('CAPY_USER_EMAIL', 'yyf2464212962@gmail.com')
    password = os.getenv('EMAIL_PASSWORD')

    if not password:
        print("No EMAIL_PASSWORD set. Please set it first.")
        sys.exit(1)

    result = connect_and_fetch(email_addr, password, max_emails=10)

    if result:
        print("\n" + "="*60)
        print("EMAIL FETCH SUMMARY")
        print("="*60)
        print(f"Total emails: {result['total_count']}")
        print(f"Unread: {result['unread_count']}")
        print(f"Fetched: {len(result['emails'])}")
        print(f"Actionable: {len(result['actionable_emails'])}")
        print("="*60)

        # Output JSON
        print("\nJSON OUTPUT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Failed to fetch emails")
        sys.exit(1)


if __name__ == "__main__":
    main()
