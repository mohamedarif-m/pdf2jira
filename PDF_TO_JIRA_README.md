# PDF to Jira Tasks Importer

Automatically read PDF requirement documents and create structured tasks in Jira.

## Features

- 📄 **PDF Parsing**: Extract text from PDF files using PyPDF2
- 🤖 **Intelligent Breakdown**: Automatically detect document structure and break content into logical tasks
- 🎯 **Jira Integration**: Create tasks directly in Jira using REST API
- ⚙️ **Configurable**: Use JSON config file for easy setup
- 🔍 **Dry Run Mode**: Preview tasks before creation
- 📊 **Progress Tracking**: Real-time feedback during task creation

## Quick Start

### 1. Install Dependencies

```bash
pip install PyPDF2 requests
```

### 2. Configure Jira Settings

Edit `config.json`:

```json
{
  "jira": {
    "url": "https://your-domain.atlassian.net",
    "email": "your-email@example.com",
    "api_token": "your-api-token",
    "project_key": "YOUR_PROJECT_KEY"
  },
  "pdf": {
    "path": "/path/to/requirements.pdf"
  },
  "task_settings": {
    "issue_type": "Task",
    "max_content_length": 2000,
    "target_tasks": 15,
    "add_labels": ["pdf-import", "requirements"],
    "priority": "Medium"
  }
}
```

### 3. Run the Importer

**Simple version:**
```bash
python pdf_to_jira_tasks.py
```

**Advanced version with options:**
```bash
# Dry run (preview without creating)
python pdf_to_jira_advanced.py --dry-run

# Specify PDF file
python pdf_to_jira_advanced.py --pdf /path/to/document.pdf

# Limit number of tasks
python pdf_to_jira_advanced.py --max-tasks 10

# Use custom config
python pdf_to_jira_advanced.py --config my-config.json
```

## Getting Jira API Token

1. Go to [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a label (e.g., "PDF Importer")
4. Copy the token and paste it in `config.json`

## Finding Your Project Key

1. Go to your Jira project
2. Look at the URL: `https://your-domain.atlassian.net/browse/PROJ-123`
3. The project key is `PROJ` (the part before the dash)

Or run the script with an invalid project key - it will list all available projects.

## How It Works

### Basic Script (`pdf_to_jira_tasks.py`)

1. **PDF Extraction**: Reads PDF and extracts all text
2. **Section Detection**: Identifies sections based on:
   - Numbered headings (1.2.3)
   - All caps text
   - Title Case headings
3. **Task Creation**: Creates one task per section (splits large sections)
4. **Jira Upload**: Creates tasks via Jira REST API

### Advanced Script (`pdf_to_jira_advanced.py`)

Enhanced features:
- Better structure detection with multiple pattern types
- Configurable via JSON file
- Command-line arguments for flexibility
- Dry-run mode to preview tasks
- Better error handling and reporting
- Automatic content chunking at sentence boundaries
- Project validation and listing

## Task Breakdown Strategy

The scripts use intelligent algorithms to break down PDF content:

1. **Structure-Based**: If the PDF has clear headings/sections, creates one task per section
2. **Content-Based**: For unstructured content, splits into equal parts at sentence boundaries
3. **Size Limiting**: Ensures no task description exceeds maximum length (configurable)

## Example Output

```
======================================================================
 PDF to Jira Requirements Import
======================================================================

[1/5] Connecting to Jira...
✓ Connected as: John Doe
✓ Project: Intellibin (INT)

[2/5] Analyzing PDF...
📄 PDF: Part 4 - Activity areas.pdf
   Pages: 11
   Characters: 45,238

[3/5] Detecting document structure...
📑 Detected 23 sections

[4/5] Generating tasks...
✓ Generated 18 tasks from document structure

[5/5] Creating 18 tasks in Jira...
----------------------------------------------------------------------
[1/18] ✓ INT-101: Activity Areas Overview
[2/18] ✓ INT-102: Goods Receipt Processing
[3/18] ✓ INT-103: Putaway Strategies
...

======================================================================
 SUMMARY
======================================================================
✓ Created: 18 tasks
✗ Failed:  0 tasks

🎉 View tasks: https://mdnoorishah.atlassian.net/browse/INT-101
```

## Configuration Options

### Jira Settings

- `url`: Your Jira instance URL
- `email`: Your Jira account email
- `api_token`: API token for authentication
- `project_key`: Project identifier (e.g., "INT", "PROJ")

### PDF Settings

- `path`: Full path to PDF file

### Task Settings

- `issue_type`: Type of Jira issue (Task, Story, Bug, etc.)
- `max_content_length`: Maximum characters per task description
- `target_tasks`: Target number of tasks to create (for unstructured content)
- `add_labels`: Labels to add to all created tasks
- `priority`: Task priority (Low, Medium, High, Highest, Lowest)

## Troubleshooting

### "Project not found" Error

The project key might be wrong. Run with `--dry-run` to see available projects:

```bash
python pdf_to_jira_advanced.py --dry-run
```

### "Authentication failed" Error

- Verify your email is correct
- Regenerate your API token
- Make sure there are no extra spaces in the token

### "PDF extraction failed" Error

- Verify the PDF path is correct
- Ensure the PDF is not encrypted
- Try opening the PDF to verify it's not corrupted

### Too Many/Too Few Tasks

Adjust in `config.json`:

```json
{
  "task_settings": {
    "target_tasks": 20,  // Increase/decrease as needed
    "max_content_length": 3000  // Larger = fewer tasks
  }
}
```

Or use command-line:
```bash
python pdf_to_jira_advanced.py --max-tasks 25
```

## Files

- `pdf_to_jira_tasks.py` - Simple, standalone script
- `pdf_to_jira_advanced.py` - Advanced script with more features
- `config.json` - Configuration file
- `PDF_TO_JIRA_README.md` - This file

## Security Notes

⚠️ **Important**: 
- Never commit `config.json` with real credentials to version control
- Add `config.json` to `.gitignore`
- Rotate API tokens regularly
- Use separate tokens for different purposes

## Current Configuration

Your current setup:
- **Jira URL**: https://mdnoorishah.atlassian.net
- **Email**: mdnoorishah@gmail.com
- **Project**: Intellibin (INT)
- **PDF**: Part 4 - Activity areas.pdf

## Next Steps

1. Review `config.json` settings
2. Run in dry-run mode first: `python pdf_to_jira_advanced.py --dry-run`
3. If satisfied, run without dry-run to create tasks
4. Check created tasks in Jira
5. Adjust settings if needed and re-run for other PDFs

## Support

For issues with:
- **PDF parsing**: Check PDF format, try different PDF library
- **Jira API**: Consult [Jira REST API docs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- **Task breakdown**: Adjust `target_tasks` and `max_content_length` settings
