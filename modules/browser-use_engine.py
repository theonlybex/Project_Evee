# Browser-use_engine - This module is used to control the browser using voice commands!
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI

class Engine:
    def __init__(self):
       # Initialize OpenAI API and browser
       self.llm = ChatOpenAI(model="gpt-4o-mini", api_key = os.getenv("OPENAI_API_KEY"))
       self.browser = Browser()

    async def execute_voice_command(self):
        # Read from audiototext file
        try:
            with open("audiototext.txt", "r") as file:
                text = file.read()
        except FileNotFoundError:
            return "error: File not found"

        # Call for an agent with command
        agent = Agent(task=text,llm=self.llm, browser = self.browser)

        # Run agent
        await agent.run()

        # Return status (success or failure)
        return "Success"

    def save_results(self):
        # Log for results
        # Save to a file
        pass