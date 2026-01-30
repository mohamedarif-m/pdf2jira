# PDF to Jira Task Importer

Convert PDF requirement documents into Jira tasks automatically.

## 🚀 Quick Start

### Option 1: GUI Application (Easiest)
```bash
python3 pdf_to_jira_gui.py
```
- File browser to select PDF
- Visual configuration forms
- Test connection button
- Preview before importing
- Real-time progress tracking

### Option 2: Interactive Mode
```bash
python3 pdf_to_jira_interactive.py
```
- Guided step-by-step wizard
- Select from available projects
- Configure all settings interactively

### Option 3: Command Line
```bash
# Preview first (no tasks created)
python3 pdf_to_jira_advanced.py --dry-run --max-tasks 5

# Import to Jira
python3 pdf_to_jira_advanced.py
```

## 📦 Build Standalone Executable

Create a distributable app that runs without Python:

```bash
python3 build_executable.py
```

Output: `dist/PDF_to_Jira` (or `.exe` on Windows)

## 📚 Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete guide (start here!)
- **[PDF_TO_JIRA_README.md](PDF_TO_JIRA_README.md)** - Full documentation
- **[QUICK_START.md](QUICK_START.md)** - Quick reference
- **[BUILD_EXECUTABLE.md](BUILD_EXECUTABLE.md)** - Build guide

## ⚙️ Requirements

```bash
pip install PyPDF2 requests
```

## 🔑 Jira Setup

1. Get API token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Configure in GUI or edit `../config.json`
3. Test connection before importing

## ✨ Features

- ✅ GUI with file browser
- ✅ Smart PDF section detection
- ✅ Configurable task breakdown
- ✅ Preview before creation
- ✅ Standalone executable build
- ✅ Batch processing support
- ✅ Save/load configuration

## 🎯 Current Setup

- **Jira**: https://mdnoorishah.atlassian.net
- **Project**: KAN (My Kanban Space)
- **PDF**: Part 4 - Activity areas.pdf

## 📊 What to Expect

From sample PDF (11 pages):
- **Sections detected**: ~10-15
- **Tasks created**: ~15-20
- **Processing time**: 30-60 seconds

## 🛠️ Files

| File | Description |
|------|-------------|
| `pdf_to_jira_gui.py` | GUI application ⭐ |
| `pdf_to_jira_interactive.py` | Interactive wizard |
| `pdf_to_jira_advanced.py` | CLI with options |
| `pdf_to_jira_tasks.py` | Simple script |
| `build_executable.py` | Build standalone app |

## 💡 Examples

**GUI Mode:**
```bash
python3 pdf_to_jira_gui.py
# 1. Browse → Select PDF
# 2. Enter credentials
# 3. Test connection
# 4. Preview tasks
# 5. Import!
```

**Batch Processing:**
```bash
for pdf in *.pdf; do
    python3 pdf_to_jira_advanced.py --pdf "$pdf" --max-tasks 15
done
```

## 🐛 Troubleshooting

**Connection failed?**
- Verify API token is correct
- Check Jira URL includes `https://`
- Test connection in GUI first

**Wrong project?**
- Use GUI "List Projects" button
- Or run with `--dry-run` to see available projects

**PDF not reading?**
- Ensure PDF is text-based (not scanned image)
- Try opening PDF manually to verify

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed troubleshooting.

## 🎉 Ready to Go!

All tools are ready in this folder. Choose your preferred method and start importing!
