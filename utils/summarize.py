from google import genai
import json
import os
from dotenv import load_dotenv
from utils import usage_tracker

load_dotenv()

client = genai.Client()


def summarize_data(data):
    json_string = json.dumps(data)

    prompt = f"""
    You are a data summarization assistant. 
    Analyze the provided JSON data. The 'details' field contains HTML; parse it intelligently.
    
    OUTPUT INSTRUCTION:
    1. Output using HTML formatting supported by Telegram.
    2. Do NOT output JSON. 
    3. Do NOT use Markdown code blocks (like ```json or ```).
    4. Use emojis to make the message visually appealing.
    5. Supported tags: <b>, <strong>, <i>, <em>, <u>, <s>, <del>, <strike>, <spoiler>, <a href="...">, <code>, <pre>.
    
    REQUIRED FORMAT:
    <b>Title:</b> [Competition Title]
    <b>Organizer:</b> [Organizer Name]
    <b>Date:</b> [Start Date Of Competition - if not found, say "See details"]
    <b>Link:</b> <a href="[Competition URL]">Apply Now</a>
    
    <b>Description:</b>
    [A concise summary (max 3-4 sentences) describing the competition's purpose, prize pool, and the flow of the rounds. Use <i>italics</i> or <b>bold</b> for emphasis where appropriate.]

    DATA:
    {json_string}
    """

    if not usage_tracker.check_rate_limits():
        return None

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=prompt
    )

    usage_tracker.increment_daily_count()
    return response.text


if __name__ == "__main__":
    try:
        with open("./competitionSampleOutput.json", "r") as f:
            competition_data = json.load(f)
    except FileNotFoundError:
        with open("./utils/competitionSampleOutput.json", "r") as f:
            competition_data = json.load(f)
    summary = summarize_data(competition_data)
    print(summary)
