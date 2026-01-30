# 🎯 PDF to Jira - Complete Solution

## Overview

A complete toolkit to import PDF requirement documents into Jira, featuring:
- ✅ **GUI Application** - User-friendly interface with file browser
- ✅ **Command-line tools** - Automated scripts for power users  
- ✅ **Standalone executable** - Run without Python installed
- ✅ **Fully configurable** - JSON config or interactive setup

---

## 🚀 Quick Start

### Option 1: GUI Application (Recommended)

```bash
cd requirements
python3 pdf_to_jira_gui.py
```

**Features:**
- 📂 Browse and select PDF files
- 🔐 Configure Jira credentials visually
- ✅ Test connection before import
- 👀 Preview tasks before creating
- 📊 Real-time progress and logging
- 💾 Save configuration for reuse

**Screenshot of GUI:**
```
┌──────────────────────────────────────────────────┐
│  📄 PDF to Jira Task Importer                    │
├──────────────────────────────────────────────────┤
│                                                   │
│  1. Select PDF File                              │
│  PDF File: [________________________] [Browse]   │
│                                                   │
│  2. Jira Configuration                           │
│  Jira URL:    [_____________________________]    │
│  Email:       [_____________________________]    │
│  API Token:   [*************************]        │
│               [Test Connection]                  │
│  Project Key: [KAN___] [List Projects]          │
│                                                   │
│  3. Task Settings                                │
│  Issue Type:  [Task ▼]                           │
│  Priority:    [Medium ▼]                         │
│  Labels:      [pdf-import,requirements]          │
│  Max Tasks:   [15__] (leave empty for auto)      │
│                                                   │
│  [Preview Tasks] [Import to Jira] [Save Config]  │
│                                                   │
│  Output Log:                                     │
│  ┌────────────────────────────────────────────┐  │
│  │ ℹ️ Selected PDF: Part 4 - Activity...      │  │
│  │ ✓ Connected as: mdnoorishah               │  │
│  │ ✓ Project: My Kanban Space               │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Option 2: Interactive Mode

```bash
cd requirements
python3 pdf_to_jira_interactive.py
```

Guides you through:
1. Project selection from list
2. PDF file selection
3. Task configuration
4. Preview and confirmation

### Option 3: Command Line

```bash
cd requirements

# Preview first
python3 pdf_to_jira_advanced.py --dry-run --max-tasks 5

# Import to Jira
python3 pdf_to_jira_advanced.py

# Custom options
python3 pdf_to_jira_advanced.py --pdf "other-file.pdf" --max-tasks 20
```

---

## 📦 Building Standalone Executable

Create an executable that runs without Python:

```bash
cd requirements
python3 build_executable.py
```

This creates:
- **macOS**: `dist/PDF_to_Jira` (~18 MB)
- **Windows**: `dist/PDF_to_Jira.exe` (~12 MB)  
- **Linux**: `dist/PDF_to_Jira` (~15 MB)

**Distribute** the file from `dist/` folder - users can double-click to run!

See [BUILD_EXECUTABLE.md](BUILD_EXECUTABLE.md) for advanced build options.

---

## 📁 Files Overview

```
requirements/
├── pdf_to_jira_gui.py              ⭐ GUI application
├── pdf_to_jira_interactive.py      🎯 Interactive wizard
├── pdf_to_jira_advanced.py         🔧 CLI with options
├── pdf_to_jira_tasks.py            📝 Simple script
│
├── build_executable.py             📦 Build standalone app
│
├── PDF_TO_JIRA_README.md           📚 Complete documentation
├── QUICK_START.md                  ⚡ Quick reference
├── BUILD_EXECUTABLE.md             🏗️ Build guide
├── GETTING_STARTED.md              👋 This file
│
└── Part 4 - Activity areas.pdf     📄 Sample PDF
```

---

## ⚙️ Configuration

### Method 1: GUI Configuration

1. Launch GUI: `python3 pdf_to_jira_gui.py`
2. Fill in all fields
3. Click "Save Config"
4. Config saved to `../config.json`

### Method 2: Manual Configuration

Edit `config.json` in project root:

```json
{
  "jira": {
    "url": "https://your-domain.atlassian.net",
    "email": "your-email@example.com",
    "api_token": "your-api-token-here",
    "project_key": "PROJ"
  },
  "pdf": {
    "path": "/full/path/to/requirements.pdf"
  },
  "task_settings": {
    "issue_type": "Task",
    "priority": "Medium",
    "add_labels": ["pdf-import", "requirements"],
    "max_content_length": 2000,
    "target_tasks": 15
  }
}
```

### Method 3: Command Line Override

```bash
python3 pdf_to_jira_advanced.py \
  --pdf "/path/to/file.pdf" \
  --max-tasks 20 \
  --config "custom-config.json"
