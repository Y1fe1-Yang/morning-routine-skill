---
name: morning-routine
description: Automate morning workflows to kickstart the day. Execute multi-step routine including email summary, task extraction with AI suggestions, and personalized motivational image generation. Use when the user requests their morning routine, morning briefing, daily startup, or wants to automate checking emails, generating today's tasks, or creating morning motivation. Trigger phrases include "run my morning routine", "generate morning briefing", "start my day", "morning automation", or "daily kickoff".
---

# Morning Routine Automator

Automate your morning workflow with a comprehensive routine that fetches email summaries, extracts actionable tasks, generates AI-powered task suggestions, and creates a personalized motivational image—all compiled into a single markdown report.

## Overview

The Morning Routine skill orchestrates a multi-step workflow:

1. **Email Summary** - Check inbox and generate concise summary of important messages
2. **Task Extraction** - Parse emails to identify actionable items
3. **AI Task Suggestions** - Generate intelligent task recommendations based on email context
4. **Motivational Image** - Create personalized inspirational image using generate-image skill
5. **Compiled Report** - Output everything in a formatted markdown file

## Quick Start

### Recommended: JSON-Based Morning Briefing

Generate your morning briefing with simple JSON input:

```bash
python scripts/generate_morning_briefing_final.py
```

**How it works:**
1. Check your emails in any email client (Gmail, Outlook, QQ Mail, etc.)
2. Edit `morning_email_input.json` with email summary and tasks
3. Run script to generate both static image and dynamic webpage

**JSON format example:**
```json
{
  "email_summary": "1606 unread emails: WeWork announcement, Security alerts, GitHub updates",
  "key_emails": [
    {
      "from": "Sender <email@example.com>",
      "subject": "Email subject",
      "snippet": "Brief description"
    }
  ],
  "custom_tasks": [
    "Review important announcement",
    "Check security alert"
  ]
}
```

**Outputs:**
- **Static Image** (`morning-briefing-YYYYMMDD.png`) - English-only text, clean visual dashboard
- **Dynamic Webpage** (`morning-briefing-YYYYMMDD.html`) - Interactive task tracker with progress

**Benefits:**
- Universal - Works with ANY email provider
- Simple - No OAuth, no API keys, no complex setup
- Dual output - Both static image and interactive webpage
- English-optimized - Clean, readable image generation
- Task tracking - Click to complete tasks in the webpage

### Alternative: Provide Email Data via Environment Variable

Set email data directly without editing JSON file:

```bash
export MORNING_EMAIL_DATA='{"email_summary":"3 unread emails","key_emails":[...],"custom_tasks":["Task 1","Task 2"]}'
python scripts/generate_morning_briefing_final.py
```

### Environment Variables

The skill uses these environment variables:

**Always available:**
- `AI_GATEWAY_API_KEY` - Already configured in sandbox for image generation
- `MORNING_ROUTINE_OUTPUT_DIR` - Custom output directory (default: `./outputs`)

**For automatic email fetching (V2 - requires system configuration):**
- `CAPY_GMAIL_ACCESS_TOKEN` - Gmail OAuth access token (auto-provided by system)
- `CAPY_GMAIL_REFRESH_TOKEN` - Gmail OAuth refresh token (auto-provided by system)
- `CAPY_GMAIL_CLIENT_ID` - OAuth client ID (auto-provided by system)
- `CAPY_GMAIL_CLIENT_SECRET` - OAuth client secret (auto-provided by system)
- `CAPY_USER_EMAIL` - User's email address (auto-provided by system)

**For manual mode:**
- `MORNING_EMAIL_DATA` - Optional: provide email data directly via environment variable

### Legacy Email Fetching (Optional)

For automated email fetching, see `references/email_setup.md` and `references/gmail_api_setup.md`. Note: These methods require complex setup and may be slow with large inboxes. The simplified approach above is recommended.

## Workflow Details

### Step 1: Email Summary

**Objective:** Fetch and summarize recent emails.

**Implementation approach:**

1. Use the send-email skill or check email inbox (the exact mechanism depends on available email access)
2. Apply the email summarization prompt from `references/prompt_templates.md`
3. Extract key information:
   - Unread count
   - Important messages requiring attention
   - Urgent vs non-urgent classification
   - Time-sensitive items and deadlines

