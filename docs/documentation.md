# Notion-GPT Scheduler Documentation

## Overview
The Notion-GPT Scheduler automates the daily planning process by integrating Notion databases with OpenAI's GPT model. It retrieves tasks from Notion and generates a personalized daily schedule, which is then posted back to Notion.

## Components

### 1. Notion Integration
- **read_notion_activities**: Fetches activities from a Notion database.
- **post_schedule_to_notion**: Posts the generated schedule back to a specific Notion page.

### 2. GPT-3.5 Integration
- **generate_daily_schedule_chatgpt**: Constructs a prompt using tasks and instructions retrieved from Notion, then calls OpenAI's GPT model to generate a daily schedule.

## Extending the Project
- **Adding New Features**: Guidelines on adding new functionality, like integrating with calendar apps or adding reminders.