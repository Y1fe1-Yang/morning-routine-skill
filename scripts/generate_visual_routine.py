#!/usr/bin/env python3
"""
Visual Morning Routine Generator
Creates a single image with email summary and todo list embedded
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path


def fetch_emails():
    """Fetch emails using the fetch_emails script."""
    print("📧 Fetching emails...")

    script_dir = Path(__file__).parent
    fetch_script = script_dir / "fetch_emails.py"

    try:
        result = subprocess.run(
            ["python3", str(fetch_script)],
            capture_output=True,
            text=True,
            check=False
        )

        # Parse JSON output (skip any print statements before JSON)
        output_lines = result.stdout.strip().split('\n')
        for i, line in enumerate(output_lines):
            if line.strip().startswith('['):
                json_text = '\n'.join(output_lines[i:])
                return json.loads(json_text)

        print("Warning: Could not parse email JSON, using empty list")
        return []

    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []


def summarize_emails_with_llm(emails):
    """Summarize emails using LLM (Claude will do this interactively)."""
    if not emails:
        return {
            'count': 0,
            'unread': 0,
            'summary': 'No emails found',
            'themes': []
        }

    unread_count = sum(1 for e in emails if e.get('unread', False))

    # Create a brief summary
    subjects = [e['subject'] for e in emails[:5]]  # Top 5

    return {
        'count': len(emails),
        'unread': unread_count,
        'summary': f"{len(emails)} emails in last 24 hours",
        'top_subjects': subjects,
        'emails': emails
    }


def extract_tasks_with_llm(email_data):
    """Extract tasks from emails (Claude will do this interactively)."""
    # Placeholder - Claude will extract tasks
    return {
        'extracted': [],
        'ai_suggested': []
    }


def generate_visual_todo_image(email_summary, tasks, output_path):
    """Generate a visual image with todo list using AI image generation."""
    print("🎨 Generating visual todo list image...")

    # Build the prompt for image generation
    unread = email_summary.get('unread', 0)
    total = email_summary.get('count', 0)

    # Format tasks for the prompt
    task_list = []
    all_tasks = tasks.get('extracted', []) + tasks.get('ai_suggested', [])

    for i, task in enumerate(all_tasks[:8], 1):  # Max 8 tasks
        priority = task.get('priority', 'medium')
        emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '⚪')
        task_list.append(f"{i}. {emoji} {task.get('task', 'Task')}")

    tasks_text = '\n'.join(task_list) if task_list else "No tasks for today"

    # Create comprehensive prompt for image generation
    today = datetime.now().strftime("%A, %B %d, %Y")

    prompt = f"""Create a beautiful, modern morning routine dashboard image with this exact layout:

HEADER SECTION (top):
- Large text: "Morning Routine - {today}"
- Subtext: "{unread} unread emails ({total} total in last 24h)"

TODO LIST SECTION (center, most prominent):
{tasks_text}

MOTIVATION SECTION (bottom):
- Inspiring quote: "Build Something Meaningful Today"

VISUAL STYLE:
- Clean, modern design with soft gradients
- Warm color palette: soft oranges, blues, whites
- Morning light aesthetic with subtle sunrise gradient background
- Professional typography, highly readable
- Organized layout like a digital dashboard
- Suitable as desktop wallpaper (16:9 or 16:10)
- Minimalist, not cluttered

LAYOUT:
- Header at top (15% of image)
- Todo list in center (60% of image) - LARGEST SECTION
- Motivation at bottom (25% of image)

The image should feel like a premium productivity app screenshot - clean, modern, and inspiring."""

    print(f"Generating image with {len(all_tasks)} tasks...")

    # Use the generate-image skill via command line
    try:
        # Find generate_image.py in the generate-image skill
        generate_script = "/home/node/.claude/skills/generate-image/scripts/generate_image.py"

        result = subprocess.run(
            [
                "python3",
                generate_script,
                prompt,
                "--model", "google/gemini-3-pro-image-preview",
                "--output", output_path
            ],
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)
        return output_path

    except subprocess.CalledProcessError as e:
        print(f"Error generating image: {e.stderr}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def main():
    """Main orchestration function."""
    print("=" * 60)
    print("☀️  VISUAL MORNING ROUTINE GENERATOR")
    print("=" * 60)

    # Set output directory
    output_dir = os.getenv('MORNING_ROUTINE_OUTPUT_DIR', './outputs')
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Fetch emails
    emails = fetch_emails()

    # Step 2: Summarize emails
    email_summary = summarize_emails_with_llm(emails)
    print(f"\n✓ Email summary: {email_summary['unread']} unread, {email_summary['count']} total")

    # Step 3: Extract tasks (will be done by Claude interactively)
    print("\n⚠️  Task extraction requires Claude to analyze email content")
    print("    Returning email data for Claude to process...")

    # Output email data as JSON for Claude to process
    print("\n--- EMAIL DATA ---")
    print(json.dumps(email_summary, indent=2))

    # Return path where image should be saved
    timestamp = datetime.now().strftime("%Y%m%d")
    output_path = f"{output_dir}/morning-routine-{timestamp}.png"

    print(f"\n--- OUTPUT PATH ---")
    print(output_path)

    return {
        'email_summary': email_summary,
        'output_path': output_path
    }


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
