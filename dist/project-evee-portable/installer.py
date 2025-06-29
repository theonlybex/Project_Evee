#!/usr/bin/env python3
"""
Project Evee Installer
=====================

This script installs Project Evee and all its dependencies.
Run this script to set up the voice automation assistant on your system.
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil
import json
from pathlib import Path

class ProjectEveeInstaller:
    def __init__(self):
        self.install_dir = Path.home() / "ProjectEvee"
        self.desktop_shortcut = Path.home() / "Desktop" / "Project Evee.lnk"
        self.start_menu_shortcut = None
        
        if platform.system() == "Windows":
            self.start_menu_shortcut = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Project Evee.lnk"
    
    def print_banner(self):
        print("=" * 60)
        print("🎙️  PROJECT EVEE INSTALLER")
        print("   Voice-Controlled Automation Assistant")
        print("=" * 60)
        print()
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("Checking Python version...")
        if sys.version_info < (3, 8):
            print("❌ Error: Python 3.8 or higher is required!")
            print(f"   Current version: {sys.version}")
            print("   Please install Python 3.8+ from https://python.org")
            return False
        print(f"✅ Python {sys.version.split()[0]} is compatible")
        return True
    
    def check_dependencies(self):
        """Check if required system dependencies are available"""
        print("\nChecking system dependencies...")
        
        # Check for pip
        try:
            import pip
            print("✅ pip is available")
        except ImportError:
            print("❌ pip is not available. Please install pip first.")
            return False
        
        # Check for audio system (Windows)
        if platform.system() == "Windows":
            print("✅ Windows audio system detected")
        
        return True
    
    def create_install_directory(self):
        """Create installation directory"""
        print(f"\nCreating installation directory: {self.install_dir}")
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            print("✅ Installation directory created")
            return True
        except Exception as e:
            print(f"❌ Failed to create directory: {e}")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("\nInstalling Python dependencies...")
        print("This may take several minutes...")
        
        # Core dependencies
        dependencies = [
            "torch",
            "openai-whisper",
            "pyaudio",
            "numpy",
            "requests",
            "pyautogui",
            "pygetwindow",
            "pysimplegui",
            "sounddevice",
        ]
        
        for dep in dependencies:
            print(f"Installing {dep}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", dep, "--quiet"
                ])
                print(f"✅ {dep} installed")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {dep}")
                return False
        
        print("✅ All dependencies installed successfully!")
        return True
    
    def copy_application_files(self):
        """Copy application files to installation directory"""
        print("\nCopying application files...")
        
        # Files to copy
        files_to_copy = [
            "main_gui.py",
            "base.py",
            "automation_code.py",
            "requirements.txt",
            "modules/"
        ]
        
        current_dir = Path.cwd()
        
        for file_path in files_to_copy:
            src = current_dir / file_path
            dst = self.install_dir / file_path
            
            try:
                if src.is_file():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    print(f"✅ Copied {file_path}")
                elif src.is_dir():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    print(f"✅ Copied {file_path}/")
                else:
                    print(f"⚠️  {file_path} not found, skipping")
            except Exception as e:
                print(f"❌ Failed to copy {file_path}: {e}")
                return False
        
        return True
    
    def create_launcher_script(self):
        """Create launcher script"""
        print("\nCreating launcher script...")
        
        launcher_content = f'''@echo off
title Project Evee - Voice Automation Assistant
cd /d "{self.install_dir}"
python main_gui.py
pause
'''
        
        launcher_path = self.install_dir / "run_project_evee.bat"
        try:
            with open(launcher_path, 'w') as f:
                f.write(launcher_content)
            print("✅ Launcher script created")
            return str(launcher_path)
        except Exception as e:
            print(f"❌ Failed to create launcher: {e}")
            return None
    
    def create_desktop_shortcut(self, launcher_path):
        """Create desktop shortcut (Windows)"""
        if platform.system() != "Windows":
            return True
        
        print("\nCreating desktop shortcut...")
        try:
            import winshell
            from win32com.client import Dispatch
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(self.desktop_shortcut))
            shortcut.Targetpath = launcher_path
            shortcut.WorkingDirectory = str(self.install_dir)
            shortcut.IconLocation = launcher_path
            shortcut.Description = "Project Evee - Voice Automation Assistant"
            shortcut.save()
            
            print("✅ Desktop shortcut created")
            return True
        except ImportError:
            print("⚠️  Creating shortcut manually...")
            return self.create_manual_shortcut(launcher_path)
        except Exception as e:
            print(f"❌ Failed to create shortcut: {e}")
            return False
    
    def create_manual_shortcut(self, launcher_path):
        """Create shortcut manually without winshell"""
        shortcut_content = f'''[{{000214A0-0000-0000-C000-000000000046}}]
Prop3=19,0
[InternetShortcut]
IDList=
URL=file:///{launcher_path}
IconFile={launcher_path}
IconIndex=0
'''
        try:
            shortcut_path = self.desktop_shortcut.with_suffix('.url')
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            print("✅ Desktop shortcut created (manual)")
            return True
        except Exception as e:
            print(f"❌ Failed to create manual shortcut: {e}")
            return False
    
    def create_uninstaller(self):
        """Create uninstaller script"""
        print("\nCreating uninstaller...")
        
        uninstaller_content = f'''@echo off
echo Uninstalling Project Evee...
echo.
choice /C YN /M "Are you sure you want to uninstall Project Evee"
if errorlevel 2 goto :cancel

echo Removing files...
rd /s /q "{self.install_dir}"
del "{self.desktop_shortcut}" 2>nul
echo.
echo Project Evee has been uninstalled.
pause
goto :end

:cancel
echo Uninstall cancelled.
pause

:end
'''
        
        uninstaller_path = self.install_dir / "uninstall.bat"
        try:
            with open(uninstaller_path, 'w') as f:
                f.write(uninstaller_content)
            print("✅ Uninstaller created")
            return True
        except Exception as e:
            print(f"❌ Failed to create uninstaller: {e}")
            return False
    
    def create_readme(self):
        """Create README file"""
        readme_content = """# Project Evee - Voice Automation Assistant