**Example prompt usage:**

```python
# After fetching email content
summary = apply_llm_prompt(
    template=load_prompt("email_summarization"),
    email_content=fetched_emails
)
```

See `references/prompt_templates.md` for the complete email summarization prompt template.

### Step 2: Task Extraction

**Objective:** Identify actionable tasks from email content.

**Implementation approach:**

1. Parse email summary and individual messages
2. Apply task extraction prompt from `references/prompt_templates.md`
3. For each task, determine:
   - Clear action verb (e.g., "Review", "Respond to", "Complete")
   - Priority level (high/medium/low)
   - Source reference (sender or subject line)

**Priority guidelines:**

- **High**: Urgent deadlines, explicit requests from management/clients
- **Medium**: Important but not time-critical, follow-ups needed
- **Low**: FYI items, nice-to-have actions

**What to filter out:**

- General FYI messages with no action needed
- Automated notifications unless they require response
- Meeting invites already on calendar

### Step 3: AI Task Suggestions

**Objective:** Generate intelligent task recommendations based on context.

**Implementation approach:**

1. Analyze email summary and extracted tasks
2. Apply AI task suggestions prompt from `references/prompt_templates.md`
3. Generate 2-4 suggestions that:
   - Complement existing tasks (no duplicates)
   - Are specific and actionable
   - Focus on high-value activities
   - Include follow-up tasks implied but not explicitly mentioned

**Example suggestions:**

- "Prepare talking points for tomorrow's client meeting" (when meeting is mentioned in email)
- "Review project documentation before the 2pm review" (proactive preparation)
- "Follow up with Sarah on the budget proposal" (implied action from thread)

### Step 4: Motivational Image Generation

**Objective:** Create personalized motivational image using generate-image skill.

**Implementation approach:**

1. Gather context:
   - Number of tasks
   - Email count
   - Key themes from emails (technical, creative, meetings, etc.)
2. Use the generate-image skill with personalized prompt
3. Apply image generation prompt template from `references/prompt_templates.md`

**Image customization based on context:**

- **Many tasks** → Organized, focused imagery (productivity, planning)
- **Few tasks** → Spacious, opportunity-focused imagery (open road, horizon)
- **Technical tasks** → Clean, tech-inspired imagery
- **Creative tasks** → Colorful, artistic imagery

**Call generate-image skill:**

```bash
# The skill automatically uses AI_GATEWAY_API_KEY from environment
# Customize prompt based on gathered context
```

See `references/prompt_templates.md` for detailed image prompt structure.

### Step 5: Compile Report

**Objective:** Assemble all components into formatted markdown report.

**Implementation approach:**

1. Use template from `assets/report_template.md`
2. Fill in sections:
   - Date and timestamp
   - Email summary with counts
   - Prioritized task list with emoji indicators
   - Embedded motivational image
3. Output to `./outputs/morning-routine-YYYYMMDD.md`

**Task formatting:**

- 🔴 High priority
- 🟡 Medium priority
- 🟢 Low priority

Each task includes source tag: *[from email]* or *[from ai]*

## Integration with Other Skills

### send-email Skill

Use for fetching emails and potentially sending the morning report:

```bash
# Check inbox (implementation depends on send-email capabilities)
# The skill may need to be adapted based on available email access methods
```

### generate-image Skill

Automatically invoked for motivational image creation:

```python
# The generate_routine.py script calls generate-image skill
# Uses AI_GATEWAY_API_KEY from environment (already configured)
```

## Customization

### Modify Prompts

Edit `references/prompt_templates.md` to customize:

- Email summarization style
- Task extraction criteria
- AI suggestion types
- Image generation themes

### Adjust Report Template

Edit `assets/report_template.md` to change:

- Report structure
- Section headings
- Formatting style

### Extend Workflow

Modify `scripts/generate_routine.py` to add:

- Calendar integration
- Weather information
- News headlines
- Custom data sources

## Example Output

