# 🚀 Quick Start Guide - Project Evee

Get up and running with Project Evee in just a few minutes!

## 📋 Prerequisites

Before installing Project Evee, make sure you have:

- ✅ **Windows 10/11** (primary support)
- ✅ **Python 3.8+** installed ([Download Python](https://python.org))
- ✅ **Working microphone**
- ✅ **Internet connection**
- ✅ **DeepSeek API Key** ([Get one here](https://platform.deepseek.com/))

## 🎯 Installation Options

### Option 1: Easy Installer (Recommended)

1. **Download** the portable package:
   ```
   project-evee-portable.zip
   ```

2. **Extract** the ZIP file to any folder

3. **Run** the installer:
   ```
   Double-click: INSTALL.bat
   ```

4. **Follow** the installation wizard

### Option 2: Manual Installation

1. **Clone or download** this repository
2. **Open Command Prompt** in the project folder
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python main_gui.py
   ```

## 🛠️ First Time Setup

### 1. Launch Project Evee
- Double-click the desktop shortcut, or
- Run `run_project_evee.bat`, or
- Execute `python main_gui.py`

### 2. Configure API Settings
1. Click the **⚙️ Settings** button
2. Enter your **DeepSeek API Key**
3. Adjust recording timeout if needed (default: 4 seconds)
4. Click **Save Settings**

### 3. Test Your Setup
1. Click **🎤 Start Recording**
2. Say: *"Open calculator"*
3. Wait for transcription to complete
4. Click **🤖 Generate Code**
5. Review the generated code
6. Click **▶️ Execute Code** (if you want to test)

## 🎤 Voice Commands Examples

Try these commands to test different functionalities:

### Basic System Operations
- *"Open notepad"*
- *"Take a screenshot"*
- *"Open calculator and compute 15 plus 27"*

### Web Browsing
- *"Open Chrome and go to YouTube"*
- *"Search for funny cat videos on Google"*
- *"Open a new browser tab"*

### File Operations
- *"Create a new text file on desktop"*
- *"Open file explorer"*
- *"Show desktop"*

### Application Control
- *"Minimize all windows"*
- *"Switch to next window"*
- *"Close current application"*

## 🎛️ Using the Interface

### Control Panel (Left Side)
- **🎤 Start Recording**: Begin voice capture
- **🤖 Generate Code**: Create automation from voice
- **▶️ Execute Code**: Run the generated automation
- **💾 Save Code**: Export code to file
- **⚙️ Settings**: Configure application

### Output Tabs (Right Side)
- **📝 Transcription**: View recognized speech
- **💻 Generated Code**: See the AI-created code
- **📊 History**: Track all your commands

## 🔧 Troubleshooting

### Common Issues

**❓ "No transcription available"**
- Check microphone permissions
- Ensure microphone is working
- Try speaking louder and clearer

**❓ "API Error"**
- Verify your DeepSeek API key
- Check internet connection
- Ensure API key has credits

**❓ "Execution failed"**
- Review the generated code first
- Some automation may require specific apps to be open
- Try simpler commands first

**❓ "Models still loading"**
- Wait for Whisper model to download (first time only)
- This can take a few minutes on first launch

### Getting Help

1. **Check the History tab** for error messages
2. **Review generated code** before execution
3. **Start with simple commands** and work up to complex ones
4. **Check GitHub Issues** for known problems

## 💡 Pro Tips

### For Better Voice Recognition
- Speak clearly and at normal pace
- Use a quiet environment
- Position microphone close to your mouth
- Pause briefly before and after commands

### For Better Code Generation
- Be specific in your commands
- Use application names (e.g., "Chrome", "Notepad")
- Include actions (e.g., "click", "type", "open")
- Break complex tasks into simpler steps

### For Safe Execution
- Always review generated code first
- Test with simple commands initially
- Use the Save Code feature for reusable scripts
- Keep important work saved before running automation

## 🚀 Next Steps

Once you're comfortable with the basics:

1. **Explore Settings** - Customize recording and API parameters
2. **Save Useful Scripts** - Build a library of automation codes
3. **Chain Commands** - Combine multiple actions in one voice command
4. **Experiment** - Try different phrasings for the same task

## 📞 Support

Need help? Here's where to get assistance:

- 📖 **Documentation**: Check the full README.md
- 🐛 **Bug Reports**: GitHub Issues
- 💬 **Community**: GitHub Discussions
- 📧 **Email**: support@projectevee.com

---

**Ready to transform your voice into powerful automation? Let's get started! 🎙️✨** 