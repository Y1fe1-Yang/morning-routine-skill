# 🚀 Quick Start Guide: Morning Routine Skill

## 📦 Installation

```bash
git clone https://github.com/Y1fe1-Yang/morning-routine-skill.git
cd morning-routine-skill
```

## ⚡ Two Ways to Use This Skill

### 🔥 Method 1: Gmail API (Auto Fetch - Gmail Only)

**One-time setup (5 minutes), then fully automatic!**

**⚠️ Note**: This method only works with Gmail accounts. For other email providers (Outlook, QQ Mail, 163 Mail, etc.), use Method 2.

---

## 📚 详细设置指南

**🔗 完整图文教程：** [GMAIL_API_SETUP_DETAILED.md](GMAIL_API_SETUP_DETAILED.md)

详细指南包含：
- ✅ 每一步的详细说明
- ✅ 常见问题解答
- ✅ 安全说明
- ✅ 故障排除

---

## ⚡ 快速步骤（5分钟）

#### Step 1: Google Cloud Console 设置

**1. Go here:** https://console.cloud.google.com/

**2. Create project:**
- Click "Select a project" → "NEW PROJECT"
- Name: `Morning Routine Skill`
- Click CREATE

**3. Enable Gmail API:**
- Search for "Gmail API" at top
- Click "Gmail API"
- Click "ENABLE"

**4. Setup OAuth:**
- Left sidebar → "OAuth consent screen"
- Choose "External" → CREATE
- App name: `Morning Routine Skill`
- User support email: your email
- Developer contact: your email
- Click "SAVE AND CONTINUE" (4 times)
- ⚠️ **Important:** On "Test users" page, click "+ ADD USERS"
- Add your Gmail email (e.g., `your_email@gmail.com`)
- Click ADD → SAVE AND CONTINUE

**5. Create credentials:**
- Left sidebar → "Credentials"
- "+ CREATE CREDENTIALS" → "OAuth client ID"
- **Application type:** Desktop app ← IMPORTANT!
- Name: `Morning Routine Desktop`
- Click CREATE
- ⚠️ **Don't miss:** Click "DOWNLOAD JSON" button
- File downloads as `client_secret_XXXXX.json`

#### Step 2: Install Downloaded JSON File

⚠️ **Important:** The file you just downloaded needs to be placed in the skill directory!

**Move and rename the file:**

```bash
# Move the downloaded file to skill directory and rename it
mv ~/Downloads/client_secret_*.json ./credentials.json

# Verify it's there
ls -l credentials.json
```

**Or manually:**
1. Find `client_secret_XXXXX.json` in your Downloads folder
2. Copy or move it to the `morning-routine-skill` directory
3. Rename it to `credentials.json`

✅ You should now have `credentials.json` in your skill folder

#### Step 3: Install Python Dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### Step 4: First-Time Authorization

```bash
python scripts/fetch_emails_gmail_api.py
```

**What happens:**
1. Browser opens automatically
2. Google asks you to sign in
3. Click "Allow" to give read-only Gmail access
4. Browser shows "Authentication complete"
5. Script fetches your emails automatically!

**Token saved**: A `token.json` file is created. Future runs won't need browser authorization.

#### Step 5: Use with Morning Briefing

Now you can fetch emails automatically:

```bash
# Fetch latest emails from Gmail
python scripts/fetch_emails_gmail_api.py > morning_email_input.json

# Generate morning briefing
python scripts/generate_morning_briefing_final.py
```

**Benefits:**
- ✅ Fully automatic email fetching
- ✅ Fast (2-3 seconds even with 1000+ emails)
- ✅ No manual copying
- ✅ Always up-to-date

---

### 📝 Method 2: Manual JSON Entry (No Setup - All Email Providers)

**Quick and simple, works with ANY email provider**

**✅ Works with**: Gmail, Outlook, QQ Mail, 163 Mail, Foxmail, Yahoo, ProtonMail, iCloud Mail, and any other email service

#### Option A: Browser Console Script (Fastest)

1. **Open Gmail** in your browser and go to your inbox
2. **Open Developer Console**:
   - Windows/Linux: Press `F12` or `Ctrl+Shift+J`
   - Mac: Press `Cmd+Option+J`
3. **Click the "Console" tab**
4. **Copy and paste this entire script**, then press Enter:

```javascript
(function() {
  console.log('📧 Extracting Gmail data...');

  const emails = [];
  const threads = document.querySelectorAll('tr.zA');

  threads.forEach((thread, index) => {
    if (index < 5) { // Get top 5 emails
      const sender = thread.querySelector('.yW span[email]')?.getAttribute('email') ||
                     thread.querySelector('.yW span')?.textContent || 'Unknown';
      const subject = thread.querySelector('.y6 span')?.textContent || 'No subject';
      const snippet = thread.querySelector('.y2')?.textContent || '';

      emails.push({
        from: sender,
        subject: subject.trim(),
        snippet: snippet.trim().substring(0, 100)
      });
    }
  });

  const unreadCount = document.querySelector('.aio.UKr6le .J-Ke.n0')?.textContent || '0';

  const output = {
    email_summary: `${unreadCount} unread emails in inbox`,
    key_emails: emails,
    custom_tasks: []
  };

  console.log('✅ JSON generated:');
  console.log(JSON.stringify(output, null, 2));
  copy(JSON.stringify(output, null, 2));
  alert('✅ JSON copied to clipboard! Now paste it into morning_email_input.json');
})();
```

