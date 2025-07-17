# 🚀 Project Evee - Quick Start Guide

Project Evee now comes in **TWO versions**! Choose the one that fits your needs:

## 🖥️ **Version 1: DeepSeek GUI App** (Default)
**Windows GUI application with DeepSeek AI for code generation**

### How to Run:
```bash
# Option 1: Use the bat file (recommended)
double-click: run_project_evee.bat

# Option 2: Run directly
python base.py
```

### Features:
- 🎨 **Full Windows GUI** with conversation bubbles and animations
- 🧠 **DeepSeek AI Engine** for intelligent code generation
- 🎤 **Voice input** with Whisper transcription
- 💾 **Manual controls** - Generate, Execute, Save buttons
- ⚙️ **Settings dialog** for API configuration

---

## 💻 **Version 2: Terminal Browser Automation** (New)
**Command-line interface with browser automation**

### How to Run:
```bash
python main_gui.py
```

### Features:
- 🔧 **Terminal-based** - fast and lightweight
- 🌐 **Browser automation** using browser-use engine
- 🤖 **OpenAI GPT-4o-mini** for smart web interactions
- ⚡ **Command-driven** - simple text commands
- 🎯 **Direct execution** - voice → browser actions

---

## 🔧 **Quick Setup**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys:**
   - For DeepSeek version: Add `DEEPSEEK_API_KEY` to `.env`
   - For Browser version: Add `OPENAI_API_KEY` to `.env`

3. **Run your preferred version!**

---

## 🎯 **Which Version Should I Use?**

| Feature | DeepSeek GUI | Terminal Browser |
|---------|--------------|------------------|
| **Interface** | Windows GUI | Terminal |
| **AI Engine** | DeepSeek | OpenAI GPT-4o-mini |
| **Best For** | Code generation | Web automation |
| **Speed** | Moderate | Fast |
| **Visual** | Yes | No |
| **Browser Control** | No | Yes |

---

## 🆘 **Need Help?**

- Check `README.md` for detailed documentation
- Both versions use the same voice input system
- API keys required for full functionality 