#!/usr/bin/env python3
"""
Project Evee - Installation Verification Script
This script checks if all required dependencies are properly installed.
"""

import sys
import platform
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_dependencies():
    """Check if all required dependencies can be imported"""
    print("\n📦 Checking dependencies...")
    
    dependencies = [
        ("tkinter", "GUI Framework"),
        ("whisper", "Speech-to-Text"),
        ("pyaudio", "Audio Recording"),
        ("requests", "HTTP Requests"),
        ("numpy", "Numerical Computing"),
        ("torch", "PyTorch ML Framework"),
        ("transformers", "Hugging Face Transformers"),
        ("openai", "OpenAI API"),
        ("selenium", "Web Automation"),
        ("pyautogui", "Desktop Automation"),
        ("pywinauto", "Windows Automation"),
        ("browser_use", "Browser Automation"),
        ("modules.file_manager", "File Manager")
    ]
    
    failed_imports = []
    
    for package, description in dependencies:
        try:
            if package == "pyautogui":
                import pyautogui
            elif package == "pywinauto":
                import pywinauto
            elif package == "browser_use":
                import browser_use
            elif package == "modules.file_manager":
                from modules.file_manager import get_file_manager
                # Test file manager functionality
                fm = get_file_manager()
                status = fm.validate_file_integrity()
                if not all(status.values()):
                    raise Exception(f"File integrity check failed: {status}")
            else:
                __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError as e:
            print(f"❌ {package} - {description} (MISSING)")
            failed_imports.append(package)
        except Exception as e:
            print(f"⚠️  {package} - {description} (ERROR: {e})")
            failed_imports.append(package)
    
    return failed_imports

def check_audio_devices():
    """Check if audio devices are available"""
    print("\n🎤 Checking audio devices...")
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        print(f"✅ Found {device_count} audio devices")
        
        # Check for input devices
        input_devices = []
        for i in range(device_count):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
        
        if input_devices:
            print(f"✅ Input devices available: {len(input_devices)}")
        else:
            print("⚠️  No input audio devices found")
        
        p.terminate()
        return True
    except Exception as e:
        print(f"❌ Audio device check failed: {e}")
        return False

def check_system_requirements():
    """Check system-specific requirements"""
    print("\n💻 Checking system requirements...")
    
    system = platform.system()
    print(f"✅ Operating System: {system} {platform.release()}")
    
    if system == "Windows":
        print("✅ Windows detected - pywinauto should work")
    else:
        print("⚠️  Non-Windows system - pywinauto may not work properly")
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        print(f"✅ Available RAM: {memory_gb:.1f} GB")
        
        if memory_gb < 4:
            print("⚠️  Less than 4GB RAM - AI models may run slowly")
    except:
        print("⚠️  Could not check system memory")

def main():
    """Main verification function"""
    print("=" * 50)
    print("🚀 Project Evee - Installation Verification")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Check dependencies
    failed_imports = check_dependencies()
    if failed_imports:
        success = False
        print(f"\n❌ {len(failed_imports)} dependencies missing:")
        for package in failed_imports:
            print(f"   - {package}")
        print("\nTo install missing packages, run:")
        print("pip install -r requirements.txt")
    
    # Check audio
    if not check_audio_devices():
        print("\n⚠️  Audio issues detected. You may need to:")
        print("   - Install audio drivers")
        print("   - Use 'pipwin install pyaudio' on Windows")
    
    # Check system requirements
    check_system_requirements()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All checks passed! Project Evee should work properly.")
    else:
        print("⚠️  Some issues detected. Please fix them before running Project Evee.")
    print("=" * 50)
    
    return success

if __name__ == "__main__":
    main() 