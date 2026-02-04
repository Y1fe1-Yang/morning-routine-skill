# Email Setup Guide

## Connecting to Your Email

The morning routine skill can connect to your real email inbox via IMAP. Here's how to set it up:

### For Gmail (yyf2464212962@gmail.com)

1. **Create an App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Sign in with your Google account
   - Select "Mail" and "Other (Custom name)"
   - Name it "Morning Routine Skill"
   - Click "Generate"
   - Copy the 16-character password

2. **Set Environment Variable:**
   ```bash
   export EMAIL_PASSWORD='your-16-char-app-password'
   ```

3. **Test Connection:**
   ```bash
   python3 /home/node/.claude/skills/morning-routine/scripts/fetch_emails.py
   ```

### For Capymail.ai (yves_yang@capymail.ai)

Capymail.ai might have different authentication. Options:

1. **IMAP Access** (if supported):
   - Find IMAP settings in capymail.ai documentation
   - Set credentials as above

2. **API Access** (if available):
   - Check if capymail.ai provides an API
   - Use API key instead of IMAP

3. **Email Forwarding**:
   - Forward capymail.ai emails to your Gmail
   - Use Gmail's IMAP connection

### For Other Email Providers

**Outlook/Hotmail:**
- IMAP Server: `outlook.office365.com`
- Port: 993
- Create App Password in Microsoft Account settings

**Yahoo:**
- IMAP Server: `imap.mail.yahoo.com`
- Port: 993
- Generate App Password in Account Security settings

**Custom Domain:**
- Check your email provider's IMAP settings
- Usually: `imap.yourdomain.com`

## Environment Variables

The skill uses these environment variables:

```bash
# Required for email fetching
export EMAIL_PASSWORD='your-app-password-here'

# Already set in your environment
export CAPY_USER_EMAIL='yyf2464212962@gmail.com'
export CAPY_USER_EMAIL_ALIAS='yves_yang@capymail.ai'
```

## Testing Without Email

If you don't want to connect real email, the skill works in **demo mode** with mock data. Just run without setting `EMAIL_PASSWORD`.

## Security Notes

- **Never commit passwords** to git repositories
- App Passwords are safer than your main password
- App Passwords can be revoked anytime without changing your main password
- The skill only reads emails, never modifies or deletes them

## Troubleshooting

**"Authentication failed"**
- Double-check the app password (no spaces)
- Verify IMAP is enabled in your email settings
- For Gmail: Ensure "Less secure app access" is NOT needed (app passwords work without it)

**"Connection timeout"**
- Check your internet connection
- Verify firewall isn't blocking port 993
- Try a different IMAP server if using custom domain

**"No emails found"**
- Check the time range (default: last 24 hours)
- Verify emails exist in your inbox
- Check that emails aren't all in folders/labels

## Email You Can Send for Testing

Send a test email to yourself (yves_yang@capymail.ai or yyf2464212962@gmail.com) with:

**Subject:** "Morning Routine Test - Action Items"

**Body:**
```
Hi Claude,

Please complete the following tasks today:

1. Review the morning routine skill documentation
2. Test the visual todo list image generation
3. Verify email fetching works with real IMAP connection

Let me know once these are done!

Attached: screenshot of the current implementation
```

This will give the skill real content to parse and extract tasks from.
