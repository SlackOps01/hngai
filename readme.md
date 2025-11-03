🧠 Cybersecurity News Summarizer
A Python-based automation tool that scrapes The Hacker News for the latest cybersecurity headlines and summarizes them using AI via OpenRouter — giving you concise daily security briefings.

🚀 Features


🔍 Scrapes the latest cybersecurity headlines from The Hacker News


🧠 Uses OpenRouter’s AI models (GLM-4.5-Air) for text summarization


⚙️ Built with simple, clean Python code


🕒 Can be automated to run daily


💬 Outputs short, readable summaries of current cyber threats and trends



🧩 Tech Stack


Python 3.10+


BeautifulSoup4 – for HTML parsing


Requests – for fetching web content


OpenRouter API – for AI summarization


python-dotenv – for secure API key management



📦 Installation
Clone this repository:

cd cybernews-summarizer

Install dependencies:
pip install -r requirements.txt

Create a .env file in the project root and add your OpenRouter API key:
API_KEY=your_openrouter_api_key_here


⚙️ Usage
Run the script to fetch and summarize the latest headlines:
python main.py

Example output:
✅ Fetching latest cybersecurity news...

🔐 Summary:
- A new phishing campaign is targeting cloud accounts using fake MFA prompts.
- Cisco patches critical RCE vulnerabilities in its router firmware.
- Ransomware activity increases across healthcare organizations this week.


🧱 Project Structure
.
├── main.py
├── .env
├── requirements.txt
├── README.md


⚡ API Model
This project uses OpenRouter as the AI gateway.
Default model: z-ai/glm-4.5-air:free
You can modify this line in main.py to switch to a different model:
model="z-ai/glm-4.5-air:free"

For faster responses, you may use:


gpt-4o-mini


claude-3-haiku


mistral-small



🧠 How It Works


Scrapes headlines from The Hacker News using BeautifulSoup.


Sends the list of headlines to an AI model on OpenRouter.


Returns a summarized version of the top stories.



🧩 Example Integration Ideas


🕵️ Daily cybersecurity digest in Slack or Discord


📈 Automated threat intel dashboard updates


📰 Cybersecurity blog automation


⚙️ FastAPI endpoint for dynamic summaries



🧰 Requirements


Python 3.10 or newer


An OpenRouter API key (free at https://openrouter.ai/)



🧑‍💻 Author
Sholarin Olanrewaju
Cybersecurity enthusiast & backend engineer
🌐 GitHub · 🧠 Powered by AI and automation

