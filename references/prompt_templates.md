# Prompt Templates for Morning Routine

This file contains prompt templates for various components of the morning routine workflow.

## Email Summarization Prompt

Use this prompt structure when summarizing emails:

```
Analyze the following emails and create a concise summary:

[EMAIL CONTENT HERE]

Provide:
1. A brief overview (2-3 sentences) of key themes and topics
2. List of important emails requiring attention
3. Count of urgent vs non-urgent messages
4. Any deadlines or time-sensitive items mentioned

Format the summary in a clear, scannable format.
```

## Task Extraction Prompt

Use this prompt to extract actionable tasks from email content:

```
Extract actionable tasks from the following email content:

[EMAIL CONTENT HERE]

For each task identified:
1. Write a clear, actionable task description (start with verb)
2. Assign priority (high/medium/low) based on:
   - High: Urgent deadlines, explicit requests from management/clients
   - Medium: Important but not time-critical, follow-ups needed
   - Low: FYI items, nice-to-have actions
3. Note the email source (sender name or subject)

Return only clear, specific action items. Ignore:
- General FYI messages with no action needed
- Automated notifications unless they require response
- Meeting invites already on calendar

Format as a list of tasks with priority indicators.
```

## AI Task Suggestions Prompt

Use this prompt to generate intelligent task suggestions:

```
Based on this morning's email summary and extracted tasks:

EMAIL SUMMARY:
[EMAIL SUMMARY HERE]

EXTRACTED TASKS:
[EXTRACTED TASKS HERE]

Generate 2-4 additional task suggestions that would help the user:
1. Follow-up tasks not explicitly mentioned but implied
2. Proactive actions based on email themes
3. Preparation tasks for mentioned meetings/deadlines
4. Quick wins that could be accomplished today

Keep suggestions:
- Specific and actionable
- Realistic for a single day
- Complementary to existing tasks (not duplicates)
- Focused on high-value activities

Format as a prioritized list with brief rationale for each suggestion.
```

## Motivational Image Generation Prompt

Use this prompt structure when calling the generate-image skill:

```
Create a motivational image with the following characteristics:

CONTEXT:
- Number of tasks today: [TASK_COUNT]
- Number of emails: [EMAIL_COUNT]
- Key themes: [EXTRACTED_THEMES]

IMAGE REQUIREMENTS:
1. Style: Modern, uplifting, professional
2. Visual theme: Choose based on task context
   - Many tasks → organized, focused imagery (desk, planning, productivity)
   - Few tasks → spacious, opportunity-focused imagery (open road, horizon)
   - Technical tasks → clean, tech-inspired imagery
   - Creative tasks → colorful, artistic imagery
3. Include inspiring text overlay:
   - Main message: Short, powerful phrase related to the day ahead
   - Optional subtitle: Relevant quote or affirmation
4. Color palette: Warm, energizing colors (avoid dark/somber tones)
5. Composition: Balanced, not cluttered, suitable as desktop background

Avoid:
- Generic stock photo aesthetics
- Overly abstract imagery
- Text that's hard to read
- Cliché motivational phrases

Generate an image that feels personalized to today's specific context and challenges.
```

## Example Workflow Integration

When orchestrating the morning routine, use prompts in this sequence:

1. **Fetch emails** → Apply email summarization prompt
2. **Analyze summary** → Apply task extraction prompt
3. **Review extracted tasks** → Apply AI task suggestions prompt
4. **Gather context** → Prepare image generation prompt with gathered data
5. **Generate image** → Call generate-image skill with personalized prompt
6. **Compile report** → Assemble all components into markdown

Each step should pass relevant context to the next step for coherent workflow.
