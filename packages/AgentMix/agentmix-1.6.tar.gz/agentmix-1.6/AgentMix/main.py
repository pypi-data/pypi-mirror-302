import os
import httpx
import asyncio
import colorama
import subprocess
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin  # You may need to install this library

# Initialize colorama for Windows
colorama.init()


# Inside AgentMix/main.py

def main():
    # Your base code logic goes here
    print("Hello from AgentMix")

# Your other functions and classes can be defined here too


# Enter your API key here
CONFIG_FILE = 'config.json'

def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            return config.get('api_key')
    return None

def save_api_key(api_key):
    with open(CONFIG_FILE, 'w') as file:
        json.dump({'api_key': api_key}, file)

def get_api_key():
    api_key = load_api_key()
    if not api_key:
        api_key = input("Please enter your Groq API key: ")
        save_api_key(api_key)
    return api_key

def main():
    api_key = get_api_key()
    print(f"Using API Key: {api_key}")
    # Your base code logic goes here

class Color:
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    WHITE = colorama.Fore.WHITE
    RESET = colorama.Fore.RESET

class Agent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.memory = []  # Memory to store conversation history for each agent

    async def process(self, user_input: str) -> str:
        try:
            api_key = get_api_key()
            if not api_key:
                return "Error: API key is missing."

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # Add user input to the memory (conversation context)
            self.memory.append({"role": "user", "content": user_input})

            # Prepare the messages with memory
            messages = [{"role": "system", "content": self.system_prompt}] + self.memory

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": "llama3-groq-70b-8192-tool-use-preview" if self.name != "Chat" else "llama-3.1-70b-versatile",
                        "messages": messages
                    },
                    timeout=30.0
                )
            response.raise_for_status()

            # Get the agent's response and store it in memory
            response_content = response.json()["choices"][0]["message"]["content"]
            self.memory.append({"role": "assistant", "content": response_content})
            return response_content
        except httpx.HTTPStatusError as e:
            return f"Error: HTTP {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Error: {str(e)}"
        except KeyError:
            return "Error: Unexpected response format from Groq API"

    def clear_memory(self):
        """Clear the memory when switching agents or closing the session."""
        self.memory = []

import os
import httpx
import asyncio
import colorama
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# ... (previous code remains the same)

class WebScrapingAgent(Agent):
    """Agent responsible for web scraping and analyzing the content."""

    async def process(self, user_input: str) -> str:
        try:
            url = user_input.strip()
            if not url.startswith("http"):
                return "Error: Invalid URL. Please enter a valid website link.", ""
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
            
            # Scraping the webpage content
            content = response.text
            
            # Analyze the content using BeautifulSoup to extract various elements
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract text content
            full_text = soup.get_text(separator='\n', strip=True)
            
            # Extract meta information
            meta_info = self.extract_meta_info(soup)
            
            # Extract links
            links = self.extract_links(soup, url)
            
            # Extract images
            images = self.extract_images(soup, url)
            
            # Extract structured data
            structured_data = self.extract_structured_data(soup)
            
            # Combine all extracted information
            scraped_data = {
                'text': full_text,
                'meta_info': meta_info,
                'links': links,
                'images': images,
                'structured_data': structured_data
            }
            
            # Send the scraped data to the analysis function
            analysis = await self.analyze_data(scraped_data)
            return analysis, str(scraped_data)
        except httpx.HTTPStatusError as e:
            return f"Error: HTTP {e.response.status_code} - {e.response.text}", ""
        except httpx.RequestError as e:
            return f"Error: {str(e)}", ""

    def extract_meta_info(self, soup):
        meta_info = {}
        meta_info['title'] = soup.title.string if soup.title else ''
        meta_info['description'] = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else ''
        meta_info['keywords'] = soup.find('meta', attrs={'name': 'keywords'})['content'] if soup.find('meta', attrs={'name': 'keywords'}) else ''
        return meta_info

    def extract_links(self, soup, base_url):
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            link_text = link.text.strip()
            links.append({'url': full_url, 'text': link_text})
        return links

    def extract_images(self, soup, base_url):
        images = []
        for img in soup.find_all('img', src=True):
            full_url = urljoin(base_url, img['src'])
            alt_text = img.get('alt', '')
            images.append({'url': full_url, 'alt': alt_text})
        return images

    def extract_structured_data(self, soup):
        structured_data = []
        for script in soup.find_all('script', type='application/ld+json'):
            structured_data.append(script.string)
        return structured_data

    async def analyze_data(self, scraped_data: dict) -> str:
        # Prepare a summary of the scraped data for analysis
        summary = f"""
        Analyze the following scraped website data:
        
        1. Title: {scraped_data['meta_info'].get('title', 'N/A')}
        2. Description: {scraped_data['meta_info'].get('description', 'N/A')}
        3. Keywords: {scraped_data['meta_info'].get('keywords', 'N/A')}
        4. Number of links: {len(scraped_data['links'])}
        5. Number of images: {len(scraped_data['images'])}
        6. Text content (first 500 characters): {scraped_data['text'][:500]}...
        7. Structured data available: {'Yes' if scraped_data['structured_data'] else 'No'}
        
        Please provide a detailed analysis of this website based on the scraped information.
        """
        
        self.memory.append({"role": "user", "content": summary})

        # Prepare the messages for the AI model
        messages = [{"role": "system", "content": "You are an AI that generates detailed analyses based on scraped website data."}] + self.memory
        
        try:
            api_key = get_api_key()
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": "llama-3.1-70b-versatile",
                        "messages": messages
                    },
                    timeout=30.0
                )
            response.raise_for_status()

            response_content = response.json()["choices"][0]["message"]["content"]
            return response_content
        except httpx.HTTPStatusError as e:
            return f"Error: HTTP {e.response.status_code} - {e.response.text}"
        except httpx.RequestError as e:
            return f"Error: {str(e)}"