```markdown
# ☀️ Morning Routine Report

**Monday, February 03, 2026**

---

## 📧 Email Summary

**Unread emails:** 12

Key highlights:
- Project review meeting scheduled for 2pm
- Client feedback on proposal received
- Team standup notes shared

---

## ✅ Today's Tasks

1. 🔴 Review and respond to client proposal feedback *[from email]*
2. 🟡 Prepare slides for 2pm project review *[from ai]*
3. 🟡 Follow up with design team on mockups *[from email]*
4. 🟢 Review team standup notes *[from email]*

---

## 💪 Daily Motivation

![Daily Motivation](./outputs/motivation.png)

*Your personalized motivation for today*

---

*Generated at 2026-02-03 08:30:15 by Morning Routine Automator*
```

## Troubleshooting

**No emails fetched:**
- Verify email access configuration
- Check send-email skill is available
- Ensure email credentials/permissions are set

**Image generation fails:**
- Verify AI_GATEWAY_API_KEY environment variable is set
- Check generate-image skill is available
- Review error messages for API issues

**Script execution errors:**
- Ensure Python 3.6+ is installed
- Check file permissions on scripts directory
- Verify output directory is writable

## Dual Output Mode

The final workflow generates TWO outputs for maximum flexibility:

### 1. Static Image Dashboard

**File:** `morning-briefing-YYYYMMDD.png`

**Contents:**
- Header with date and email summary
- Todo list with priority indicators (largest section)
- Motivational message at bottom
- **English-only text** for clean, readable output

**Use cases:**
- Desktop wallpaper
- Quick reference throughout the day
- Easy to share via messaging apps
- Print and put on desk

### 2. Dynamic Webpage

**File:** `morning-briefing-YYYYMMDD.html`

**Features:**
- Interactive task completion (click to mark done)
- Progress bar showing completion percentage
- Task statistics (total, completed, remaining)
- localStorage persistence (state saved across sessions)
- Responsive design with modern UI

**Use cases:**
- Active task tracking throughout the day
- Share with team members
- Track progress in real-time
- Works offline in any browser

### How It Works

1. Run `python scripts/generate_morning_briefing_final.py`
2. Script reads email data from `morning_email_input.json`
3. Extracts tasks from emails and generates AI suggestions
4. Creates static image with English-only text (ASCII filtering)
5. Creates dynamic HTML webpage with interactive features
6. Both files saved to `./outputs/` directory

### Benefits

- **Two formats** - Static reference + interactive tracker
- **English-optimized** - Clean image rendering without character issues
- **Progress tracking** - Check off tasks as you complete them
- **Persistent state** - Webpage remembers completed tasks
- **Zero setup** - No authentication, works with all email providers

## Email Provider Compatibility

The simplified morning briefing approach supports ALL email providers:

- Gmail
- Outlook / Hotmail
- QQ Mail (QQ邮箱)
- 163 Mail (网易邮箱)
- Foxmail
- Yahoo Mail
- ProtonMail
- iCloud Mail
- Any other email service

You simply check your emails manually and provide the information to the script. No complex IMAP setup, no OAuth configuration, no API keys needed.

## Resources

**Recommended Scripts:**
- **scripts/generate_morning_briefing_final.py** - JSON input, dual output (static image + dynamic webpage)
- **morning_email_input.json** - Input file for email data and custom tasks

**Legacy Scripts:**
- **scripts/generate_morning_briefing.py** - Original version (static image only)
- **scripts/generate_visual_routine.py** - Legacy visual mode with IMAP
- **scripts/generate_routine.py** - Legacy markdown report generator
- **scripts/generate_morning_briefing_v2.py** - OAuth attempt (deprecated)
- **scripts/generate_morning_briefing_complete.py** - Gmail API attempt (deprecated)
- **scripts/fetch_emails_auto.py** - OAuth fetcher (deprecated)
- **scripts/fetch_emails_simple.py** - Gmail API fetcher (deprecated)
- **scripts/fetch_emails.py** - IMAP fetcher (deprecated)
- **scripts/fetch_emails_gmail_api.py** - Gmail API with manual OAuth (deprecated)

**References:**
- **references/prompt_templates.md** - LLM prompt templates for all workflow steps
- **references/email_setup.md** - Legacy guide for IMAP email access
- **references/gmail_api_setup.md** - Legacy guide for Gmail API setup
- **assets/report_template.md** - Markdown template for classic mode
