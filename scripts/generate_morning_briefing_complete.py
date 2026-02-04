#!/usr/bin/env python3
"""
Complete Morning Briefing Generator
Automatically fetches Gmail using your existing credentials!
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

def try_fetch_gmail():
    """Try to fetch emails from Gmail using existing credentials."""
    print("🔍 Attempting to fetch emails from Gmail...")

    try:
        result = subprocess.run(
            ['python3', '/home/node/.claude/skills/morning-routine/scripts/fetch_emails_simple.py'],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            # Parse JSON from output
            lines = result.stdout.split('\n')
            json_started = False
            json_lines = []

            for line in lines:
                if line.strip() == "JSON Output:":
                    json_started = True
                    continue
                if json_started and line.strip().startswith('{'):
                    json_lines.append(line)
                elif json_started and json_lines:
                    json_lines.append(line)
                    if line.strip().endswith('}'):
                        break

            if json_lines:
                json_str = '\n'.join(json_lines)
                return json.loads(json_str)

        # If failed, print error
        if result.stderr:
            print(f"⚠️  {result.stderr}")

        return None
    except subprocess.TimeoutExpired:
        print("⚠️  Gmail fetch timed out")
        return None
    except Exception as e:
        print(f"⚠️  Gmail fetch error: {e}")
        return None

def convert_gmail_data_to_briefing_format(gmail_data):
    """Convert Gmail API response to morning briefing format."""
    emails = gmail_data.get('emails', [])
    unread_count = gmail_data.get('unread_count', 0)

    email_summary = f"{unread_count} unread emails"
    if len(emails) > 0:
        subjects = [email['subject'][:30] for email in emails[:3]]
        email_summary += ": " + ", ".join(subjects)

    key_emails = []
    for email in emails[:5]:
        key_emails.append({
            'from': email['from'],
            'subject': email['subject'],
            'snippet': email.get('snippet', '')[:100]
        })

    return {
        'email_summary': email_summary,
        'key_emails': key_emails,
        'custom_tasks': [],
        'source': 'gmail_automatic'
    }

def get_manual_input():
    """Fallback to manual input if Gmail fetch fails."""
    email_data_env = os.getenv('MORNING_EMAIL_DATA')
    if email_data_env:
        return json.loads(email_data_env)

    email_data_file = Path('./morning_email_input.json')
    if email_data_file.exists():
        with open(email_data_file, 'r') as f:
            return json.load(f)

    return None

def extract_tasks_from_data(email_data):
    """Extract tasks from email data."""
    tasks = []

    # User's custom tasks
    if 'custom_tasks' in email_data:
        for task in email_data['custom_tasks']:
            tasks.append({
                'task': task,
                'priority': 'high',
                'source': 'user'
            })

    # Extract from key emails
    if 'key_emails' in email_data:
        for email in email_data['key_emails']:
            subject = email.get('subject', '')
            snippet = email.get('snippet', '')

            action_words = ['meeting', 'review', 'feedback', 'deadline', 'urgent', 'asap']
            if any(word in subject.lower() or word in snippet.lower() for word in action_words):
                task_text = f"Respond to: {subject}"
                tasks.append({
                    'task': task_text,
                    'priority': 'medium',
                    'source': 'email'
                })

    return tasks

def generate_ai_suggestions(email_summary, existing_tasks):
    """Generate AI task suggestions."""
    suggestions = []

    if 'meeting' in email_summary.lower():
        suggestions.append({
            'task': 'Review meeting agenda and prepare notes',
            'priority': 'medium',
            'source': 'ai'
        })

    if 'feedback' in email_summary.lower() or 'response' in email_summary.lower():
        suggestions.append({
            'task': 'Draft responses to important emails',
            'priority': 'low',
            'source': 'ai'
        })

    suggestions.append({
        'task': 'Archive or organize processed emails',
        'priority': 'low',
        'source': 'ai'
    })

    return suggestions[:2]

def generate_visual_dashboard(email_summary, tasks, output_path):
    """Generate visual dashboard using generate-image skill."""
    print("🎨 Generating visual dashboard...")

    # Build task list
    task_lines = []
    for i, task in enumerate(tasks[:8], 1):
        emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(task['priority'], '⚪')
        task_lines.append(f"{i}. {emoji} {task['task']}")

    tasks_text = '\n'.join(task_lines) if task_lines else "No tasks for today"
    today = datetime.now().strftime("%A, %B %d, %Y")

    prompt = f"""Create a clean morning briefing dashboard:

HEADER (top 15%):
━━━━━━━━━━━━━━━━━━━━━━━━━━━
☀️ Morning Briefing - {today}
📧 {email_summary}
━━━━━━━━━━━━━━━━━━━━━━━━━━━

TODO LIST (center 65% - MAIN FOCUS):
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Today's Tasks:

{tasks_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━

MOTIVATION (bottom 20%):
━━━━━━━━━━━━━━━━━━━━━━━━━━━
💪 "Make Today Count"
Focus on what matters most
━━━━━━━━━━━━━━━━━━━━━━━━━━━

STYLE:
- Modern, clean dashboard
- Warm sunrise gradient (peach/orange → light blue)
- Professional typography, highly readable
- Todo list is largest section
- Minimalist, organized
- 16:9 desktop wallpaper
- Premium productivity app aesthetic"""

    try:
        result = subprocess.run([
            'python3',
            '/home/node/.claude/skills/generate-image/scripts/generate_image.py',
            prompt,
            '--model', 'google/gemini-3-pro-image-preview',
            '--output', output_path
        ], capture_output=True, text=True, check=True)

        print(f"✓ Dashboard generated: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating image: {e.stderr}")
        return None

def main():
    """Main function."""
    print("=" * 60)
    print("☀️  COMPLETE MORNING BRIEFING GENERATOR")
    print("=" * 60)

    # Try automatic Gmail fetch
    gmail_data = try_fetch_gmail()

    if gmail_data:
        print("✓ Emails fetched automatically from Gmail!")
        email_data = convert_gmail_data_to_briefing_format(gmail_data)
    else:
        print("⚠️  Automatic Gmail fetch not available")
        print("   Falling back to manual input mode...")
        email_data = get_manual_input()

        if not email_data:
            print("\n✗ No email data available")
            print("\nOptions:")
            print("1. Authorize Gmail: Run the script again and follow prompts")
            print("2. Manual mode: Create morning_email_input.json with your email info")
            return 1

    # Extract email summary
    email_summary = email_data.get('email_summary', 'Email data provided')
    source = email_data.get('source', 'manual')
    print(f"\n📧 Email summary ({source}): {email_summary}")

    # Extract and generate tasks
    print("\n📋 Extracting tasks...")
    tasks = extract_tasks_from_data(email_data)

    print("🤖 Generating AI suggestions...")
    ai_suggestions = generate_ai_suggestions(email_summary, tasks)
    tasks.extend(ai_suggestions)

    print(f"✓ Total tasks: {len(tasks)}")

    # Generate visual dashboard
    output_dir = os.getenv('MORNING_ROUTINE_OUTPUT_DIR', './outputs')
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d")
    output_path = f"{output_dir}/morning-briefing-{timestamp}.png"

    dashboard = generate_visual_dashboard(email_summary, tasks, output_path)

    if dashboard:
        print("\n" + "=" * 60)
        print("✓ MORNING BRIEFING COMPLETE!")
        print("=" * 60)
        print(f"📊 Dashboard: {dashboard}")
        print(f"📝 Tasks: {len(tasks)}")
        print(f"🔧 Source: {source}")
        print("=" * 60)
        return 0
    else:
        print("\n✗ Failed to generate dashboard")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
