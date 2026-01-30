#!/usr/bin/env python3
"""
Build script to create standalone executable from GUI application.
"""

import os
import sys
import subprocess
from pathlib import Path


def install_pyinstaller():
    """Install PyInstaller if not available."""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller installed")


def build_executable():
    """Build standalone executable."""
    script_dir = Path(__file__).parent
    gui_script = script_dir / "pdf_to_jira_gui.py"
    
    if not gui_script.exists():
        print(f"❌ GUI script not found: {gui_script}")
        return False
    
    print("\n" + "="*70)
    print("Building Standalone Executable")
    print("="*70 + "\n")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=PDF_to_Jira",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (GUI only)
        "--clean",
        str(gui_script)
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd, cwd=str(script_dir), check=True)
        
        print("\n" + "="*70)
        print("✅ Build Complete!")
        print("="*70)
        
        # Find the executable
        dist_dir = script_dir / "dist"
        if sys.platform == "darwin":
            exe_name = "PDF_to_Jira"
        elif sys.platform == "win32":
            exe_name = "PDF_to_Jira.exe"
        else:
            exe_name = "PDF_to_Jira"
        
        exe_path = dist_dir / exe_name
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n📦 Executable created:")
            print(f"   Location: {exe_path}")
            print(f"   Size: {size_mb:.1f} MB")
            print(f"\n🚀 You can now distribute this file!")
            print(f"   Just double-click to run the application.")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False


def main():
    """Main build process."""
    print("PDF to Jira - Executable Builder")
    print("-" * 70)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher required")
        return 1
    
    print(f"✓ Python {sys.version.split()[0]}")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    if build_executable():
        print("\n✅ Success! Your standalone application is ready.")
        return 0
    else:
        print("\n❌ Build failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