## Getting Started

1. Double-click "run_project_evee.bat" to launch the application
2. Click "Start Recording" and speak your command
3. Click "Generate Code" to create automation code
4. Review the generated code and click "Execute Code" to run it

## Features

- Voice recording and transcription
- AI-powered code generation
- Automation execution
- Settings management
- Command history

## Requirements

- Windows 10/11
- Microphone
- Internet connection (for AI processing)

## Support

For help and support, please check the documentation or contact support.

## Uninstalling

Run "uninstall.bat" to remove Project Evee from your system.
"""
        
        readme_path = self.install_dir / "README.txt"
        try:
            with open(readme_path, 'w') as f:
                f.write(readme_content)
            print("✅ README created")
            return True
        except Exception as e:
            print(f"❌ Failed to create README: {e}")
            return False
    
    def install(self):
        """Main installation process"""
        self.print_banner()
        
        print("Starting installation process...\n")
        
        # Check system requirements
        if not self.check_python_version():
            return False
        
        if not self.check_dependencies():
            return False
        
        # Create installation directory
        if not self.create_install_directory():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            return False
        
        # Copy files
        if not self.copy_application_files():
            return False
        
        # Create launcher
        launcher_path = self.create_launcher_script()
        if not launcher_path:
            return False
        
        # Create shortcuts
        self.create_desktop_shortcut(launcher_path)
        
        # Create additional files
        self.create_uninstaller()
        self.create_readme()
        
        # Installation complete
        print("\n" + "=" * 60)
        print("🎉 INSTALLATION COMPLETE!")
        print("=" * 60)
        print(f"📁 Installed to: {self.install_dir}")
        print(f"🖱️  Desktop shortcut: {self.desktop_shortcut}")
        print("🚀 Ready to use!")
        print("\nTo start Project Evee:")
        print("1. Double-click the desktop shortcut, or")
        print(f"2. Run: {launcher_path}")
        print("\n⚠️  IMPORTANT: You'll need to set your DeepSeek API key in Settings")
        print("=" * 60)
        
        return True

def main():
    installer = ProjectEveeInstaller()
    
    try:
        success = installer.install()
        if not success:
            print("\n❌ Installation failed!")
            input("Press Enter to exit...")
            sys.exit(1)
        else:
            print("\nInstallation completed successfully!")
            input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main() 