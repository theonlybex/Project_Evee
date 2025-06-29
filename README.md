# 🎙️ Project Evee - Voice Automation Assistant

Project Evee is a powerful voice-controlled automation assistant that transforms your spoken commands into executable automation code. Simply speak what you want to do, and let AI generate and execute the automation for you!

## ✨ Features

- 🎤 **Voice Recording**: Smart voice detection with automatic silence cutoff
- 🧠 **AI Transcription**: Uses OpenAI Whisper for accurate speech-to-text
- 🤖 **Code Generation**: DeepSeek AI generates Python automation code
- 🖥️ **Modern GUI**: Clean, intuitive interface with tabbed layout
- ⚙️ **Configurable Settings**: Customize API keys and recording parameters
- 📊 **History Tracking**: Keep track of all your commands and executions
- 💾 **Code Management**: Save, edit, and reuse generated automation scripts

## 🚀 Quick Start

### Option 1: Easy Installation (Recommended)

1. **Download the installer**: Get `installer.py` from the releases
2. **Run the installer**: Double-click `installer.py` or run:
   ```bash
   python installer.py
   ```
3. **Follow the installation wizard**: The installer will:
   - Check system requirements
   - Install all dependencies
   - Set up the application
   - Create desktop shortcuts

4. **Launch Project Evee**: Use the desktop shortcut or run `run_project_evee.bat`

### Option 2: Manual Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/project-evee.git
   cd project-evee
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main_gui.py
   ```

## 🛠️ System Requirements

- **Operating System**: Windows 10/11 (primary), Linux/macOS (experimental)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for models and dependencies
- **Audio**: Working microphone
- **Internet**: Required for AI processing

## 📖 How to Use

1. **First Launch**:
   - Open Settings (⚙️ button)
   - Enter your DeepSeek API key
   - Adjust recording settings if needed

2. **Voice Commands**:
   - Click "🎤 Start Recording"
   - Speak your command clearly
   - Recording stops automatically after silence

3. **Generate Code**:
   - Click "🤖 Generate Code" after recording
   - Review the generated automation code
   - Make manual edits if needed

4. **Execute Automation**:
   - Click "▶️ Execute Code" to run the automation
   - Confirm the execution when prompted
   - Monitor the results

## 💡 Example Commands

Try these voice commands to get started:

- "Open YouTube and search for funny cat videos"
- "Take a screenshot and save it to desktop"
- "Open calculator and compute 25 times 17"
- "Send an email to john@example.com with subject 'Meeting Tomorrow'"
- "Create a new Word document and type 'Hello World'"
- "Open Chrome and navigate to google.com"

## 🔧 Configuration

### API Setup

You'll need a DeepSeek API key:

1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create an account and generate an API key
3. In Project Evee, go to Settings and enter your API key

### Recording Settings

- **Silence Timeout**: How long to wait before stopping recording (default: 4 seconds)
- **Audio Quality**: Adjust sample rate and channels if needed

## 📁 Project Structure

```
Project_Evee/
├── main_gui.py              # Main GUI application
├── base.py                  # Original command-line version
├── installer.py             # Installation script
├── setup.py                 # Package setup configuration
├── requirements.txt         # Python dependencies
├── modules/
│   ├── voice_input.py       # Audio recording functionality
│   ├── deepseek_api_engine.py # AI code generation
│   ├── deepseek_engine.py   # Alternative engine
│   ├── openai_engine.py     # OpenAI integration
│   └── engine.py            # Base engine class
├── automation_code.py       # Generated automation scripts
├── audiototext.txt          # Transcription storage
├── recording.wav            # Audio recordings
└── settings.json            # User settings
```

## 🔒 Security & Privacy

- **Local Processing**: Voice transcription happens locally using Whisper
- **API Communication**: Only transcribed text is sent to DeepSeek API
- **No Data Storage**: Your voice recordings are not stored permanently
- **Code Review**: Always review generated code before execution
- **Safe Execution**: Confirmation prompts before running automation

## 🛠️ Development

### Building from Source

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install build wheel setuptools
   ```

3. Build the package:
   ```bash
   python -m build
   ```

### Creating Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="ProjectEvee" main_gui.py
```

## 🚨 Troubleshooting

### Common Issues

**"No module named 'modules'"**
- Ensure you're running from the project root directory
- Check that the `modules/` folder exists

**"Recording failed"**
- Check microphone permissions
- Verify audio device is working
- Try adjusting recording settings

**"API Error"**
- Verify your DeepSeek API key is correct
- Check internet connection
- Ensure API key has sufficient credits

**"Execution failed"**
- Review the generated code for errors
- Check if required applications are installed
- Try running code manually first

### Getting Help

1. Check the [Issues](https://github.com/yourusername/project-evee/issues) page
2. Review the troubleshooting guide
3. Join our community discussions
4. Contact support

## 📋 Dependencies

Core dependencies include:

- `torch` - PyTorch for deep learning
- `openai-whisper` - Speech recognition
- `pyaudio` - Audio recording
- `requests` - HTTP requests for API
- `pyautogui` - GUI automation
- `tkinter` - GUI framework (built-in)
- `numpy` - Numerical computing

See `requirements.txt` for the complete list.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code style and standards
- Submitting pull requests
- Reporting bugs
- Suggesting enhancements

## 🙏 Acknowledgments

- **OpenAI Whisper** for excellent speech recognition
- **DeepSeek** for powerful code generation AI
- **Python Community** for amazing libraries and tools
- **Contributors** who help improve Project Evee

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/project-evee/wiki)
- **Bug Reports**: [Issues](https://github.com/yourusername/project-evee/issues)
- **Feature Requests**: [Discussions](https://github.com/yourusername/project-evee/discussions)
- **Email**: support@projectevee.com

---

**Made with ❤️ by the Project Evee Team**

*Transform your voice into powerful automation!* 