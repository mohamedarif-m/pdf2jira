# Building Standalone Executable

This guide explains how to create a standalone executable application that can run without Python installed.

## Quick Build

### Option 1: Automated Build Script

```bash
cd requirements
python3 build_executable.py
```

This will:
1. Install PyInstaller if needed
2. Build the executable
3. Create `dist/PDF_to_Jira` (or `.exe` on Windows)

### Option 2: Manual PyInstaller

```bash
cd requirements

# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --name=PDF_to_Jira --onefile --windowed pdf_to_jira_gui.py
```

## What You Get

After building, you'll have:

```
requirements/
├── dist/
│   └── PDF_to_Jira          # ← Standalone executable
├── build/                    # Build artifacts (can delete)
└── PDF_to_Jira.spec         # Build specification
```

## Running the Executable

**macOS/Linux:**
```bash
cd dist
./PDF_to_Jira
```

**Windows:**
```
Double-click PDF_to_Jira.exe
```

## Distribution

The executable in `dist/` folder:
- ✅ Can run on any computer (same OS)
- ✅ No Python installation needed
- ✅ All dependencies included
- ✅ Can be distributed as single file

**File sizes:**
- macOS: ~15-20 MB
- Windows: ~10-15 MB
- Linux: ~12-18 MB

## Advanced Build Options

### Add Custom Icon

```bash
# macOS/Linux
pyinstaller --name=PDF_to_Jira --onefile --windowed --icon=icon.icns pdf_to_jira_gui.py

# Windows
pyinstaller --name=PDF_to_Jira --onefile --windowed --icon=icon.ico pdf_to_jira_gui.py
```

### Include Additional Files

Create a `PDF_to_Jira.spec` file:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pdf_to_jira_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),  # Include config file
        ('README.md', '.'),    # Include readme
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF_to_Jira',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Then build:
```bash
pyinstaller PDF_to_Jira.spec
```

### Optimize Size

```bash
# Use UPX compression
pyinstaller --name=PDF_to_Jira --onefile --windowed --upx-dir=/path/to/upx pdf_to_jira_gui.py

# Exclude unused modules
pyinstaller --name=PDF_to_Jira --onefile --windowed \
  --exclude-module matplotlib \
  --exclude-module numpy \
  pdf_to_jira_gui.py
```

## Platform-Specific Notes

### macOS

**Code Signing (for distribution):**
```bash
# Sign the app
codesign --force --sign "Developer ID Application: Your Name" dist/PDF_to_Jira

# Verify signature
codesign --verify --verbose dist/PDF_to_Jira
```

**Create DMG for distribution:**
```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "PDF to Jira" \
  --window-size 500 300 \
  --app-drop-link 350 120 \
  "PDF_to_Jira.dmg" \
  "dist/"
```

### Windows

**Create Installer:**

Use Inno Setup or NSIS to create a proper Windows installer.

Example Inno Setup script (`setup.iss`):

```ini
[Setup]
AppName=PDF to Jira
AppVersion=1.0
DefaultDirName={pf}\PDF to Jira
DefaultGroupName=PDF to Jira
OutputBaseFilename=PDF_to_Jira_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\PDF_to_Jira.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\PDF to Jira"; Filename: "{app}\PDF_to_Jira.exe"
```

### Linux

**Create AppImage:**
```bash
# Install appimagetool
wget "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
mkdir -p PDF_to_Jira.AppDir/usr/bin
cp dist/PDF_to_Jira PDF_to_Jira.AppDir/usr/bin/

# Create AppImage
./appimagetool-x86_64.AppImage PDF_to_Jira.AppDir
```

## Troubleshooting

### "Module not found" errors

Add missing imports to spec file:
```python
hiddenimports=['pkg_resources.py2_warn', 'requests', 'PyPDF2']
```

### Large file size

Exclude unnecessary modules:
```bash
--exclude-module matplotlib --exclude-module PIL
```

### GUI doesn't show

Make sure to use `--windowed` flag.

### macOS Gatekeeper blocks app

```bash
# Remove quarantine flag
xattr -d com.apple.quarantine dist/PDF_to_Jira
```

Or right-click and select "Open" instead of double-clicking.

## Testing

Before distribution:

1. **Test on clean machine** without Python installed
2. **Test all features** in the GUI
3. **Check file paths** - use relative paths
4. **Test error handling** - simulate failures
5. **Check different OS versions**

## Distribution Checklist

- [ ] Test executable on target OS
- [ ] Include README/documentation
- [ ] Add license file if applicable
- [ ] Create release notes
- [ ] Sign code (macOS/Windows)
- [ ] Test installation process
- [ ] Verify no hardcoded paths
- [ ] Check file permissions

## File Structure for Distribution

```
PDF_to_Jira_v1.0/
├── PDF_to_Jira[.exe]       # Executable
├── README.md               # User guide
├── LICENSE.txt             # License
├── CHANGELOG.md            # Version history
└── sample_config.json      # Sample configuration
```

## Versioning

Update version in your code:

```python
__version__ = "1.0.0"
```

And in PyInstaller command:
```bash
pyinstaller --name="PDF to Jira v1.0" --onefile --windowed pdf_to_jira_gui.py
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build Executable

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install pyinstaller PyPDF2 requests
    
    - name: Build executable
      run: |
        pyinstaller --name=PDF_to_Jira --onefile --windowed pdf_to_jira_gui.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: PDF_to_Jira-${{ matrix.os }}
        path: dist/
```

## Support

For issues building the executable:
- Check PyInstaller docs: https://pyinstaller.org/
- Verify Python version compatibility
- Check console output for errors
- Test on clean Python environment
