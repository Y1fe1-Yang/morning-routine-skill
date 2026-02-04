#!/usr/bin/env python3
"""
Morning Routine Generator
Orchestrates the morning routine workflow: email summary, task extraction, and motivational image.
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_command(cmd, description=""):
    """Execute a shell command and return output."""
    print(f"→ {description}..." if description else f"→ Running: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e.stderr}")
        return None


def get_email_summary():
    """Fetch recent emails and generate summary."""
    print("\n📧 Fetching emails...")

    # Check if send-email skill is available
    # For now, we'll create a placeholder that Claude can populate
    email_summary = {
        "unread_count": 0,
        "important_emails": [],
        "summary": "No emails fetched yet. Claude will use send-email skill to check inbox."
    }

    return email_summary


def extract_tasks_from_emails(email_data):
    """Extract actionable tasks from email content."""
    tasks = []

    # This will be handled by Claude using LLM
    # Placeholder for task extraction logic
    tasks.append({
        "source": "email",
        "task": "Extracted tasks will be populated by Claude using LLM",
        "priority": "medium"
    })

    return tasks


def generate_ai_suggestions(email_summary, extracted_tasks):
    """Generate AI task suggestions based on context."""
    suggestions = []

    # This will be handled by Claude using LLM
    # Placeholder for AI suggestion logic
    suggestions.append({
        "source": "ai",
        "task": "AI-generated suggestions will be populated by Claude",
        "priority": "low"
    })

    return suggestions


def generate_motivational_image(tasks_context):
    """Generate personalized motivational image based on tasks."""
    print("\n🎨 Generating motivational image...")

    # This will use the generate-image skill
    # Return placeholder path that Claude will populate
    image_path = "./outputs/motivation.png"

    print(f"  Image will be generated at: {image_path}")
    return image_path


def create_markdown_report(email_summary, tasks, image_path, output_dir):
    """Create the final morning routine markdown report."""
    print("\n📝 Creating morning routine report...")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%A, %B %d, %Y")

    # Read the report template
    template_path = Path(__file__).parent.parent / "assets" / "report_template.md"

    if template_path.exists():
        with open(template_path, 'r') as f:
            template = f.read()
    else:
        # Fallback template if asset doesn't exist
        template = """# Morning Routine Report
{date}

## 📧 Email Summary

{email_summary}

## ✅ Today's Tasks

{tasks}

## 💪 Daily Motivation

{motivation}

---
*Generated at {timestamp}*
"""

    # Format email summary
    email_section = f"**Unread emails:** {email_summary.get('unread_count', 0)}\n\n"
    email_section += email_summary.get('summary', 'No email summary available.')

    # Format tasks
    tasks_section = ""
    for i, task in enumerate(tasks, 1):
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get('priority', 'medium'), "⚪")
        source_tag = f"*[from {task.get('source', 'unknown')}]*"
        tasks_section += f"{i}. {priority_emoji} {task.get('task', 'Untitled task')} {source_tag}\n"

    # Format motivation section
    motivation_section = f"![Daily Motivation]({image_path})\n\n*Your personalized motivation for today*"

    # Fill template
    report = template.format(
        date=date_str,
        email_summary=email_section,
        tasks=tasks_section,
        motivation=motivation_section,
        timestamp=timestamp
    )

    # Write report
    output_path = Path(output_dir) / f"morning-routine-{datetime.now().strftime('%Y%m%d')}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(report)

    print(f"✓ Report created: {output_path}")
    return str(output_path)


def main():
    """Main orchestration function."""
    print("=" * 60)
    print("☀️  MORNING ROUTINE AUTOMATOR")
    print("=" * 60)

    # Set output directory
    output_dir = os.getenv('MORNING_ROUTINE_OUTPUT_DIR', './outputs')

    # Step 1: Get email summary
    email_summary = get_email_summary()

    # Step 2: Extract tasks from emails
    extracted_tasks = extract_tasks_from_emails(email_summary)

    # Step 3: Generate AI task suggestions
    ai_suggestions = generate_ai_suggestions(email_summary, extracted_tasks)

    # Combine all tasks
    all_tasks = extracted_tasks + ai_suggestions

    # Step 4: Generate motivational image
    tasks_context = {
        "task_count": len(all_tasks),
        "email_count": email_summary.get('unread_count', 0),
        "tasks": all_tasks
    }
    image_path = generate_motivational_image(tasks_context)

    # Step 5: Create markdown report
    report_path = create_markdown_report(email_summary, all_tasks, image_path, output_dir)

    print("\n" + "=" * 60)
    print("✓ Morning routine complete!")
    print(f"  Report: {report_path}")
    print("=" * 60)

    return report_path


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
