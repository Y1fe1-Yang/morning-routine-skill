# 🚀 Quick Start Guide: Morning Routine Skill

## 📦 Installation

```bash
git clone https://github.com/Y1fe1-Yang/morning-routine-skill.git
cd morning-routine-skill
```

## ⚡ Quick Gmail JSON Export (3 Minutes)

### Method 1: Browser Console Script (Fastest)

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

### Method 2: Manual Entry (5 Minutes)

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

**Gmail console script doesn't work?**
- Make sure you're in the inbox view (not a specific email)
- Try refreshing Gmail and running the script again
- If still not working, use Method 2 (manual entry)

**Image generation fails?**
- Check that `AI_GATEWAY_API_KEY` environment variable is set
- Verify Python 3.6+ is installed

**HTML page doesn't open?**
- Check the `./outputs/` folder exists
- Verify the HTML file was created
- Try opening manually from file explorer

## 📚 Next Steps

- Read `README.md` for detailed documentation
- Customize prompts in `references/prompt_templates.md`
- Modify visual style in `scripts/generate_morning_briefing_final.py`
- Star the repo if you find it useful! ⭐

---

**Repository**: https://github.com/Y1fe1-Yang/morning-routine-skill
**Made with ❤️ using Claude Code**
