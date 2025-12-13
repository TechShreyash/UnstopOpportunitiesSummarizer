from google import genai
import json
import os
import logging
from dotenv import load_dotenv
from utils import usage_tracker

load_dotenv()

client = genai.Client()


def summarize_data(data):
    """
    Summarizes the competition data using Gemini AI.

    Args:
        data (dict): The competition data to summarize.

    Returns:
        str: The generated summary in HTML format for Telegram, or None if failed/skipped.
    """
    logging.info("Attempting to summarize competition data...")

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
    6. Format dates as "DD MMM YYYY" (e.g., "12 Jan 2024"). Do NOT include the time. If the input contains time, strip it.
    
    REQUIRED FORMAT:
    <b>Title:</b> [Competition Title]
    <b>Organizer:</b> [Organizer Name]
    <b>Date:</b> [Start Date Of Competition in DD MMM YYYY format - if not found, say "See details"]
    <b>Link:</b> <a href="[Competition URL]">Apply Now</a>
    
    <b>Description:</b>
    [A concise summary (max 3-4 sentences) describing the competition's purpose, prize pool, and the flow of the rounds. Use <i>italics</i> or <b>bold</b> for emphasis where appropriate.]

    DATA:
    {json_string}
    """

    if not usage_tracker.check_rate_limits():
        logging.warning("Rate limit reached. Skipping summarization.")
        return None

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt
        )
        usage_tracker.increment_daily_count()
        logging.info("Summary successfully generated.")
        return response.text
    except Exception as e:
        logging.error(f"Error during summarization with Gemini: {e}")
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Suppress noisy logs from external libraries
    for logger_name in ["google", "urllib3", "httpcore", "httpx", "google_genai"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    try:
        with open("./sampleOutputs/competitionSampleOutput.json", "r") as f:
            competition_data = json.load(f)
    except FileNotFoundError:
        # Fallback to local utils path if running from root
        try:
            with open("./utils/sampleOutputs/competitionSampleOutput.json", "r") as f:
                competition_data = json.load(f)
        except FileNotFoundError:
            logging.error("Sample data file not found.")
            exit(1)

    summary = summarize_data(competition_data)
    print(summary)
