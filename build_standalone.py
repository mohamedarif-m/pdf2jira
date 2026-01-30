#!/usr/bin/env python3
"""
Build Standalone Executable for PDF to Jira Importer
Creates a single executable file that includes Python and all dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("⚠ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def build_gui_executable():
    """Build GUI executable."""
    print("\n" + "="*70)
    print(" Building GUI Executable")
    print("="*70)
    
    system = platform.system()
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed" if system == "Darwin" or system == "Windows" else "--console",  # No console on Mac/Windows
        "--name=PDF-to-Jira-Importer",
        "--icon=NONE",  # Add icon path if you have one
        "--clean",
        "--noconfirm",
    ]
    
    # Add data files
    cmd.extend([
        "--add-data=pdf_to_jira_gui.py:.",
        "--hidden-import=tkinter",
        "--hidden-import=PyPDF2",
        "--hidden-import=requests",
    ])
    
    # Main script
    cmd.append("pdf_to_jira_gui.py")
    
    print(f"\n📦 Building for {system}...")
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✓ Build successful!")
        
        # Find the executable
        if system == "Windows":
            exe_path = Path("dist/PDF-to-Jira-Importer.exe")
        elif system == "Darwin":
            exe_path = Path("dist/PDF-to-Jira-Importer.app")
        else:
            exe_path = Path("dist/PDF-to-Jira-Importer")
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n🎉 Executable created: {exe_path}")
            print(f"   Size: {size_mb:.1f} MB")
            return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def build_cli_executable():
    """Build CLI executable."""
    print("\n" + "="*70)
    print(" Building CLI Executable")
    print("="*70)
    
    system = platform.system()
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=pdf-to-jira-cli",
        "--clean",
        "--noconfirm",
        "--hidden-import=PyPDF2",
        "--hidden-import=requests",
        "pdf_to_jira_advanced.py"
    ]
    
    print(f"\n📦 Building CLI for {system}...")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ CLI build successful!")
        return True
    except Exception as e:
        print(f"\n❌ CLI build failed: {e}")
        return False

def create_distribution_package():
    """Create a distribution package with executable and documentation."""
    print("\n" + "="*70)
    print(" Creating Distribution Package")
    print("="*70)
    
    dist_dir = Path("PDF-to-Jira-Distribution")
    dist_dir.mkdir(exist_ok=True)
    
    # Copy executable
    system = platform.system()
    if system == "Windows":
        exe_name = "PDF-to-Jira-Importer.exe"
    elif system == "Darwin":
        exe_name = "PDF-to-Jira-Importer.app"
    else:
        exe_name = "PDF-to-Jira-Importer"
    
    source = Path(f"dist/{exe_name}")
    if source.exists():
        import shutil
        if source.is_dir():
            shutil.copytree(source, dist_dir / exe_name, dirs_exist_ok=True)
        else:
            shutil.copy2(source, dist_dir / exe_name)
    
    # Create sample config
    sample_config = {
        "jira": {
            "url": "https://your-domain.atlassian.net",
            "email": "your-email@example.com",
            "api_token": "YOUR_API_TOKEN_HERE",
            "project_key": "PROJ"
        }
    }
    
    import json
    with open(dist_dir / "config-sample.json", "w") as f:
        json.dump(sample_config, f, indent=2)
    
    # Create README
    readme = """# PDF to Jira Importer - Distribution Package

## Quick Start

### Windows
1. Double-click `PDF-to-Jira-Importer.exe`
2. Click "Browse" to select a PDF file
3. Enter your Jira credentials
4. Click "Create Tasks"

### macOS
1. Double-click `PDF-to-Jira-Importer.app`
   (If blocked by security, go to System Preferences > Security & Privacy and click "Open Anyway")
2. Click "Browse" to select a PDF file
3. Enter your Jira credentials
4. Click "Create Tasks"

### Linux
1. Open terminal in this folder
2. Run: `./PDF-to-Jira-Importer`
3. Use the GUI to import PDF to Jira

## Getting Jira API Token

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy the token and paste it in the application

## Finding Project Key

1. Go to your Jira project
2. Look at the URL: https://your-domain.atlassian.net/browse/PROJ-123
3. The project key is "PROJ" (the part before the dash)

## Support

For issues or questions, refer to the documentation or contact your administrator.

## System Requirements

- No Python installation required
- Internet connection for Jira API
- Supported OS: Windows 10+, macOS 10.13+, Linux

## Version

Built on: """ + str(subprocess.run(["date"], capture_output=True, text=True).stdout.strip()) + """
Python: """ + sys.version.split()[0] + """
"""
    
    with open(dist_dir / "README.txt", "w") as f:
        f.write(readme)
    
    print(f"\n✓ Distribution package created in: {dist_dir}")
    print(f"\n📦 Package contents:")
    for item in dist_dir.iterdir():
        print(f"   • {item.name}")
    
    return dist_dir

def main():
    """Main build process."""
    print("="*70)
    print(" PDF to Jira - Standalone Executable Builder")
    print("="*70)
    print(f"\nSystem: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version.split()[0]}")
    
    # Check dependencies
    if not check_pyinstaller():
        return 1
    
    # Build options
    print("\n📋 Build Options:")
    print("1. GUI Executable (Recommended)")
    print("2. CLI Executable")
    print("3. Both")
    
    choice = input("\nSelect (1-3, default: 1): ").strip() or "1"
    
    success = True
    
    if choice in ["1", "3"]:
        if not build_gui_executable():
            success = False
    
    if choice in ["2", "3"]:
        if not build_cli_executable():
            success = False
    
    if success:
        # Create distribution package
        dist_dir = create_distribution_package()
        
        print("\n" + "="*70)
        print(" ✅ BUILD COMPLETE")
        print("="*70)
        print(f"\n📦 Distribution ready: {dist_dir}")
        print("\nTo share with others:")
        print(f"  1. Zip the '{dist_dir}' folder")
        print(f"  2. Share the zip file")
        print(f"  3. Recipients can extract and run the executable")
        print("\n⚠️  Note: Build on each target platform (Windows/Mac/Linux)")
        
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