# ... (rest of the code remains the same)

class CommandAgent(Agent):
    """Agent responsible for generating and executing CMD commands."""

    async def process(self, user_input: str) -> str:
        command = await super().process(user_input)
        try:
            subprocess.Popen(f'start cmd /k {command}', shell=True)
            return f"Command executed: {command}"
        except Exception as e:
            return f"Error executing command: {str(e)}"

class OmniAgent:
    def __init__(self):
        self.agents = {
            "coder": Agent("Coder", "You are an expert programmer. Provide only the code asked for, without any explanations or comments. Your response should be pure, executable code."),
            "writer": Agent("Writer", "You are a skilled writer. Create articles, blog posts, and scripts. Create more human-like content and use SEO and big vocabulary."),
            "chat": Agent("Chat", "You are a friendly conversational AI. Engage in natural dialogue."),
            "web": WebScrapingAgent("Web", "You are an agent that scrapes websites. Get the content of the given link and return an analysis."),
            "command": CommandAgent("Command", "You are only allowed to generate cmd terminal based commands only. No extra sentences or explanations.")
        }
        self.current_agent = self.agents["chat"]  # Default to "chat"
        self.coder_files_dir = r"C:\Users\Diyon\Desktop\agentmix\coder files"
        os.makedirs(self.coder_files_dir, exist_ok=True)

    def display_code(self, code):
        if self.current_agent.name == "Coder":
            print(code)  # Show the code normally without a white box

    async def run(self):
       


        print(f"{Color.GREEN}Agent mix is running. You can switch agents with /coder, /writer, /chat, /web, or /command.{Color.RESET}")
        print(f"{Color.YELLOW}Start by entering a command like '/coder [prompt]' or just start talking with the current agent.{Color.RESET}")

        while True:
            user_input = input(f"{Color.YELLOW}> {Color.RESET}").strip()

            if user_input.startswith("/coder"):
                self.current_agent.clear_memory()  # Clear memory when switching agents
                self.current_agent = self.agents["coder"]
                print(f"{Color.GREEN}Switched to Coder agent. Please enter your coding request.{Color.RESET}")
                user_input = input(f"{Color.YELLOW}> {Color.RESET}").strip()
            elif user_input.startswith("/writer"):
                self.current_agent.clear_memory()  # Clear memory when switching agents
                self.current_agent = self.agents["writer"]
                print(f"{Color.GREEN}Switched to Writer agent. Please enter your writing request.{Color.RESET}")
                user_input = input(f"{Color.YELLOW}> {Color.RESET}").strip()
            elif user_input.startswith("/chat"):
                self.current_agent.clear_memory()  # Clear memory when switching agents
                self.current_agent = self.agents["chat"]
                print(f"{Color.GREEN}Switched to Chat agent. How can I assist you today?{Color.RESET}")
                user_input = input(f"{Color.YELLOW}> {Color.RESET}").strip()
            elif user_input.startswith("/web"):
                self.current_agent.clear_memory()  # Clear memory when switching agents
                self.current_agent = self.agents["web"]
                print(f"{Color.GREEN}Switched to Web agent. Please paste the website URL.{Color.RESET}")
                user_input = input(f"{Color.YELLOW}> {Color.RESET}").strip()
            elif user_input.startswith("/command"):
                self.current_agent.clear_memory()  # Clear memory when switching agents
                self.current_agent = self.agents["command"]
                print(f"{Color.GREEN}Switched to Command agent. Please enter your command request.{Color.RESET}")
                user_input = input(f"{Color.YELLOW}> {Color.RESET}").strip()
            elif user_input.lower() in ["exit", "quit"]:
                print("Exiting agent mix. Goodbye!")
                break

            if self.current_agent.name == "Web":
                response, scraped_data = await self.current_agent.process(user_input)
                print(response)
                
                # Automatically switch to Chat agent with scraped data
                self.current_agent = self.agents["chat"]
                self.current_agent.clear_memory()
                self.current_agent.memory.append({"role": "system", "content": f"You are a friendly conversational AI. The following is the content of a webpage that was just scraped. Use this information to answer the user's questions:\n\n{scraped_data}"})
                print(f"{Color.GREEN}Switched to Chat agent. You can now ask questions about the scraped website.{Color.RESET}")
            else:
                response = await self.current_agent.process(user_input)
                print(response)

            # New code for handling Coder agent response
            if self.current_agent.name == "Coder":
                save_file = input(f"{Color.YELLOW}Do you want to save this code to a file? (y/n): {Color.RESET}").strip().lower()
                if save_file == 'y':
                    file_name = input(f"{Color.YELLOW}Enter the file name with extension: {Color.RESET}").strip()
                    file_path = os.path.join(self.coder_files_dir, file_name)
                    with open(file_path, 'w') as f:
                        f.write(response)
                    print(f"{Color.GREEN}File saved as {file_path}{Color.RESET}")
                    
                    open_file = input(f"{Color.YELLOW}Do you want to open the file? (y/n): {Color.RESET}").strip().lower()
                    if open_file == 'y':
                        os.startfile(file_path)

# Run the agent framework
if __name__ == "__main__":
    if not get_api_key():
        print(f"{Color.YELLOW}Please enter your Groq API key in the GROQ_API_KEY variable at the top of the script before running.{Color.RESET}")
    else:
        agent_framework = OmniAgent()
        asyncio.run(agent_framework.run())