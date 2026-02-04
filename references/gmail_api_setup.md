# Gmail API Setup Guide

## Why Gmail API vs IMAP?

**Gmail API advantages:**
- ✅ **Much faster** for large inboxes (1000+ emails)
- ✅ **No timeouts** - Efficient pagination
- ✅ **Better queries** - Search by label, date, sender easily
- ✅ **Official Google API** - Better support and reliability
- ✅ **Structured data** - Clean JSON responses

**IMAP disadvantages:**
- ❌ Slow for large inboxes
- ❌ Timeouts on date searches
- ❌ Less efficient queries
- ❌ Text parsing required

## Setup Steps (One-time, ~5 minutes)

### Step 1: Enable Gmail API in Google Cloud Console

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Create a New Project** (or select existing):
   - Click "Select a project" → "New Project"
   - Project name: "Morning Routine Skill"
   - Click "Create"

3. **Enable Gmail API:**
   - In the search bar, type "Gmail API"
   - Click "Gmail API"
   - Click "Enable"

### Step 2: Create OAuth 2.0 Credentials

1. **Go to Credentials page:**
   - Left sidebar → "APIs & Services" → "Credentials"
   - Or visit: https://console.cloud.google.com/apis/credentials

2. **Configure OAuth Consent Screen** (if first time):
   - Click "Configure Consent Screen"
   - Select "External" (unless you have Google Workspace)
   - Fill in:
     - App name: "Morning Routine Skill"
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - Skip "Scopes" (click "Save and Continue")
   - Add your email as a test user
   - Click "Save and Continue" → "Back to Dashboard"

3. **Create OAuth Client ID:**
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: **"Desktop app"**
   - Name: "Morning Routine Desktop Client"
   - Click "Create"

4. **Download credentials.json:**
   - Click "Download JSON" button
   - Save the file

### Step 3: Install credentials.json

Move the downloaded file to the skill directory:

```bash
# Move credentials.json to skill directory
mv ~/Downloads/client_secret_*.json ~/.claude/skills/morning-routine/credentials.json

# Or manually copy it:
cp /path/to/downloaded/credentials.json ~/.claude/skills/morning-routine/credentials.json
```

Verify the file exists:
```bash
ls -la ~/.claude/skills/morning-routine/credentials.json
```

### Step 4: Install Python Dependencies

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 5: First-Time Authorization

Run the Gmail API fetcher:

```bash
cd /home/node/.claude/skills/morning-routine
python3 scripts/fetch_emails_gmail_api.py
```

**What happens:**
1. Script will open a browser window
2. Google will ask you to sign in
3. Review permissions (read-only access to Gmail)
4. Click "Allow"
5. Browser shows "The authentication flow has completed"
6. Script continues and fetches your emails

**Token saved:**
After authorization, a `token.json` file is created at:
```
~/.claude/skills/morning-routine/token.json
```

This token is reused for future runs (no browser popup needed).

## Usage

Once set up, just run:

```bash
python3 scripts/fetch_emails_gmail_api.py
```

**Output:**
```json
{
  "email_address": "yyf2464212962@gmail.com",
  "total_count": 1857,
  "unread_count": 1606,
  "emails": [
    {
      "id": "abc123...",
      "subject": "Email Subject",
      "from": "sender@example.com",
      "body": "Email content...",
      "date": "Tue, 3 Feb 2026...",
      "unread": true,
      "automated": false
    }
  ]
}
```

## Integration with Morning Routine

The skill will automatically use Gmail API if:
1. `credentials.json` exists
2. `token.json` exists (after first auth)
3. Gmail API packages are installed

Otherwise, it falls back to IMAP (if EMAIL_PASSWORD is set).

## Security Notes

**credentials.json:**
- Contains your OAuth client ID and secret
- Not as sensitive as passwords (requires user authorization)
- Should still be kept private (don't commit to git)

**token.json:**
- Contains your authorized access token
- **More sensitive** - grants access to your Gmail
- Already in .gitignore
- Can be revoked at: https://myaccount.google.com/permissions

**Permissions:**
- Read-only access to Gmail
- Cannot send, delete, or modify emails
- Can be revoked anytime without affecting your account

## Troubleshooting

### "credentials.json not found"

**Solution:**
1. Download credentials from Google Cloud Console (Step 2 above)
2. Move to: `~/.claude/skills/morning-routine/credentials.json`

### "Access blocked: This app's request is invalid"

**Solution:**
1. Make sure OAuth Consent Screen is configured (Step 2.2 above)
2. Add your email as a test user
3. Make sure you selected "Desktop app" not "Web application"

### "The authentication flow has completed" but script fails

**Solution:**
1. Check that `token.json` was created
2. Try running the script again (should work without browser)
3. If still fails, delete `token.json` and re-authorize

### "ModuleNotFoundError: No module named 'google'"

**Solution:**
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Revoking Access

If you want to revoke the skill's access:
1. Visit: https://myaccount.google.com/permissions
2. Find "Morning Routine Skill"
3. Click "Remove Access"
4. Delete `token.json` from skill directory

## Advantages Over IMAP

**For your inbox (1857 emails, 1606 unread):**

| Feature | IMAP | Gmail API |
|---------|------|-----------|
| Fetch 10 emails | 30-60s (timeout) | 2-3s ✓ |
| Search by date | Timeout | Instant ✓ |
| Count unread | Slow | Instant ✓ |
| Connection | Can timeout | Reliable ✓ |
| Setup complexity | Easy (just password) | Medium (OAuth once) |

**Conclusion:** Gmail API is **much better** for large inboxes like yours!

## Quick Reference

**Files:**
- `~/.claude/skills/morning-routine/credentials.json` - OAuth client credentials (download once)
- `~/.claude/skills/morning-routine/token.json` - Access token (auto-generated after first auth)
- `scripts/fetch_emails_gmail_api.py` - Gmail API fetcher script

**Commands:**
```bash
# First time setup (opens browser for authorization)
python3 scripts/fetch_emails_gmail_api.py

# Subsequent runs (no browser needed)
python3 scripts/fetch_emails_gmail_api.py

# Reset authorization (delete token and re-authorize)
rm ~/.claude/skills/morning-routine/token.json
python3 scripts/fetch_emails_gmail_api.py
```

## Next Steps

After setting up Gmail API:
1. Run `fetch_emails_gmail_api.py` to test
2. The morning routine skill will automatically use it
3. Enjoy much faster email fetching!
