# Test the browser engine
import asyncio
from modules.browser_use_engine import Engine

async def main():
    engine = Engine()
    result = await engine.executeCommand()
    print("Results: ",result)
    engine.save_results(result)

asyncio.run(main())
