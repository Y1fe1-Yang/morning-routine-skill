#!/usr/bin/env python3
"""
Morning Briefing Generator - Final Version
Simple JSON input, generates both static image and dynamic webpage
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
import subprocess

def get_email_data():
    """Get email data from JSON file or environment variable."""
    # Check environment variable
    email_data_env = os.getenv('MORNING_EMAIL_DATA')
    if email_data_env:
        return json.loads(email_data_env)

    # Check file
    email_data_file = Path('./morning_email_input.json')
    if email_data_file.exists():
        with open(email_data_file, 'r') as f:
            return json.load(f)

    return None

def extract_tasks_from_data(email_data):
    """Extract tasks from email data."""
    tasks = []

    # User's custom tasks (highest priority)
    if 'custom_tasks' in email_data:
        for task in email_data['custom_tasks']:
            tasks.append({
                'task': task,
                'priority': 'high',
                'source': 'user',
                'completed': False
            })

    # Extract from key emails
    if 'key_emails' in email_data:
        for email in email_data['key_emails']:
            subject = email.get('subject', '')
            snippet = email.get('snippet', '')

            action_words = ['meeting', 'review', 'feedback', 'deadline', 'urgent', 'asap']
            if any(word in subject.lower() or word in snippet.lower() for word in action_words):
                # Use English translation for subject
                task_text = f"Respond to: {subject}"
                tasks.append({
                    'task': task_text,
                    'priority': 'medium',
                    'source': 'email',
                    'completed': False
                })

    return tasks

def generate_ai_suggestions(email_summary, existing_tasks):
    """Generate AI task suggestions."""
    suggestions = []

    if 'meeting' in email_summary.lower():
        suggestions.append({
            'task': 'Review meeting agenda and prepare notes',
            'priority': 'medium',
            'source': 'ai',
            'completed': False
        })

    if 'feedback' in email_summary.lower() or 'response' in email_summary.lower():
        suggestions.append({
            'task': 'Draft responses to important emails',
            'priority': 'low',
            'source': 'ai',
            'completed': False
        })

    suggestions.append({
        'task': 'Archive or organize processed emails',
        'priority': 'low',
        'source': 'ai',
        'completed': False
    })

    return suggestions[:2]

def translate_to_english(text):
    """Simple translation helper - keep only ASCII characters for image generation."""
    # Remove non-ASCII characters for image generation
    return ''.join(char for char in text if ord(char) < 128)

def generate_static_image(email_summary, tasks, output_path):
    """Generate static image dashboard (English only)."""
    print("🎨 Generating static image dashboard...")

    # Build task list (English only)
    task_lines = []
    for i, task in enumerate(tasks[:8], 1):
        emoji = {'high': 'HIGH', 'medium': 'MED', 'low': 'LOW'}.get(task['priority'], 'TASK')
        # Clean task text - remove non-ASCII
        clean_task = translate_to_english(task['task'])
        task_lines.append(f"{i}. [{emoji}] {clean_task}")

    tasks_text = '\n'.join(task_lines) if task_lines else "No tasks for today"
    today = datetime.now().strftime("%A, %B %d, %Y")

    # Clean email summary
    clean_summary = translate_to_english(email_summary)

    prompt = f"""Create a clean morning briefing dashboard:

HEADER (top 15%):
================================================
Morning Briefing - {today}
{clean_summary}
================================================

TODO LIST (center 65% - MAIN FOCUS):
================================================
Today's Tasks:

{tasks_text}
================================================

MOTIVATION (bottom 20%):
================================================
Make Today Count
Focus on what matters most
================================================

