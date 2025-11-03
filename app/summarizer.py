from bs4 import BeautifulSoup
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

def summarize_articles():
    """
    Scrapes headlines from The Hacker News and summarizes them using an AI model.
    Returns: summary text (str)
    """
    try:
        url = "https://thehackernews.com/"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")
        content_headlines = soup.find_all("h2", class_="home-title")
        headlines = [entry.text.strip() for entry in content_headlines]

        if not headlines:
            return "No headlines found."

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY
        )

        completions = client.chat.completions.create(
            model="z-ai/glm-4.5-air:free",
            messages=[
                {"role": "system", "content": "You are an AI that summarizes cybersecurity headlines."},
                {"role": "user", "content": f"Summarize the following articles:\n{headlines}"}
            ]
        )

        return completions.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"