```

---

## 🔑 Getting Jira API Token

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Label it (e.g., "PDF Importer")
4. Copy the token
5. Paste in GUI or config.json

**Security:** Never commit config.json with real token to Git!

---

## 📋 Current Setup

Your configuration:
```
Jira URL:     https://mdnoorishah.atlassian.net
Email:        mdnoorishah@gmail.com
Project:      KAN (My Kanban Space)
PDF File:     Part 4 - Activity areas.pdf
```

---

## 🎬 Workflow

### Standard Workflow

1. **Select PDF** → Browse to requirements document
2. **Configure Jira** → Enter URL, email, token, project
3. **Test Connection** → Verify credentials work
4. **Preview Tasks** → See what will be created
5. **Import** → Create tasks in Jira
6. **Review** → Check tasks in Jira web interface

### Batch Processing

```bash
# Process multiple PDFs
for pdf in *.pdf; do
    python3 pdf_to_jira_advanced.py --pdf "$pdf" --max-tasks 10
    sleep 2  # Rate limiting
done
```

---

## 🔧 Advanced Features

### Custom Task Breakdown

The tool intelligently breaks down PDF content:

1. **Structure Detection**: Finds headings, sections, numbered lists
2. **Content Chunking**: Splits large sections at sentence boundaries
3. **Smart Sizing**: Keeps descriptions under max length
4. **Context Preservation**: Maintains section hierarchy

### Supported PDF Features

- ✅ Multi-page documents
- ✅ Text-based PDFs (not scanned images)
- ✅ Structured documents with headings
- ✅ Unstructured plain text
- ✅ Mixed content (text + formatting)

### Customization

**Issue Types**: Task, Story, Bug, Epic
**Priorities**: Highest, High, Medium, Low, Lowest  
**Labels**: Custom tags (comma-separated)
**Max Tasks**: Limit number created (for testing)

---

## 📊 What to Expect

From "Part 4 - Activity areas.pdf":

```
Input:
  Pages:        11
  Characters:   ~13,000
  Sections:     ~10-15

Output:
  Tasks:        ~15-20
  Time:         ~30-60 seconds
  Each task:    Section title + content
  Labels:       pdf-import, requirements
```

---

## 🐛 Troubleshooting

### GUI doesn't launch

**Issue**: No window appears  
**Solution**: Make sure X11/display server is running (Linux/SSH)

```bash
# Run in terminal mode instead
python3 pdf_to_jira_interactive.py
```

### "Module not found" errors

**Issue**: Missing dependencies  
**Solution**: Install requirements

```bash
pip3 install PyPDF2 requests
```

### "Project not found"

**Issue**: Wrong project key  
**Solution**: Use GUI "List Projects" or run:

```bash
python3 pdf_to_jira_advanced.py --dry-run
# Shows available projects in output
```

### Authentication failed

**Issue**: Invalid credentials  
**Solution**:
1. Regenerate API token
2. Check email is correct  
3. Verify Jira URL (include https://)

### PDF extraction failed

**Issue**: Can't read PDF  
**Solution**:
- Ensure PDF is text-based (not scanned image)
- Check file permissions
- Try opening PDF manually to verify

### Too many/few tasks

**Issue**: Not right number of tasks  
**Solution**: Adjust in GUI or config:

```json
{
  "task_settings": {
    "target_tasks": 25,  // Increase/decrease
    "max_content_length": 3000  // Larger = fewer tasks
  }
}
```

---

## 💡 Tips & Best Practices

### Before First Run

1. ✅ Test connection in GUI
2. ✅ Use Preview mode first
3. ✅ Start with `--max-tasks 5` for testing
4. ✅ Save config for future use

### During Import

1. 📊 Watch progress in log
2. ⏱️ Be patient (rate limiting)
3. 🔍 Check first few tasks in Jira
4. 🛑 Can stop if issues detected

### After Import

1. 📝 Review tasks in Jira
2. 🏷️ Adjust labels if needed
3. 👥 Assign to team members
4. 📋 Create epics/sprints

### Optimization

```bash
# For large PDFs (100+ pages)
python3 pdf_to_jira_advanced.py --max-tasks 50

