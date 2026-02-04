#!/bin/bash
# Gmail API Setup Helper Script

echo "=========================================="
echo "Gmail API Setup for Morning Routine Skill"
echo "=========================================="
echo

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip not found"
    echo "Please install pip first"
    exit 1
fi

# Use pip3 if available, otherwise pip
PIP_CMD=$(command -v pip3 || command -v pip)

echo "Step 1: Installing Python dependencies..."
echo "Running: $PIP_CMD install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"
echo

$PIP_CMD install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo
echo "Step 2: Check for credentials.json..."
SKILL_DIR="$HOME/.claude/skills/morning-routine"
CREDS_FILE="$SKILL_DIR/credentials.json"

if [ -f "$CREDS_FILE" ]; then
    echo "✓ credentials.json found at: $CREDS_FILE"
else
    echo "⚠️  credentials.json NOT found"
    echo
    echo "You need to:"
    echo "1. Go to: https://console.cloud.google.com/apis/credentials"
    echo "2. Create OAuth 2.0 Client ID (Desktop app)"
    echo "3. Download the credentials JSON file"
    echo "4. Save it to: $CREDS_FILE"
    echo
    echo "See detailed guide: references/gmail_api_setup.md"
    exit 1
fi

echo
echo "Step 3: Testing Gmail API connection..."
echo

cd "$SKILL_DIR"
python3 scripts/fetch_emails_gmail_api.py

if [ $? -eq 0 ]; then
    echo
    echo "=========================================="
    echo "✓ Gmail API setup complete!"
    echo "=========================================="
    echo
    echo "You can now use the morning routine skill with Gmail API"
    echo "Run: python3 scripts/fetch_emails_gmail_api.py"
else
    echo
    echo "⚠️  Setup incomplete or test failed"
    echo "Check the error messages above"
    echo "See: references/gmail_api_setup.md for troubleshooting"
fi
