import os
from dotenv import load_dotenv
from notion_client import Client
import openai
import tiktoken

# Load environment variables from .env file
load_dotenv()

# Load keys and credentials from .env
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Notion and OpenAI configurations using loaded keys
notion = Client(auth=NOTION_API_KEY)
openai.api_key = OPENAI_API_KEY

# Function to count tokens for OpenAI usage
def count_tokens(text):
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = tokenizer.encode(text)
    return len(tokens)

# Function to dynamically read and clean activities from a Notion database
def read_notion_activities(database_id):
    response = notion.databases.query(database_id=database_id)
    activities = []

    for result in response['results']:
        properties = result['properties']
        activity = {}
        
        # Extract all properties dynamically, handling any new columns added
        for key, value in properties.items():
            # Depending on the property type, extract its contents dynamically
            if value['type'] == 'title':
                activity[key] = value['title'][0]['plain_text'] if value['title'] else "Unnamed"
            elif value['type'] == 'rich_text':
                activity[key] = " ".join([text_part['plain_text'] for text_part in value['rich_text']])
            elif value['type'] == 'select':
                activity[key] = value['select']['name'] if value['select'] else "No selection"
            elif value['type'] == 'multi_select':
                activity[key] = ", ".join([item['name'] for item in value['multi_select']])
            elif value['type'] == 'number':
                activity[key] = value['number']
            elif value['type'] == 'date':
                activity[key] = value['date']['start'] if value['date'] else "No date"
            elif value['type'] == 'checkbox':
                activity[key] = value['checkbox']
            elif value['type'] == 'url':
                activity[key] = value['url'] or "No URL"
            elif value['type'] == 'email':
                activity[key] = value['email'] or "No email"
            elif value['type'] == 'phone_number':
                activity[key] = value['phone_number'] or "No phone number"
            # Additional handlers can be added as needed for other property types

        activities.append(activity)
    
    print(activities)
    return activities

# Function to dynamically read and clean content from a Notion page
def read_notion_page_content(page_id):
    blocks = notion.blocks.children.list(block_id=page_id).get('results', [])
    content = ""

    # Clean and extract relevant text content from blocks
    for block in blocks:
        block_type = block.get('type')
        block_data = block.get(block_type, {})

        # Extract text from different block types dynamically
        if block_type in ['paragraph', 'heading_1', 'heading_2', 'heading_3']:
            text_elements = block_data.get('rich_text', [])
            text = "".join([part['plain_text'] for part in text_elements])
            content += text + " "
    
    return content.strip()

# Function to generate the daily schedule via ChatGPT
def generate_daily_schedule_chatgpt(activities, instructions, schedule_history):
    prompt = f"""
    Using these activities: {activities}, along with these personal instructions: {instructions}, and the schedule from the previous day: {schedule_history}, suggest a flexible daily plan that accomodates my interests and goals. Optimize the routine, and make any recommendations for adjustments if needed. Also give a overview of what is in the activities list and is not on the daily routine and should be done as soon as possible.
    """

    # Print token count for debugging
    print(f"Tokens in activities: {count_tokens(str(activities))}")
    print(f"Tokens in instructions: {count_tokens(instructions)}")
    print(f"Tokens in schedule history: {count_tokens(schedule_history)}")
    print(f"Total tokens in prompt: {count_tokens(prompt)}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,  # Increase temperature for more creative responses
        top_p=0.95,       # Increase top_p for a more varied response
        max_tokens=1000
    )
    
    suggestion = response['choices'][0]['message']['content']
    return suggestion

# Function to delete the previous day's schedule
def delete_previous_schedule(page_id):
    blocks = notion.blocks.children.list(block_id=page_id).get('results', [])
    
    for block in blocks:
        notion.blocks.delete(block_id=block['id'])

# Function to post the new schedule to Notion
def post_schedule_to_notion(page_id, schedule):
    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": schedule
                            }
                        }
                    ]
                }
            }
        ]
    )

# Main code
ACTIVITIES_DATABASE_ID = "5860dd020f394803a4303d9b5cc5cf85"
PROGRAM_DAY_PAGE_ID = "107e7e0f4b8480d98f36c14557b0cb5f"
INSTRUCTIONS_PAGE_ID = "107e7e0f4b84808183d8c97b9686c435"

# Read activities, instructions, and the previous schedule dynamically
activities = read_notion_activities(ACTIVITIES_DATABASE_ID)
instructions = read_notion_page_content(INSTRUCTIONS_PAGE_ID)
schedule_history = read_notion_page_content(PROGRAM_DAY_PAGE_ID)

# Generate the new daily schedule via ChatGPT
new_schedule = generate_daily_schedule_chatgpt(activities, instructions, schedule_history)

# Delete the previous schedule and post the new one on Notion
delete_previous_schedule(PROGRAM_DAY_PAGE_ID)
post_schedule_to_notion(PROGRAM_DAY_PAGE_ID, new_schedule)

print("Daily schedule successfully updated!")