# For quick import (small documents)
python3 pdf_to_jira_advanced.py --max-tasks 10

# For detailed breakdown
# Edit config.json: "max_content_length": 1000
```

---

## 🔒 Security

### Protecting Credentials

```bash
# Add to .gitignore
echo "config.json" >> ../.gitignore

# Use environment variables
export JIRA_TOKEN="your-token"
# Update script to read from env
```

### Token Best Practices

- 🔄 Rotate tokens every 90 days
- 🔐 Use separate tokens per purpose
- 📝 Label tokens clearly
- 🗑️ Delete unused tokens

---

## 📈 Scaling

### Multiple Projects

```json
// configs/project-a.json
{
  "jira": {
    "project_key": "PROJA"
  }
}

// configs/project-b.json  
{
  "jira": {
    "project_key": "PROJB"
  }
}
```

```bash
python3 pdf_to_jira_advanced.py --config configs/project-a.json
python3 pdf_to_jira_advanced.py --config configs/project-b.json
```

### Automation

```bash
#!/bin/bash
# auto-import.sh

for pdf in /path/to/pdfs/*.pdf; do
    echo "Processing: $pdf"
    python3 pdf_to_jira_advanced.py \
        --pdf "$pdf" \
        --max-tasks 15
    
    # Rate limiting
    sleep 5
done
```

---

## 🎓 Examples

### Example 1: Quick Test

```bash
cd requirements
python3 pdf_to_jira_advanced.py --dry-run --max-tasks 3
```

Output:
```
[DRY RUN] Would create 3 tasks:
  1. Activity Areas
     Description: Section: Activity Areas...
  2. Define Activity Areas
     Description: Section: Define Activity Areas...
  3. Define Sort Sequence
     Description: Section: Define Sort Sequence...
```

### Example 2: GUI Workflow

1. Launch: `python3 pdf_to_jira_gui.py`
2. Click "Browse" → Select PDF
3. Fill Jira details → Click "Test Connection"
4. Click "List Projects" → Select project
5. Click "Preview Tasks" → Review output
6. Click "Import to Jira" → Confirm
7. ✅ Done! Tasks created

### Example 3: Batch Processing

```python
# batch_import.py
import subprocess
import os

pdfs = [
    "Part 1 - Overview.pdf",
    "Part 2 - Requirements.pdf",
    "Part 3 - Architecture.pdf",
]

for pdf in pdfs:
    print(f"Processing {pdf}...")
    subprocess.run([
        "python3", "pdf_to_jira_advanced.py",
        "--pdf", pdf,
        "--max-tasks", "20"
    ])
```

---

## 📞 Support & Resources

**Documentation:**
- [PDF_TO_JIRA_README.md](PDF_TO_JIRA_README.md) - Full documentation
- [QUICK_START.md](QUICK_START.md) - Quick reference
- [BUILD_EXECUTABLE.md](BUILD_EXECUTABLE.md) - Build guide

**Jira API:**
- https://developer.atlassian.com/cloud/jira/platform/rest/v3/

**PyPDF2:**
- https://pypdf2.readthedocs.io/

**PyInstaller:**
- https://pyinstaller.org/

---

## ✅ Checklist

Before distributing to team:

- [ ] Test with sample PDF
- [ ] Verify Jira connection
- [ ] Build standalone executable
- [ ] Create user guide
- [ ] Set up shared config (without token!)
- [ ] Test on clean machine
- [ ] Document troubleshooting steps
- [ ] Set up support channel

---

## 🎉 You're Ready!

Everything is set up and ready to use:

```bash
# Start here:
cd /Users/bmnoorishah/Documents/WAREHOUSE/intellibin/requirements

# Option 1: GUI
python3 pdf_to_jira_gui.py

# Option 2: Interactive
python3 pdf_to_jira_interactive.py

# Option 3: Quick command
python3 pdf_to_jira_advanced.py --dry-run
```

**Happy importing! 🚀**
