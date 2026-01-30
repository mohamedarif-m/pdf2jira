# PDF to Jira - Quick Start Guide

## 🚀 Three Ways to Use

### Option 1: Interactive Mode (Recommended for First Time)
```bash
python3 pdf_to_jira_interactive.py
```
- Guides you through each step
- Select project from list
- Select PDF file from list
- Configure task settings
- Preview before creating
- Save configuration for future use

### Option 2: Command Line (Advanced)
```bash
# Dry run (preview only)
python3 pdf_to_jira_advanced.py --dry-run

# Create tasks
python3 pdf_to_jira_advanced.py

# With options
python3 pdf_to_jira_advanced.py --max-tasks 10 --pdf path/to/file.pdf
```

### Option 3: Simple Script (Basic)
```bash
python3 pdf_to_jira_tasks.py
```
- Uses hardcoded settings
- No configuration needed
- Edit the script to change settings

## 📋 Current Configuration

**Your Jira Instance:**
- URL: https://mdnoorishah.atlassian.net
- Email: mdnoorishah@gmail.com
- Project: KAN (My Kanban Space)

**PDF File:**
- Part 4 - Activity areas.pdf (11 pages)

## 🎯 What Will Happen

1. **Connect to Jira** - Verify credentials and project access
2. **Read PDF** - Extract all text from the PDF
3. **Detect Structure** - Find sections, headings, and logical breaks
4. **Generate Tasks** - Create one task per section (or split large sections)
5. **Create in Jira** - Upload tasks using Jira REST API

## 📊 Expected Results

From "Part 4 - Activity areas.pdf":
- **Detected sections:** ~10-15
- **Tasks to create:** ~15-20
- **Each task includes:**
  - Summary: Section title
  - Description: Section content
  - Labels: pdf-import, requirements
  - Issue Type: Task

## ✅ Ready to Run?

**Dry run first (no tasks created):**
```bash
cd /Users/bmnoorishah/Documents/WAREHOUSE/intellibin
python3 pdf_to_jira_advanced.py --dry-run --max-tasks 5
```

**Create tasks:**
```bash
cd /Users/bmnoorishah/Documents/WAREHOUSE/intellibin
python3 pdf_to_jira_advanced.py
```

**Interactive mode:**
```bash
cd /Users/bmnoorishah/Documents/WAREHOUSE/intellibin
python3 pdf_to_jira_interactive.py
```

## 🔧 Troubleshooting

**If you get "module not found":**
```bash
python3 -m pip install PyPDF2 requests
```

**If project not found:**
- Run with `--dry-run` to see available projects
- Update `config.json` with correct project key

**If API token expires:**
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Create new token
3. Update `config.json`

## 📝 Command Line Options

```bash
python3 pdf_to_jira_advanced.py [OPTIONS]

Options:
  --config FILE       Config file (default: config.json)
  --pdf FILE          PDF file path (overrides config)
  --dry-run           Preview without creating tasks
  --max-tasks N       Limit number of tasks to create
  --help              Show help message
```

## 🎨 Customization

Edit `config.json`:

```json
{
  "task_settings": {
    "issue_type": "Story",        // Change to Story, Bug, Epic, etc.
    "max_content_length": 3000,   // Increase for longer descriptions
    "target_tasks": 20,           // Target number of tasks
    "add_labels": ["requirements", "automated"],
    "priority": "High"            // Highest, High, Medium, Low, Lowest
  }
}
```

## 📈 Tips

1. **Start with dry-run** to preview tasks
2. **Limit tasks** for testing: `--max-tasks 5`
3. **Save config** in interactive mode for reuse
4. **Check labels** - use consistent labels for filtering
5. **Review in Jira** - adjust task descriptions as needed

## 🔐 Security

- Never commit `config.json` with credentials
- Rotate API tokens regularly
- Use separate tokens for automation

## 📚 Files Created

- `pdf_to_jira_tasks.py` - Simple version
- `pdf_to_jira_advanced.py` - Advanced with CLI options
- `pdf_to_jira_interactive.py` - Interactive guided mode
- `config.json` - Configuration file
- `PDF_TO_JIRA_README.md` - Full documentation
- `QUICK_START.md` - This file
