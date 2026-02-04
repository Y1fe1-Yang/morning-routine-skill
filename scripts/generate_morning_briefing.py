#!/usr/bin/env python3
"""
Morning Briefing Generator - Simplified & Fast
Works with ANY email provider - no IMAP/API setup needed!
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path


def get_user_input_mode():
    """Check if running in interactive mode or with pre-provided data."""
    # Check if email data is provided via environment variable or file
    email_data_env = os.getenv('MORNING_EMAIL_DATA')
    email_data_file = Path('./morning_email_input.json')

    if email_data_env:
        return json.loads(email_data_env)
    elif email_data_file.exists():
        with open(email_data_file, 'r') as f:
            return json.load(f)
    else:
        return None


def create_sample_input():
    """Create a sample input template for users."""
    sample = {
        "email_summary": "3 unread emails: Project meeting invite, Client feedback, Team update",
        "key_emails": [
            {
                "from": "boss@company.com",
                "subject": "Project Review Meeting Tomorrow",
                "snippet": "Let's meet at 2pm to discuss Q1 progress"
            },
            {
                "from": "client@example.com",
                "subject": "Feedback on Proposal",
                "snippet": "We've reviewed your proposal and have some questions"
            }
        ],
        "custom_tasks": [
            "Prepare slides for 2pm meeting",
            "Follow up with design team"
        ]
    }

    output_file = Path('./morning_email_input.json')
    with open(output_file, 'w') as f:
        json.dump(sample, indent=2, fp=f)

    print(f"✓ Sample input template created: {output_file}")
    print("\nEdit this file with your email info, then run the script again!")
    return None


def extract_tasks_from_data(email_data):
    """Extract tasks from provided email data."""
    tasks = []

    # User's custom tasks (highest priority)
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

            # Simple heuristic: look for action words
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
    """Generate simple AI task suggestions."""
    suggestions = []

    # Common morning tasks
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

    # Always suggest inbox cleanup
    suggestions.append({
        'task': 'Archive or organize processed emails',
        'priority': 'low',
        'source': 'ai'
    })

    return suggestions[:2]  # Max 2 AI suggestions


def generate_visual_dashboard(email_summary, tasks, output_path):
    """Generate visual dashboard using generate-image skill."""
    print("🎨 Generating visual dashboard...")

    # Count tasks by priority
    high_priority = [t for t in tasks if t['priority'] == 'high']
    medium_priority = [t for t in tasks if t['priority'] == 'medium']
    low_priority = [t for t in tasks if t['priority'] == 'low']

    # Build task list text
    task_lines = []
    for i, task in enumerate(tasks[:8], 1):  # Max 8 tasks
        emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(task['priority'], '⚪')
        task_lines.append(f"{i}. {emoji} {task['task']}")

    tasks_text = '\n'.join(task_lines) if task_lines else "No tasks for today"

    today = datetime.now().strftime("%A, %B %d, %Y")

    # Create image generation prompt
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

    # Call generate-image skill
    import subprocess
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
    print("☀️  MORNING BRIEFING GENERATOR")
    print("=" * 60)

    # Check for input data
    email_data = get_user_input_mode()

    if not email_data:
        print("\n⚠️  No email data provided.")
        print("\nTwo ways to provide your email info:")
        print("\n1. CREATE INPUT FILE (Recommended):")
        print("   I'll create a template file you can edit")

        create_sample = input("\nCreate sample input file? (y/n): ").strip().lower()
        if create_sample == 'y':
            create_sample_input()
            return 0

        print("\n2. PROVIDE DATA VIA ENVIRONMENT:")
        print("   export MORNING_EMAIL_DATA='{\"email_summary\":\"...\",\"key_emails\":[...]}'")

        return 1

    # Extract email summary
    email_summary = email_data.get('email_summary', 'Email data provided')
    print(f"\n📧 Email summary: {email_summary}")

    # Extract tasks
    print("\n📋 Extracting tasks...")
    tasks = extract_tasks_from_data(email_data)

    # Generate AI suggestions
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