5. **You'll see an alert**: "JSON copied to clipboard!"
6. **Open `morning_email_input.json`** in your editor
7. **Paste** (Ctrl+V / Cmd+V) to replace the entire content
8. **Save** the file

#### Option B: Manual Entry (5 Minutes)

If the script doesn't work, manually edit `morning_email_input.json`:

```json
{
  "email_summary": "15 unread emails: Team updates, Client feedback",
  "key_emails": [
    {
      "from": "Sender Name <email@example.com>",
      "subject": "Email Subject Here",
      "snippet": "First few words of the email content..."
    }
  ],
  "custom_tasks": [
    "Your custom task here"
  ]
}
```

**Tips for manual entry:**
- Check your inbox
- Copy sender email, subject, and first sentence
- Add 3-5 most important emails
- Add any custom tasks you want to track

## ▶️ Run the Skill

```bash
python scripts/generate_morning_briefing_final.py
```

**Output location:**
- 📊 `./outputs/morning-briefing-YYYYMMDD.png` - Static image
- 🌐 `./outputs/morning-briefing-YYYYMMDD.html` - Interactive webpage

## 🌐 Open Interactive Webpage

**Windows:**
```bash
start outputs/morning-briefing-*.html
```

**Mac:**
```bash
open outputs/morning-briefing-*.html
```

**Linux:**
```bash
xdg-open outputs/morning-briefing-*.html
```

Or just double-click the HTML file in your file explorer!

## 📱 For Other Email Providers

### Outlook / Hotmail
1. Open Outlook web or app
2. View your inbox
3. Copy email details (sender, subject, preview)
4. Paste into `morning_email_input.json`

### QQ Mail (QQ邮箱)
1. 打开QQ邮箱
2. 查看收件箱
3. 复制发件人、主题、预览内容
4. 粘贴到 `morning_email_input.json`

### 163 Mail (网易邮箱)
1. 打开163邮箱
2. 查看收件箱
3. 复制邮件信息
4. 更新JSON文件

### Any Other Email Provider
Just copy the sender, subject, and a brief snippet from your emails into the JSON format!

## 🎯 What You Get

### Static Image Dashboard
- Beautiful visual design with your tasks
- Color-coded priorities (High/Medium/Low)
- Perfect for desktop wallpaper
- Quick reference throughout the day

### Interactive Webpage
- Click tasks to mark as complete ✅
- Progress bar updates automatically
- Task statistics (total, completed, remaining)
- State saves automatically (localStorage)
- Works offline in any browser

## 💡 Pro Tips

1. **Daily routine**: Run this every morning to plan your day
2. **Desktop wallpaper**: Set the PNG image as your wallpaper
3. **Browser bookmark**: Keep the HTML page open in a pinned tab
4. **Team sharing**: Share the HTML page with teammates
5. **Quick update**: Re-run the script anytime to refresh your tasks

## 🆘 Troubleshooting

### Gmail API Issues

**"credentials.json not found"**
- Download from Google Cloud Console (see Method 1, Step 1)
- Move to skill directory: `mv ~/Downloads/client_secret_*.json ./credentials.json`

**"Access blocked: This app's request is invalid"**
- Make sure OAuth Consent Screen is configured
- Add your email as a test user
- Use "Desktop app" not "Web application"

**"Browser doesn't open for authorization"**
- Manually visit the URL shown in terminal
- Copy the authorization code
- Paste it back in terminal

### Manual Entry Issues

**Gmail console script doesn't work?**
- Make sure you're in the inbox view (not a specific email)
- Try refreshing Gmail and running the script again
- If still not working, use Option B (manual entry)

### General Issues

**Image generation fails?**
- Check that `AI_GATEWAY_API_KEY` environment variable is set
- Verify Python 3.6+ is installed

**HTML page doesn't open?**
- Check the `./outputs/` folder exists
- Verify the HTML file was created
- Try opening manually from file explorer

**ModuleNotFoundError: No module named 'google'**
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 📚 Next Steps

- Read `README.md` for detailed documentation
- Customize prompts in `references/prompt_templates.md`
- Modify visual style in `scripts/generate_morning_briefing_final.py`
- Star the repo if you find it useful! ⭐

---

**Repository**: https://github.com/Y1fe1-Yang/morning-routine-skill
**Made with ❤️ using Claude Code**
