# ☀️ Morning Routine Automator

Automate your morning workflow with AI-powered email analysis, task extraction, and dual-format output (static image dashboard + interactive webpage).

![Morning Briefing Example](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 📧 **Universal Email Support** - Works with Gmail, Outlook, QQ Mail, 163 Mail, Foxmail, and any email provider
- 🎯 **Smart Task Extraction** - AI analyzes emails and extracts actionable tasks
- 🤖 **AI Task Suggestions** - Generates intelligent task recommendations
- 🖼️ **Static Image Dashboard** - Beautiful visual dashboard with English-only text
- 🌐 **Interactive Webpage** - Dynamic HTML with task tracking and progress bar
- 💾 **Persistent State** - Webpage remembers completed tasks using localStorage
- 🚀 **Zero Setup** - No OAuth, no API keys, no complex configuration

## 🎬 Quick Start (3 Steps)

### Step 1: Install the Skill

```bash
# Download and install
git clone https://github.com/Y1fe1-Yang/morning-routine-skill.git
cd morning-routine-skill
```

### Step 2: Create Your Email Input JSON

**Method 1: Quick Gmail Export (Recommended)**

1. Open Gmail in your browser
2. Open browser console (F12 → Console tab)
3. Paste this script and press Enter:

```javascript
// Gmail Email Extractor - Copy this entire script
(function() {
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

  console.log('Copy this JSON:');
  console.log(JSON.stringify(output, null, 2));
  copy(JSON.stringify(output, null, 2));
  alert('JSON copied to clipboard! Paste it into morning_email_input.json');
})();
```

4. The JSON will be automatically copied to your clipboard
5. Paste it into `morning_email_input.json`

**Method 2: Manual Entry**

Edit `morning_email_input.json`:

```json
{
  "email_summary": "15 unread emails: Team updates, Client feedback, Project deadlines",
  "key_emails": [
    {
      "from": "Boss <boss@company.com>",
      "subject": "Q1 Review Meeting - Tomorrow 2PM",
      "snippet": "Please prepare slides for quarterly review"
    }
  ],
  "custom_tasks": [
    "Prepare Q1 review slides"
  ]
}
```

**Method 3: For Other Email Providers**

- **Outlook**: View inbox → Copy email details manually
- **QQ Mail/163 Mail**: Check inbox → Fill in the JSON template
- **Any Email App**: Just copy sender, subject, and preview text

### Step 3: Generate Your Morning Briefing

```bash
python scripts/generate_morning_briefing_final.py
```

**Output:**
- 📊 `./outputs/morning-briefing-YYYYMMDD.png` - Static image dashboard
- 🌐 `./outputs/morning-briefing-YYYYMMDD.html` - Interactive webpage

Open the HTML file in your browser to track tasks throughout the day!

## 📸 Example Outputs

### Static Image Dashboard
- Clean visual design with date and email summary
- Prioritized task list with color indicators
- English-only text for perfect rendering
- Perfect for desktop wallpaper or quick reference

### Interactive Webpage
- Click tasks to mark as complete
- Real-time progress bar
- Task statistics (total, completed, remaining)
- State persists across browser sessions
- Works offline

## 🔧 Environment Variables (Optional)

```bash
# Optional: Set output directory
export MORNING_ROUTINE_OUTPUT_DIR="./custom-outputs"

# Optional: Provide email data directly (skip JSON file)
export MORNING_EMAIL_DATA='{"email_summary":"...","key_emails":[...],"custom_tasks":[]}'
```

The skill automatically uses `AI_GATEWAY_API_KEY` from your environment for image generation.

## 📚 Email Provider Compatibility

| Provider | Support | Method |
|----------|---------|--------|
| Gmail | ✅ | Console script or manual |
| Outlook / Hotmail | ✅ | Manual entry |
| QQ Mail (QQ邮箱) | ✅ | Manual entry |
| 163 Mail (网易邮箱) | ✅ | Manual entry |
| Foxmail | ✅ | Manual entry |
| Yahoo Mail | ✅ | Manual entry |
| ProtonMail | ✅ | Manual entry |
| iCloud Mail | ✅ | Manual entry |
| Any other | ✅ | Manual entry |

## 🎯 Use Cases

- **Desktop Wallpaper**: Use the static image as your daily task reminder
- **Team Sharing**: Share the HTML page with your team for collaborative task tracking
- **Daily Planning**: Review tasks in the morning and track progress throughout the day
- **Email Triage**: Quickly identify important emails requiring action
- **Task Management**: Let AI suggest follow-up tasks you might have missed

## 🛠️ Advanced Usage

### Customize AI Prompts

Edit `references/prompt_templates.md` to customize:
- Email summarization style
- Task extraction criteria
- AI suggestion types
- Motivational messages

### Adjust Visual Style

Modify `scripts/generate_morning_briefing_final.py` to change:
- Color scheme
- Layout design
- Font sizes
- Task priority indicators

## 📖 Documentation

- **SKILL.md** - Complete skill documentation
- **references/prompt_templates.md** - LLM prompt templates
- **assets/report_template.md** - Report formatting template

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use and modify for your needs.

## 🌟 Star History

If you find this useful, please star the repository!

---

**Made with ❤️ using Claude Code**
