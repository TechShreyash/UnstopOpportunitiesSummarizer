# 🚀 Unstop Opportunities Summarizer

![Unstop Opportunities Banner](assets/banner.png)

An automated tool designed to scrape, analyze, and summarize high-value opportunities (hackathons, competitions, quizzes) from **Unstop**. It uses **Google Gemini AI** to generate concise, readable summaries and instantly sends them to a **Telegram Channel**.

---

## 📱 Demo

Stay updated with the latest opportunities! Join our demo Telegram channel where the bot posts live updates:

👉 **[Join Telegram Channel](https://t.me/UnstopAlertsDaily)**

*(Note: Updates are posted automatically based on the schedule)*

---

## ✨ Features

*   **🔍 Smart Discovery**: Automatically finds top competitions sorted by the highest prize pool.
*   **🧠 AI-Powered Summaries**: Uses **Google Gemini 2.5 Flash Lite** to extract key details (dates, eligibility, rounds) and generate a clean, formatted summary.
*   **⚡ Instant Alerts**: Sends real-time notifications to Telegram with direct apply links.
*   **🛡️ Duplicate Protection**: Keeps track of processed opportunities to prevent spamming.
*   **📉 Rate Limiting**: Intelligent usage tracking to respect API limits.
*   **🤖 Automation Ready**: Designed to run on a schedule (e.g., via GitHub Actions).

---

## ⚙️ How It Works

The system operates in a streamlined pipeline to ensure you never miss a high-value opportunity:

1.  **Search & Filter**: 
    *   The script queries the Unstop API for the latest competitions, prioritizing those with the highest prizes.
    *   It cross-references these results with a local database (`db.txt`) to identify *new* opportunities that haven't been processed yet.

2.  **Data Extraction**:
    *   For every new competition, the system fetches comprehensive details, including eligibility criteria, round structures, and important dates.

3.  **AI Summarization**:
    *   The raw data is sent to **Google Gemini**.
    *   The AI analyzes the content and generates a structured HTML message for Telegram, highlighting the most critical information (Title, Organizer, Prize, Deadline, etc.).

4.  **Notification**:
    *   The generated summary is sent to your configured Telegram channel or chat.

5.  **State Management**:
    *   Successfully processed competition IDs are saved to `db.txt` to ensure they are not repeated in future runs.

---

## 🛠️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/UnstopScrapper.git
    cd UnstopScrapper
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    # or if using uv
    uv sync
    ```

3.  **Configure Environment Variables**

    Copy the `sample.env` file to a new file named `.env`:
    ```bash
    cp sample.env .env
    ```

    Open `.env` and fill in the required details:

    | Variable | Description | How to Get It |
    | :--- | :--- | :--- |
    | `GEMINI_API_KEY` | API Key for Google Gemini AI | [Get it here](https://aistudio.google.com/app/api-keys) |
    | `TELEGRAM_BOT_TOKEN` | Token for your Telegram Bot | Create a bot with [@BotFather](https://t.me/BotFather) |
    | `TELEGRAM_CHAT_ID` | ID of the Telegram Channel/Group | Use [@userinfobot](https://t.me/userinfobot) or similar |
    | `MAX_RPM` | Max requests per minute (Rate Limit) | Default: `6` (Adjust based on your quota) |
    | `MAX_RPD` | Max requests per day (Rate Limit) | Default: `15` (Adjust based on your quota) |

4.  **Run the Scraper**
    ```bash
    python main.py
    ```

    > **⚠️ IMPORTANT:** Before running the code for the first time, make sure to **delete** `db.txt` and `gemini_usage.json` if they exist. These files contain data from the repository's own usage (e.g., GitHub Actions). If you don't delete them, the script will assume many competitions have already been processed and will skip them.

---

## 📂 API Reference

### 1. Search API
Fetches the top 50 opportunities sorted by the highest prize pool.

*   **URL:** `https://unstop.com/api/public/opportunity/search-result?opportunity=all&page=1&per_page=50&sortBy=&orderBy=&filter_condition=&undefined=true`
*   **Method:** `GET`
*   **Sample Output:** [JSON](assets/unstopRawApiResponse/search.json)

### 2. Competition Details API
Fetches comprehensive details for a specific competition using its ID (e.g., `1582532`).

*   **URL:** `https://unstop.com/api/public/competition/{id}`
*   **Example:** `https://unstop.com/api/public/competition/1582532`
*   **Method:** `GET`
*   **Sample Output:** [JSON](assets/unstopRawApiResponse/competition.json)
