# 🚀 Project Evee - Cross-Platform Installation Guide

This guide ensures Project Evee works consistently across different devices and operating systems.

## 📋 Prerequisites

### Minimum Requirements
- **Python 3.8+** (Recommended: Python 3.10-3.12)
- **4GB RAM** (8GB+ recommended for better AI model performance)
- **2GB free disk space**
- **Microphone** (for voice input)
- **Internet connection** (for AI API calls)

### Operating System Support
- ✅ **Windows 10/11** (Fully supported)
- ⚠️ **macOS** (Limited - pywinauto won't work)
- ⚠️ **Linux** (Limited - pywinauto won't work)

## 🛠️ Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Project_Evee.git
cd Project_Evee
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv evee_env
evee_env\Scripts\activate

# macOS/Linux
python3 -m venv evee_env
source evee_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Platform-Specific Setup

#### Windows Additional Steps
```bash
# If PyAudio installation fails:
pip install pipwin
pipwin install pyaudio

# Install Visual C++ Redistributable if needed
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

#### macOS Additional Steps
```bash
# Install portaudio for PyAudio
brew install portaudio
pip install pyaudio

# Install FFmpeg
brew install ffmpeg
```

#### Linux Additional Steps
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev python3-pip portaudio19-dev ffmpeg

# CentOS/RHEL
sudo yum install python3-devel portaudio-devel ffmpeg

# Install PyAudio
pip install pyaudio
```

### 5. Verify Installation
```bash
python verify_installation.py
```

This script will check:
- ✅ Python version compatibility
- ✅ All required dependencies
- ✅ Audio device availability
- ✅ System requirements

## 🔧 Configuration

### 1. Set Up API Keys
Run the application and click **"⚙️ Settings"** to configure:
- **DeepSeek API Key** (for AI code generation)
- **OpenAI API Key** (optional, for alternative AI engine)

### 2. Audio Configuration
If you encounter audio issues:
```bash
# Test audio devices
python -c "import pyaudio; p=pyaudio.PyAudio(); print('Devices:', p.get_device_count()); p.terminate()"

# Windows: Try different audio drivers
# macOS: Check System Preferences > Security > Microphone
# Linux: Check ALSA/PulseAudio configuration
```

## 🚀 Running Project Evee

### Method 1: GUI Application (Recommended)
```bash
python base.py
```

### Method 2: Command Line Interface
```bash
python main_gui.py
```

### Method 3: Windows Batch File
```batch
run_project_evee.bat
```

## 🧪 Testing the Installation

### 1. Basic Test
```bash
python verify_installation.py
```

### 2. Voice Recording Test
1. Run `python base.py`
2. Click "🎤 Start Recording"
3. Speak a simple command like "open notepad"
4. Check if transcription appears

### 3. AI Engine Test
```bash
python test_browser_engine.py
```

## 🛠️ Troubleshooting

### Common Issues

#### PyAudio Installation Failed
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# Or download wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

#### Whisper Model Download Issues
```bash
# Pre-download Whisper model
python -c "import whisper; whisper.load_model('base')"
```

#### Permission Errors (Windows)
- Run Command Prompt as Administrator
- Check Windows Defender exclusions
- Verify microphone permissions

#### Import Errors
```bash
# Reinstall problematic packages
pip uninstall package_name
pip install package_name

# Check Python path
python -c "import sys; print(sys.path)"
```

#### Audio Device Not Found
- **Windows**: Check Device Manager > Audio inputs
- **macOS**: System Preferences > Security & Privacy > Microphone
- **Linux**: `alsamixer` or check PulseAudio

### Performance Issues

#### Slow AI Model Loading
- Ensure 4GB+ RAM available
- Use SSD storage if possible
- Close unnecessary applications

#### High CPU Usage
- Use smaller Whisper model: `whisper.load_model("tiny")`
- Reduce audio quality in recording settings

## 📝 Development Setup

### For Contributors
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python -m pytest tests/

# Code formatting
black *.py modules/*.py
```

### Building Portable Distribution
```bash
python build_distribution.py
```

## 🔒 Security Notes

- **API Keys**: Never commit API keys to version control
- **Network**: Application makes HTTPS requests to AI services
- **Permissions**: Requires microphone and automation permissions
- **Antivirus**: May flag automation features - add exclusions if needed

## 📞 Support

### Getting Help
1. Check this installation guide
2. Run `python verify_installation.py`
3. Check [GitHub Issues](https://github.com/your-username/Project_Evee/issues)
4. Review logs in the application

### Reporting Issues
When reporting bugs, include:
- Operating system and version
- Python version (`python --version`)
- Full error message
- Output of `python verify_installation.py`

## 📄 Environment Variables (Optional)

Create a `.env` file in the project root:
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
WHISPER_MODEL=base
AUDIO_TIMEOUT=4
```

---

**Happy Automating! 🎉** 