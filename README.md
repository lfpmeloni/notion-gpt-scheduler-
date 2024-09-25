# notion-gpt-scheduler-

# Notion-GPT Scheduler

Automate your daily schedule by integrating Notion with OpenAI's GPT model. This script retrieves activities from a Notion database and generates a new daily schedule based on your tasks, instructions, and past schedule history.

Demo
https://github.com/lfpmeloni/notion-gpt-scheduler-/blob/main/docs/Notion%20GPT%20Scheduler.gif

## Features
- Input your routine or instructions into a Notion page.
- The script retrieves the information, processes it, and generates a detailed schedule based on your needs.
- Automatically generates a schedule using GPT-3.5.
- Posts the new schedule back into Notion.
- Flexibility to handle dynamic Notion table structures.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/lfpmeloni/notion-gpt-scheduler-.git
   ```

2. Navigate to the project directory:
   ```bash
   cd notion-gpt-scheduler
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your **Notion** and **OpenAI** API keys:
   ```bash
   NOTION_API_KEY=your_notion_key
   OPENAI_API_KEY=your_openai_key
   ```

## Usage

1. Modify the Notion page IDs in the `agent.py` file, lines 139 to 141:
   ```python
    ACTIVITIES_DATABASE_ID = "your_activity_page_id"
    PROGRAM_DAY_PAGE_ID = "your_schedule_page_id"
    INSTRUCTIONS_PAGE_ID = "your_instruction_page_id"
   ```

2. Run the script:
   ```bash
   python agent.py
   ```

### Setup Guide for Notion:
1. **Create a Notion Integration**:
   - Go to [Notion API](https://www.notion.so/my-integrations) and create a new integration.
   - Copy the API key and add it to your `.env` file.

2. **Configure Access**:
   - Share the Notion page with your integration by selecting "Share" and adding your integration from the share menu.

3. **Page Setup**:
   - Create a page in Notion with your daily instructions and task ideas. Example of instructions:
  

## Contributing
Contributions are welcome! Please submit a pull request or open an issue.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