STYLE:
- Modern, clean dashboard
- Warm sunrise gradient (peach/orange to light blue)
- Professional typography, highly readable
- Todo list is largest section
- Minimalist, organized
- 16:9 desktop wallpaper
- Premium productivity app aesthetic
- IMPORTANT: Use only English text, clear and readable"""

    try:
        result = subprocess.run([
            'python3',
            '/home/node/.claude/skills/generate-image/scripts/generate_image.py',
            prompt,
            '--model', 'google/gemini-2.5-flash-image',
            '--output', output_path
        ], capture_output=True, text=True, check=True, timeout=45)

        print(f"✓ Static image generated: {output_path}")
        return output_path
    except subprocess.TimeoutExpired:
        print("✗ Image generation timed out")
        return None
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating image: {e.stderr}")
        return None

def generate_dynamic_webpage(email_summary, tasks, output_path):
    """Generate dynamic HTML webpage with interactive task tracking."""
    print("📄 Generating dynamic webpage...")

    today = datetime.now().strftime("%A, %B %d, %Y")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Morning Briefing - {today}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .date {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .email-summary {{
            background: #f8f9fa;
            padding: 20px 30px;
            border-left: 4px solid #667eea;
            margin: 20px;
            border-radius: 8px;
        }}

        .email-summary h2 {{
            color: #667eea;
            margin-bottom: 10px;
        }}

        .tasks {{
            padding: 20px 30px;
        }}

        .tasks h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}

        .task-item {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .task-item:hover {{
            border-color: #667eea;
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }}

        .task-item.completed {{
            background: #f8f9fa;
            opacity: 0.7;
        }}

        .task-item.completed .task-text {{
            text-decoration: line-through;
            color: #6c757d;
        }}

        .task-checkbox {{
            width: 24px;
            height: 24px;
            border: 2px solid #667eea;
            border-radius: 50%;
            margin-right: 15px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }}

        .task-item.completed .task-checkbox {{
            background: #667eea;
            border-color: #667eea;
        }}

        .task-checkbox::after {{
            content: '✓';
            color: white;
            font-size: 16px;
            font-weight: bold;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .task-item.completed .task-checkbox::after {{
            opacity: 1;
        }}

        .task-content {{
            flex: 1;
        }}

        .task-text {{
            font-size: 1.1em;
            color: #333;
            margin-bottom: 5px;
        }}

        .task-meta {{
            display: flex;
            gap: 10px;
            font-size: 0.85em;
        }}

        .task-priority {{
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 600;
        }}

        .task-priority.high {{
            background: #fee;
            color: #c00;
        }}

        .task-priority.medium {{
            background: #ffd;
            color: #880;
        }}

        .task-priority.low {{
            background: #efe;
            color: #080;
        }}

        .task-source {{
            color: #6c757d;
        }}

        .progress-section {{
            padding: 20px 30px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }}

        .progress-bar {{
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin-top: 10px;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }}

        .motivation {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 30px;
            text-align: center;
            font-size: 1.3em;
            color: #333;
            font-weight: 500;
        }}

        .stats {{
            display: flex;
            justify-content: space-around;
            padding: 20px 30px;
            background: white;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}

        .stat-label {{
            color: #6c757d;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>☀️ Morning Briefing</h1>
            <div class="date">{today}</div>
        </div>

        <div class="email-summary">
            <h2>📧 Email Summary</h2>
            <p>{email_summary}</p>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-value" id="total-tasks">{len(tasks)}</div>
                <div class="stat-label">Total Tasks</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="completed-tasks">0</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="remaining-tasks">{len(tasks)}</div>
                <div class="stat-label">Remaining</div>
            </div>
        </div>

        <div class="tasks">
            <h2>✅ Today's Tasks</h2>
            <div id="task-list">
"""

    # Add tasks
    for i, task in enumerate(tasks):
        priority_class = task['priority']
        priority_label = task['priority'].upper()
        source_icon = {'user': '👤', 'email': '📧', 'ai': '🤖'}.get(task['source'], '📝')

        html_content += f"""
                <div class="task-item" data-task-id="{i}">
                    <div class="task-checkbox"></div>
                    <div class="task-content">
                        <div class="task-text">{task['task']}</div>
                        <div class="task-meta">
                            <span class="task-priority {priority_class}">{priority_label}</span>
                            <span class="task-source">{source_icon} {task['source']}</span>
                        </div>
                    </div>
                </div>
"""

    html_content += """
            </div>
        </div>

        <div class="progress-section">
            <h3>Progress</h3>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill" style="width: 0%">0%</div>
            </div>
        </div>

        <div class="motivation">
            💪 Make Today Count - Focus on what matters most
        </div>
    </div>

    <script>
        // Load saved state from localStorage
        let taskStates = JSON.parse(localStorage.getItem('taskStates')) || {};

        // Apply saved states
        document.querySelectorAll('.task-item').forEach(item => {
            const taskId = item.dataset.taskId;
            if (taskStates[taskId]) {
                item.classList.add('completed');
            }
        });

        // Update progress
        function updateProgress() {
            const tasks = document.querySelectorAll('.task-item');
            const completed = document.querySelectorAll('.task-item.completed').length;
            const total = tasks.length;
            const remaining = total - completed;
            const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

            document.getElementById('completed-tasks').textContent = completed;
            document.getElementById('remaining-tasks').textContent = remaining;
            document.getElementById('progress-fill').style.width = percentage + '%';
            document.getElementById('progress-fill').textContent = percentage + '%';
        }

        // Add click handlers
        document.querySelectorAll('.task-item').forEach(item => {
            item.addEventListener('click', function() {
                const taskId = this.dataset.taskId;
                this.classList.toggle('completed');

                // Save state
                if (this.classList.contains('completed')) {
                    taskStates[taskId] = true;
                } else {
                    delete taskStates[taskId];
                }
                localStorage.setItem('taskStates', JSON.stringify(taskStates));

                updateProgress();
            });
        });

        // Initial progress update
        updateProgress();
    </script>
</body>
</html>
"""

    # Write HTML file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ Dynamic webpage generated: {output_path}")
        return output_path
    except Exception as e:
        print(f"✗ Error generating webpage: {e}")
        return None

