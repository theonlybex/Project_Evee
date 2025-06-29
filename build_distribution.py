#!/usr/bin/env python3
"""
Project Evee Distribution Builder
================================

This script builds a complete distribution package for Project Evee.
It creates both a wheel package and a portable installer.
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🏗️  PROJECT EVEE DISTRIBUTION BUILDER")
    print("=" * 60)
    print()

def clean_build_artifacts():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '*.egg-info', '__pycache__']
    
    for pattern in dirs_to_clean:
        if '*' in pattern:
            # Handle glob patterns
            import glob
            for path in glob.glob(pattern):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"   Removed directory: {path}")
        else:
            if os.path.exists(pattern):
                if os.path.isdir(pattern):
                    shutil.rmtree(pattern)
                    print(f"   Removed directory: {pattern}")
                else:
                    os.remove(pattern)
                    print(f"   Removed file: {pattern}")
    
    print("✅ Cleanup complete")

def build_wheel():
    """Build wheel distribution"""
    print("\n📦 Building wheel distribution...")
    
    try:
        # Install build dependencies
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "build", "wheel", "--quiet"
        ])
        
        # Build the package
        subprocess.check_call([
            sys.executable, "-m", "build"
        ])
        
        print("✅ Wheel distribution built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build wheel: {e}")
        return False

def create_portable_package():
    """Create portable installation package"""
    print("\n📁 Creating portable package...")
    
    try:
        # Create distribution directory
        dist_dir = Path("dist/project-evee-portable")
        dist_dir.mkdir(parents=True, exist_ok=True)
        
        # Files to include in portable package
        files_to_copy = [
            "main_gui.py",
            "base.py",
            "automation_code.py",
            "installer.py",
            "requirements.txt",
            "README.md",
            "LICENSE",
            "modules/"
        ]
        
        # Copy files
        for file_path in files_to_copy:
            src = Path(file_path)
            dst = dist_dir / file_path
            
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"   Copied: {file_path}")
            elif src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"   Copied: {file_path}/")
        
        # Create installation script for portable version
        install_script = dist_dir / "INSTALL.bat"
        install_content = """@echo off
echo Installing Project Evee...
echo.
python installer.py
echo.
echo Installation complete!
pause
"""
        with open(install_script, 'w') as f:
            f.write(install_content)
        
        # Create run script for development
        run_script = dist_dir / "RUN_DEV.bat"
        run_content = """@echo off
title Project Evee - Development Mode
python main_gui.py
pause
"""
        with open(run_script, 'w') as f:
            f.write(run_content)
        
        # Create ZIP archive
        zip_path = Path("dist/project-evee-portable.zip")
        print(f"   Creating ZIP archive: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dist_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(dist_dir.parent)
                    zipf.write(file_path, arcname)
        
        print("✅ Portable package created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create portable package: {e}")
        return False

def create_executable():
    """Create standalone executable using PyInstaller"""
    print("\n🔧 Creating standalone executable...")
    
    try:
        # Install PyInstaller
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"
        ])
        
        # Create executable
        subprocess.check_call([
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=ProjectEvee",
            "--icon=icon.ico" if os.path.exists("icon.ico") else "",
            "--add-data=modules;modules",
            "--add-data=requirements.txt;.",
            "main_gui.py"
        ])
        
        print("✅ Standalone executable created")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create executable: {e}")
        return False
    except FileNotFoundError:
        print("⚠️  PyInstaller not found, skipping executable creation")
        return True

def create_installer_exe():
    """Create Windows installer using NSIS (if available)"""
    print("\n📋 Creating Windows installer...")
    
    # Check if NSIS is available
    try:
        subprocess.check_output(["makensis", "/VERSION"], stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  NSIS not found, skipping installer creation")
        print("   Install NSIS from https://nsis.sourceforge.io/ to create Windows installer")
        return True
    
    # Create NSIS script
    nsis_script = """
!define APPNAME "Project Evee"
!define COMPANYNAME "Project Evee Team"
!define DESCRIPTION "Voice-Controlled Automation Assistant"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0

!define HELPURL "https://github.com/yourusername/project-evee"
!define UPDATEURL "https://github.com/yourusername/project-evee/releases"
!define ABOUTURL "https://github.com/yourusername/project-evee"

!define INSTALLSIZE 1048576  # 1GB estimated

RequestExecutionLevel admin

InstallDir "$PROGRAMFILES\\${APPNAME}"

Name "${APPNAME}"
Icon "icon.ico"
outFile "dist\\ProjectEveeInstaller.exe"

!include LogicLib.nsh

page components
page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    
    # Copy files
    file /r "dist\\project-evee-portable\\*"
    
    # Create shortcuts
    createShortCut "$SMPROGRAMS\\${APPNAME}.lnk" "$INSTDIR\\main_gui.py" "" "$INSTDIR\\icon.ico"
    createShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\main_gui.py" "" "$INSTDIR\\icon.ico"
    
    # Registry information for add/remove programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "UninstallString" "$\\"$INSTDIR\\uninstall.exe$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "QuietUninstallString" "$\\"$INSTDIR\\uninstall.exe$\" /S"
    
    writeUninstaller "$INSTDIR\\uninstall.exe"
sectionEnd

section "uninstall"
    delete "$SMPROGRAMS\\${APPNAME}.lnk"
    delete "$DESKTOP\\${APPNAME}.lnk"
    
    rmDir /r $INSTDIR
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}"
sectionEnd
"""
    
    # Write NSIS script
    with open("installer.nsi", "w") as f:
        f.write(nsis_script)
    
    try:
        subprocess.check_call(["makensis", "installer.nsi"])
        os.remove("installer.nsi")
        print("✅ Windows installer created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create installer: {e}")
        return False

def print_distribution_info():
    """Print information about created distributions"""
    print("\n" + "=" * 60)
    print("🎉 DISTRIBUTION BUILD COMPLETE!")
    print("=" * 60)
    
    dist_dir = Path("dist")
    if dist_dir.exists():
        print("\n📦 Created distributions:")
        for item in dist_dir.iterdir():
            size = ""
            if item.is_file():
                size_bytes = item.stat().st_size
                if size_bytes > 1024*1024:
                    size = f" ({size_bytes/(1024*1024):.1f} MB)"
                elif size_bytes > 1024:
                    size = f" ({size_bytes/1024:.1f} KB)"
                else:
                    size = f" ({size_bytes} bytes)"
            
            print(f"   📄 {item.name}{size}")
    
    print("\n🚀 Distribution is ready!")
    print("\nTo distribute Project Evee:")
    print("1. Share the portable ZIP file for easy installation")
    print("2. Use the wheel file for pip installation")
    print("3. Use the installer EXE for Windows users")
    print("=" * 60)

def main():
    print_banner()
    
    print("Building Project Evee distribution package...")
    print("This process will create multiple distribution formats.\n")
    
    # Clean previous builds
    clean_build_artifacts()
    
    # Build distributions
    success = True
    
    # Build wheel package
    if not build_wheel():
        success = False
    
    # Create portable package
    if not create_portable_package():
        success = False
    
    # Create executable (optional)
    create_executable()
    
    # Create Windows installer (optional)
    create_installer_exe()
    
    if success:
        print_distribution_info()
    else:
        print("\n❌ Some builds failed. Check the output above for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 