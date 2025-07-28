# LinkedIn Login using liengine automation
import asyncio
import sys

# Import the LinkedIn automation engine
try:
    from automations import liengine
    print("✅ LinkedIn engine loaded successfully!")
except ImportError as e:
    print(f"❌ Error importing LinkedIn engine: {e}")
    print("Make sure liengine.py is in the automations/ directory.")
    sys.exit(1)

async def linkedin_login_session():
    """Use liengine to open LinkedIn and handle login"""
    print("🚀 LinkedIn Login Assistant (using liengine)")
    print("=" * 60)
    
    # Get user's credentials from configuration
    try:
        print(f"📁 Using config file: {liengine.config_manager.config_file}")
        
        # Force reload the config to pick up any changes
        liengine.config_manager.config = liengine.config_manager._load_or_create_config()
        
        user_email = liengine.config_manager.config.personal_info['email']
        user_password = liengine.config_manager.config.personal_info.get('linkedin_password', 'PASSWORD_NOT_SET')
        
        print(f"📧 Email from config: {user_email}")
        print(f"🔐 Password found: {'Yes' if user_password != 'PASSWORD_NOT_SET' else 'No'}")
        
        if user_password == 'PASSWORD_NOT_SET':
            print("❌ LinkedIn password not found in config file")
            print("Please add 'linkedin_password' field to personal_info section in test_config_25.json")
            return
            
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        print(f"Config file path: {getattr(liengine.config_manager, 'config_file', 'Unknown')}")
        return
    
    # Create a fully automated LinkedIn login task
    task = f"""
    FULLY AUTOMATED LinkedIn Login Task:
    
    Credentials from config:
    - Email: {user_email}
    - Password: {user_password}
    
    Steps (NO USER INPUT REQUIRED):
    1. Navigate to https://www.linkedin.com
    2. Wait for the page to load completely
    3. Look for login form or "Sign in" button
    4. Fill in the email field with: {user_email}
    5. Fill in the password field with: {user_password}
    6. Click the sign-in button
    7. Wait for successful login (check if we reach LinkedIn homepage)
    8. Confirm login was successful
    9. Keep the browser open and ready for use
    10. Tell the user that LinkedIn is ready and logged in
    
    Important Instructions:
    - DO NOT ask user for any input during login process
    - Use the configured credentials automatically
    - Complete the entire login process without interruption
    - Only use ask_human() if there's a technical error or if login fails
    - Keep browser open at the end for user to browse LinkedIn
    - If login fails, report the error but don't ask for new credentials
    """
    
    try:
        print("🔧 Initializing LinkedIn automation engine...")
        
        # Use proper browser-use imports (same as modules/browser_use_engine.py)
        from browser_use import Agent, BrowserSession
        from browser_use.llm import ChatOpenAI
        import os
        
        # Check for OpenAI API key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("❌ OpenAI API key not found!")
            print("💡 Please set OPENAI_API_KEY environment variable")
            print("   Example: set OPENAI_API_KEY=sk-your-openai-key-here")
            print("   (Note: The DeepSeek key in settings.json won't work for browser-use)")
            return
        
        # Initialize LLM using browser-use's ChatOpenAI (not langchain)
        llm = ChatOpenAI(
            model="gpt-4o-mini", 
            api_key=openai_api_key,
            temperature=0.0
        )
        
        # Configure browser session
        browser_session = BrowserSession(
            headless=False,
            window_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        
        # Create agent using proper browser-use pattern
        agent = Agent(
            task=task, 
            llm=llm, 
            browser_session=browser_session,
            use_vision=False,
            max_actions_per_step=5
        )
        
        print("🌐 Starting LinkedIn login automation...")
        print("📝 The system will:")
        print("   • Open LinkedIn in a browser")
        print("   • Ask for your login credentials")
        print("   • Handle the login process")
        print("   • Keep browser open for your use")
        
        await agent.run()
        
    except Exception as e:
        print(f"❌ Error in LinkedIn automation: {e}")
        print("This might be due to:")
        print("- Missing OpenAI API key")
        print("- Browser-use compatibility issues") 
        print("- Network connectivity problems")
        print("\n💡 Troubleshooting:")
        print("1. Make sure you have an OpenAI API key set")
        print("2. Check: pip install browser-use langchain-openai")
        print("3. Try: playwright install")

def main():
    """Main function"""
    print("🎯 Starting LinkedIn Login with liengine automation...")
    asyncio.run(linkedin_login_session())
    print("👋 Session complete!")

if __name__ == '__main__':
    main() 