def main():
    """Main function."""
    print("=" * 60)
    print("☀️  MORNING BRIEFING GENERATOR - FINAL VERSION")
    print("=" * 60)

    # Get email data
    email_data = get_email_data()

    if not email_data:
        print("\n⚠️  No email data provided")
        print("\nPlease create 'morning_email_input.json' with your email info")
        print("Run the script again to generate template")
        return 1

    # Extract email summary
    email_summary = email_data.get('email_summary', 'Email data provided')
    print(f"\n📧 Email summary: {email_summary}")

    # Extract and generate tasks
    print("\n📋 Extracting tasks...")
    tasks = extract_tasks_from_data(email_data)

    print("🤖 Generating AI suggestions...")
    ai_suggestions = generate_ai_suggestions(email_summary, tasks)
    tasks.extend(ai_suggestions)

    print(f"✓ Total tasks: {len(tasks)}")

    # Generate outputs
    output_dir = os.getenv('MORNING_ROUTINE_OUTPUT_DIR', './outputs')
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d")
    image_path = f"{output_dir}/morning-briefing-{timestamp}.png"
    html_path = f"{output_dir}/morning-briefing-{timestamp}.html"

    # Generate both static image and dynamic webpage
    image_result = generate_static_image(email_summary, tasks, image_path)
    webpage_result = generate_dynamic_webpage(email_summary, tasks, html_path)

    # Summary
    print("\n" + "=" * 60)
    print("✓ MORNING BRIEFING COMPLETE!")
    print("=" * 60)

    if image_result:
        print(f"📊 Static Image: {image_result}")
    if webpage_result:
        print(f"🌐 Dynamic Webpage: {webpage_result}")
        print(f"   Open in browser to track tasks interactively!")

    print(f"📝 Total tasks: {len(tasks)}")
    print("=" * 60)

    return 0 if (image_result or webpage_result) else 1

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
