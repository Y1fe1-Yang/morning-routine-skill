#!/usr/bin/env python3
"""
Automatic Email Fetcher - Uses System-Provided OAuth Tokens
Works with ZERO user input when environment variables are configured.
"""

import os
import sys
import json
from datetime import datetime, timedelta

def check_environment():
    """Check if Gmail OAuth tokens are provided via environment."""
    required_vars = [
        'CAPY_GMAIL_ACCESS_TOKEN',
        'CAPY_GMAIL_REFRESH_TOKEN',
        'CAPY_GMAIL_CLIENT_ID',
        'CAPY_GMAIL_CLIENT_SECRET'
    ]

    available = all(os.getenv(var) for var in required_vars)
    return available

def fetch_with_gmail_api():
    """Fetch emails using Gmail API with system-provided tokens."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        print("✗ Gmail API libraries not installed")
        print("  Install with: pip install --break-system-packages google-auth google-auth-oauthlib google-api-python-client")
        return None

    # Use system-provided OAuth tokens (zero user input!)
    creds = Credentials(
        token=os.getenv('CAPY_GMAIL_ACCESS_TOKEN'),
        refresh_token=os.getenv('CAPY_GMAIL_REFRESH_TOKEN'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.getenv('CAPY_GMAIL_CLIENT_ID'),
        client_secret=os.getenv('CAPY_GMAIL_CLIENT_SECRET')
    )

    # Auto-refresh if needed
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # Build Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # Fetch recent emails (last 24 hours)
    yesterday = datetime.now() - timedelta(days=1)
    query = f'after:{int(yesterday.timestamp())}'

    results = service.users().messages().list(
        userId='me',
        maxResults=10,
        q=query
    ).execute()

    messages = results.get('messages', [])

    # Get profile for email address
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
        'source': 'gmail_api_auto'
    }

def fetch_with_worker_api():
    """Fetch emails via Worker API (alternative pattern)."""
    try:
        import requests
    except ImportError:
        return None

    base_url = os.getenv('AGENT_WORKER_BASE_URL')
    secret = os.getenv('AGENT_WORKER_SECRET')
    sandbox_id = os.getenv('FLY_APP_NAME')
    user_email = os.getenv('CAPY_USER_EMAIL')

    if not all([base_url, secret, sandbox_id]):
        return None

    response = requests.post(
        f"{base_url}/api/email/read",
        headers={
            'Authorization': f"Bearer {secret}",
            'X-Sandbox-Id': sandbox_id,
            'Content-Type': 'application/json'
        },
        json={
            'user_email': user_email,
            'max_results': 10,
            'time_range': '24h'
        },
        timeout=10
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    """Main function - tries automatic methods, falls back to manual."""
    print("=" * 60)
    print("🔍 Automatic Email Fetcher")
    print("=" * 60)

    # Method 1: System-provided Gmail OAuth tokens (BEST)
    if check_environment():
        print("\n✓ Gmail OAuth tokens found in environment")
        print("  Fetching emails automatically...")

        result = fetch_with_gmail_api()
        if result:
            print(f"✓ Fetched {result['total_fetched']} emails from {result['email_address']}")
            print(f"  Unread count: {result['unread_count']}")
            print(json.dumps(result, indent=2))
            return 0
        else:
            print("✗ Gmail API fetch failed")
    else:
        print("\n⚠️  Gmail OAuth tokens not found in environment")
        print("   Missing: CAPY_GMAIL_ACCESS_TOKEN, CAPY_GMAIL_REFRESH_TOKEN")

    # Method 2: Worker API (ALTERNATIVE)
    print("\n🔍 Trying Worker API...")
    result = fetch_with_worker_api()
    if result:
        print("✓ Fetched emails via Worker API")
        print(json.dumps(result, indent=2))
        return 0
    else:
        print("✗ Worker API not available")

    # Method 3: Fallback to manual input
    print("\n" + "=" * 60)
    print("📝 Automatic email fetching not configured")
    print("=" * 60)
    print("\nPlease use one of these methods:")
    print("\n1. Manual Input (CURRENT FALLBACK):")
    print("   python3 scripts/generate_morning_briefing.py")
    print("\n2. System Configuration (RECOMMENDED):")
    print("   Ask system admin to configure CAPY_GMAIL_ACCESS_TOKEN")
    print("\n3. Worker API (ALTERNATIVE):")
    print("   Ask system admin to enable /api/email/read endpoint")

    return 1

if __name__ == "__main__":
    sys.exit(main())
