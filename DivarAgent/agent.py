import os
import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openai/gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def scrape_website(url: str) -> list[dict]:

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching HTML from {url}: {e}"

    except requests.exceptions.RequestException as e:
        print(f"Error scraping website: {e}")
        return []

root_agent = Agent(
    name="DivarAgent",
    model=model,
    description=(
        "Agent to answer questions about Divar."
    ),
    instruction=("""
        You are a helpful agent who works at Divar (Divar (Persian: دیوار; lit. 'wall') is an Iranian Persian classified ads and E-commerce mobile app, and an online platform for users in Iran founded in Iran in 2012 with sections devoted to real estate, vehicles, goods, community service, Industrial equipment and jobs. On average, Divar’s users post more than 139.7 million new ads & over 53.1 million users open the app annually based on the latest published annual report.). 
        To answer questions about the content of a specific URL, you must first use the 'scrape_website' tool to fetch the webpage's HTML.Once you have the HTML, analyze it to answer the user's question.

        """),
    tools=[scrape_website]

)