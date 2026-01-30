# Distribution Guide - PDF to Jira Importer

## Creating Standalone Executables

### Quick Build (Automated)

```bash
cd requirements
python3 build_standalone.py
```

This will:
- Install PyInstaller if needed
- Build a standalone executable
- Create a distribution package
- No Python required on target machines

### Manual Build

#### 1. Install PyInstaller

```bash
pip install pyinstaller
```

#### 2. Build GUI Executable

**macOS:**
```bash
pyinstaller --onefile --windowed --name PDF-to-Jira \
  --hidden-import=PyPDF2 --hidden-import=requests \
  pdf_to_jira_gui.py
```

**Windows:**
```bash
pyinstaller --onefile --windowed --name PDF-to-Jira ^
  --hidden-import=PyPDF2 --hidden-import=requests ^
  pdf_to_jira_gui.py
```

**Linux:**
```bash
pyinstaller --onefile --console --name PDF-to-Jira \
  --hidden-import=PyPDF2 --hidden-import=requests \
  pdf_to_jira_gui.py
```

#### 3. Build CLI Executable (Optional)

```bash
pyinstaller --onefile --console --name pdf-to-jira-cli \
  pdf_to_jira_advanced.py
```

### Output

- **macOS**: `dist/PDF-to-Jira.app` (~40-50 MB)
- **Windows**: `dist/PDF-to-Jira.exe` (~15-20 MB)
- **Linux**: `dist/PDF-to-Jira` (~20-30 MB)

## Distribution Options

### Option 1: Direct Executable (Single Platform)

1. Build on target platform
2. Share the executable from `dist/` folder
3. Recipients double-click to run

**Pros:**
- Simplest for users
- No installation needed

**Cons:**
- Must build separately for each OS
- Large file size

### Option 2: Python Scripts (All Platforms)

1. Zip the requirements folder
2. Share with instructions to install Python + dependencies

**Pros:**
- Works on all platforms
- Smaller file size
- Easier to update

**Cons:**
- Requires Python installation
- Users must run `pip install`

### Option 3: Docker Container (Advanced)

```bash
docker build -t pdf-to-jira .
docker run -v $(pwd):/data pdf-to-jira
```

**Pros:**
- Consistent environment
- No local dependencies

**Cons:**
- Requires Docker
- More complex for non-technical users

## Recommended Distribution Package

Create a folder with:

```
PDF-to-Jira-Distribution/
├── PDF-to-Jira.exe (or .app or Linux binary)
├── README.txt
├── config-sample.json
└── LICENSE.txt (if applicable)
```

### README.txt Example

```
PDF to Jira Importer
====================

Quick Start:
1. Double-click the executable
2. Browse to select your PDF file
3. Enter Jira credentials:
   - URL: https://your-company.atlassian.net
   - Email: your-email@company.com
   - API Token: Get from https://id.atlassian.com/manage-profile/security/api-tokens
   - Project Key: Your project identifier (e.g., PROJ)
4. Click "Create Tasks"

No Python or other software installation required!

System Requirements:
- Windows 10+, macOS 10.13+, or Linux
- Internet connection
- Jira account with API access

Support: contact@your-company.com
```

## Building for Multiple Platforms

### Using GitHub Actions (Automated)

Create `.github/workflows/build.yml`:

```yaml
name: Build Executables

on: [push, release]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install pyinstaller PyPDF2 requests
    
    - name: Build executable
      run: |
        cd requirements
        python build_standalone.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: PDF-to-Jira-${{ matrix.os }}
        path: requirements/dist/
```

### Manual Multi-Platform Build

1. **On macOS**: Build .app file
2. **On Windows**: Build .exe file  
3. **On Linux**: Build binary
4. Create separate distribution packages for each

## Security Considerations

⚠️ **Important for Distribution:**

1. **Never include real credentials** in distribution package
2. **Use config-sample.json** with placeholder values
3. **Educate users** about API token security
4. **Recommend** users keep their config.json private
5. **Consider** adding encryption for stored credentials

## File Size Optimization

### Reduce Executable Size

```bash
# Use UPX compression (reduces size by ~40%)
pyinstaller --onefile --upx-dir=/path/to/upx \
  pdf_to_jira_gui.py

# Exclude unnecessary modules
pyinstaller --onefile \
  --exclude-module matplotlib \
  --exclude-module numpy \
  pdf_to_jira_gui.py
```

### Tips:
- Remove unused imports from code
- Use `--exclude-module` for large unused libraries
- Use UPX compression (download from upx.github.io)
- Consider separate builds for GUI vs CLI

## Testing Distribution

Before sharing:

1. **Test on clean system** without Python
2. **Verify all features** work in executable
3. **Check file paths** are relative/configurable
4. **Test with sample PDF** and Jira instance
5. **Verify error messages** are user-friendly

## Alternative Distribution Methods

### 1. Web-Based Service

Deploy as a web app using Flask/FastAPI:
- Users access via browser
- No installation needed
- Centralized credential management

### 2. Electron App

Convert to Electron for cross-platform GUI:
- Professional appearance
- Auto-updates
- Native OS integration

### 3. Package Managers

- **macOS**: Homebrew (`brew install pdf-to-jira`)
- **Windows**: Chocolatey (`choco install pdf-to-jira`)
- **Linux**: APT/DNF packages

## Current Setup Summary

**Your Files:**
- Source: `/Users/bmnoorishah/Documents/WAREHOUSE/intellibin/requirements/`
- Scripts: GUI, CLI, and Interactive versions
- Config: Project-specific settings

**To Create Executable:**

```bash
cd /Users/bmnoorishah/Documents/WAREHOUSE/intellibin/requirements
python3 build_standalone.py
```

**Output:**
- Executable in `dist/` folder
- Distribution package in `PDF-to-Jira-Distribution/`
- Ready to share as .zip

## Support & Updates

### Version Management

Add version info to your scripts:

```python
__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "support@company.com"
```

### Update Distribution

When updating:
1. Increment version number
2. Rebuild executables
3. Create release notes
4. Notify users
5. Provide update instructions

## Troubleshooting Distribution

### "App is damaged" (macOS)

```bash
xattr -cr PDF-to-Jira.app
```

### "Windows protected your PC" (Windows)

Users need to click "More info" → "Run anyway"

Consider code signing certificate for production.

### Linux permissions

```bash
chmod +x PDF-to-Jira
```

## Recommended Distribution Workflow

1. **Develop & Test** on your machine
2. **Build executables** for target platforms
3. **Test on clean systems** (virtual machines)
4. **Package** with README and sample config
5. **Create .zip** for each platform
6. **Share via** email, cloud storage, or internal network
7. **Provide support** documentation and contact info

## Next Steps

1. Run `python3 build_standalone.py` to create executable
2. Test the executable on your machine
3. Test on a clean machine (VM or colleague's computer)
4. Create distribution package
5. Share with your team

---

**Ready to build?**

```bash
cd /Users/bmnoorishah/Documents/WAREHOUSE/intellibin/requirements
python3 build_standalone.py
```
