# Browser-use_engine - This module is used to control the browser using voice commands!
import os
import json
import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent, BrowserSession
from browser_use.llm import ChatOpenAI

class Engine:
    def __init__(self):
       # Initialize OpenAI API and browser session
       self.llm = ChatOpenAI(
           model="gpt-4o-mini", 
           api_key = os.getenv("OPENAI_API_KEY"),
           temperature = 0.0,  # Faster responses
           )
       
       # Configure browser using browser_use's BrowserSession
       self.browser_session = BrowserSession(
           headless=False,                    # Run in background (no visible window)
           window_size={"width": 1920, "height": 1080},  # Window size (browser_use format)
           viewport={"width": 1920, "height": 1080},     # Viewport size
           slow_mo=0,                        # No delays for speed
           # Performance optimizations
           args=[
               '--disable-images',           # Don't load images for speed
               '--disable-javascript',       # Disable JS if not needed
               '--disable-plugins',          # Disable plugins
               '--disable-extensions',       # Disable extensions
               '--no-sandbox',              # Faster startup
               '--disable-dev-shm-usage'    # Better performance
           ]
       )

    async def executeCommand(self):
        # Read from audiototext file
        try:
            with open("audiototext.txt", "r") as file:
                text = file.read()
        except FileNotFoundError:
            return "error: File not found"

        # Create agent with the configured browser session
        agent = Agent(
            task=text, 
            llm=self.llm, 
            browser_session=self.browser_session,
            use_vision=False,                # Disable vision for speed
            max_actions_per_step=5,          # Limit actions for efficiency
            )

        # Run agent
        history = await agent.run()

        # Return status (success or failure)
        results = {
            'success': True,
            'urls_visited': history.urls() if hasattr(history, 'urls') else [],
            'extracted_content': history.extracted_content() if hasattr(history, 'extracted_content') else [],
            'final_result': history.final_result() if hasattr(history, 'final_result') else None,
        }
        
        # Auto-save results
        self.save_results(results)
        return results 

    def save_results(self, results):
        # Log for results
        # Save to a file
        with open("results.json", "w") as file:
           json.dump(results, file, indent=2)
        print("Results saved to results.json") 
        