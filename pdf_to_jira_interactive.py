#!/usr/bin/env python3
"""
Interactive PDF to Jira Importer
Guides user through the process with interactive prompts.
"""

import os
import sys
import json
from pathlib import Path

# Import the advanced module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdf_to_jira_advanced import Config, JiraClient, PDFAnalyzer, TaskGenerator


def select_project(jira: JiraClient) -> str:
    """Interactively select a Jira project."""
    print("\n📋 Fetching available projects...")
    projects = jira.list_projects()
    
    if not projects:
        print("❌ No projects found or unable to fetch projects")
        return ""
    
    print("\nAvailable Projects:")
    print("-" * 60)
    for i, proj in enumerate(projects, 1):
        print(f"{i}. {proj.get('key'):8} - {proj.get('name')}")
    print("-" * 60)
    
    while True:
        try:
            choice = input(f"\nSelect project (1-{len(projects)}): ").strip()
            idx = int(choice) - 1
            
            if 0 <= idx < len(projects):
                selected = projects[idx]
                return selected.get('key')
            else:
                print(f"Please enter a number between 1 and {len(projects)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nCancelled by user")
            sys.exit(0)


def select_pdf() -> str:
    """Interactively select a PDF file."""
    print("\n📄 Available PDF files in requirements/:")
    
    req_dir = Path(__file__).parent / "requirements"
    if not req_dir.exists():
        req_dir = Path(__file__).parent
    
    pdf_files = list(req_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return ""
    
    print("-" * 60)
    for i, pdf in enumerate(pdf_files, 1):
        size_kb = pdf.stat().st_size / 1024
        print(f"{i}. {pdf.name:40} ({size_kb:.1f} KB)")
    print("-" * 60)
    
    while True:
        try:
            choice = input(f"\nSelect PDF (1-{len(pdf_files)}): ").strip()
            idx = int(choice) - 1
            
            if 0 <= idx < len(pdf_files):
                return str(pdf_files[idx].absolute())
            else:
                print(f"Please enter a number between 1 and {len(pdf_files)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nCancelled by user")
            sys.exit(0)


def get_task_settings() -> dict:
    """Interactively configure task settings."""
    print("\n⚙️  Task Settings")
    print("-" * 60)
    
    settings = {}
    
    # Number of tasks
    while True:
        try:
            num = input("Target number of tasks (default: auto): ").strip()
            if not num:
                break
            num = int(num)
            if num > 0:
                settings['max_tasks'] = num
                break
            print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")
    
    # Issue type
    print("\nIssue types: Task, Story, Bug, Epic")
    issue_type = input("Issue type (default: Task): ").strip()
    if issue_type:
        settings['issue_type'] = issue_type
    
    # Priority
    print("\nPriorities: Highest, High, Medium, Low, Lowest")
    priority = input("Priority (default: Medium): ").strip()
    if priority:
        settings['priority'] = priority
    
    # Labels
    labels = input("Labels (comma-separated, default: pdf-import): ").strip()
    if labels:
        settings['labels'] = [l.strip() for l in labels.split(',')]
    
    return settings


def confirm_action(message: str) -> bool:
    """Ask for user confirmation."""
    while True:
        response = input(f"\n{message} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")


def main():
    """Interactive main function."""
    print("=" * 70)
    print(" 🎯 Interactive PDF to Jira Importer")
    print("=" * 70)
    
    # Load or create config
    config_path = "config.json"
    config = Config.load_config(config_path)
    
    if not config or not config.get('jira'):
        print("\n⚠️  No configuration found. Let's set it up!")
        
        print("\n📝 Jira Configuration")
        print("-" * 60)
        
        jira_url = input("Jira URL (e.g., https://company.atlassian.net): ").strip()
        email = input("Email: ").strip()
        api_token = input("API Token: ").strip()
        
        config = {
            "jira": {
                "url": jira_url,
                "email": email,
                "api_token": api_token,
                "project_key": ""
            },
            "pdf": {"path": ""},
            "task_settings": {}
        }
    
    # Initialize Jira
    print("\n[1/5] Connecting to Jira...")
    jira = JiraClient(config)
    
    success, user_info = jira.test_connection()
    if not success:
        print("❌ Failed to connect. Please check your credentials in config.json")
        return 1
    
    print(f"✓ Connected as: {user_info.get('displayName', jira.email)}")
    
    # Select project
    project_key = select_project(jira)
    if not project_key:
        return 1
    
    jira.project_key = project_key
    config['jira']['project_key'] = project_key
    
    # Verify project
    project = jira.get_project()
    if not project:
        print(f"❌ Cannot access project {project_key}")
        return 1
    
    print(f"✓ Selected: {project.get('name')} ({project_key})")
    
    # Select PDF
    pdf_path = select_pdf()
    if not pdf_path:
        return 1
    
    config['pdf']['path'] = pdf_path
    
    # Get task settings
    task_settings = get_task_settings()
    
    # Save config
    if confirm_action("💾 Save this configuration to config.json?"):
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Configuration saved to {config_path}")
    
    # Analyze PDF
    print(f"\n[2/5] Analyzing PDF...")
    analyzer = PDFAnalyzer(pdf_path)
    
    if not analyzer.extract_content():
        return 1
    
    # Detect structure
    print(f"\n[3/5] Detecting document structure...")
    sections = analyzer.detect_structure()
    
    # Generate tasks
    print(f"\n[4/5] Generating tasks...")
    
    if sections and len(sections) > 2:
        tasks = TaskGenerator.from_sections(sections)
        print(f"✓ Generated {len(tasks)} tasks from document structure")
    else:
        target = task_settings.get('max_tasks', 15)
        tasks = TaskGenerator.from_raw_content(analyzer.raw_content, target)
        print(f"✓ Generated {len(tasks)} tasks from content analysis")
    
    if task_settings.get('max_tasks'):
        tasks = tasks[:task_settings['max_tasks']]
        print(f"  Limited to {len(tasks)} tasks")
    
    # Preview
    print(f"\n📋 Task Preview (first 3):")
    print("-" * 70)
    for i, task in enumerate(tasks[:3], 1):
        print(f"\n{i}. {task['summary']}")
        print(f"   {task['description'][:100]}...")
    
    if len(tasks) > 3:
        print(f"\n... and {len(tasks) - 3} more tasks")
    
    # Confirm creation
    if not confirm_action(f"\n🚀 Create {len(tasks)} tasks in {project_key}?"):
        print("\n❌ Cancelled by user")
        return 0
    
    # Create tasks
    print(f"\n[5/5] Creating tasks in Jira...")
    print("-" * 70)
    
    created = []
    failed = []
    
    issue_type = task_settings.get('issue_type', 'Task')
    labels = task_settings.get('labels', ['pdf-import'])
    priority = task_settings.get('priority', 'Medium')
    
    for i, task in enumerate(tasks, 1):
        print(f"[{i}/{len(tasks)}] ", end='', flush=True)
        
        issue_key = jira.create_issue(
            summary=task['summary'],
            description=task['description'],
            issue_type=issue_type,
            labels=labels,
            priority=priority
        )
        
        if issue_key:
            print(f"✓ {issue_key}")
            created.append(issue_key)
        else:
            print(f"✗ Failed")
            failed.append(task)
        
        # Rate limiting
        if i % 10 == 0:
            import time
            time.sleep(1)
    
    # Summary
    print("\n" + "=" * 70)
    print(" ✅ COMPLETED")
    print("=" * 70)
    print(f"Created: {len(created)} tasks")
    print(f"Failed:  {len(failed)} tasks")
    
    if created:
        print(f"\n🎉 View tasks in Jira:")
        print(f"   {jira.jira_url}/browse/{created[0]}")
        print(f"\n📋 Created issues:")
        for key in created[:10]:
            print(f"   • {key}")
        if len(created) > 10:
            print(f"   ... and {len(created) - 10} more")
    
    return 0 if not failed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
