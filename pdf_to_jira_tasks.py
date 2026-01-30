#!/usr/bin/env python3
"""
PDF to Jira Tasks Creator
Reads PDF files, breaks down content into multiple tasks, and creates them in Jira.
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Optional
import requests
from requests.auth import HTTPBasicAuth

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not installed. Installing...")
    os.system(f"{sys.executable} -m pip install PyPDF2")
    import PyPDF2

try:
    from openai import OpenAI
except ImportError:
    print("openai not installed. Installing...")
    os.system(f"{sys.executable} -m pip install openai")
    from openai import OpenAI


class JiraTaskCreator:
    """Handles creation of Jira tasks via API."""
    
    def __init__(self, jira_url: str, email: str, api_token: str, project_key: str):
        """
        Initialize Jira API client.
        
        Args:
            jira_url: Base URL of Jira instance (e.g., https://company.atlassian.net)
            email: Email address for authentication
            api_token: Jira API token
            project_key: Project key in Jira (e.g., 'PROJ')
        """
        self.jira_url = jira_url.rstrip('/')
        self.email = email
        self.api_token = api_token
        self.project_key = project_key
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def test_connection(self) -> bool:
        """Test Jira connection and credentials."""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/myself",
                headers=self.headers,
                auth=self.auth
            )
            if response.status_code == 200:
                user_info = response.json()
                print(f"✓ Connected to Jira as: {user_info.get('displayName', self.email)}")
                return True
            else:
                print(f"✗ Connection failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {str(e)}")
            return False
    
    def get_project_info(self) -> Optional[Dict]:
        """Get project information."""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/project/{self.project_key}",
                headers=self.headers,
                auth=self.auth
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"✗ Project fetch failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"✗ Project fetch error: {str(e)}")
            return None
    
    def get_issue_types(self) -> List[Dict]:
        """Get available issue types for the project."""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/project/{self.project_key}/statuses",
                headers=self.headers,
                auth=self.auth
            )
            if response.status_code == 200:
                data = response.json()
                return data
            return []
        except Exception as e:
            print(f"✗ Issue types fetch error: {str(e)}")
            return []
    
    def create_task(self, summary: str, description: str, issue_type: str = "Task") -> Optional[str]:
        """
        Create a Jira task.
        
        Args:
            summary: Task summary/title
            description: Task description
            issue_type: Type of issue (Task, Story, Bug, etc.)
        
        Returns:
            Created issue key or None if failed
        """
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "name": issue_type
                }
            }
        }
        
        try:
            response = requests.post(
                f"{self.jira_url}/rest/api/3/issue",
                headers=self.headers,
                auth=self.auth,
                data=json.dumps(payload)
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                issue_key = issue_data.get('key')
                print(f"✓ Created task: {issue_key} - {summary}")
                return issue_key
            else:
                print(f"✗ Task creation failed: {response.status_code}")
                print(f"  Response: {response.text}")
                return None
        except Exception as e:
            print(f"✗ Task creation error: {str(e)}")
            return None


class PDFProcessor:
    """Handles PDF reading and content extraction."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF processor.
        
        Args:
            pdf_path: Path to PDF file
        """
        self.pdf_path = pdf_path
        self.content = ""
    
    def extract_text(self) -> str:
        """Extract all text from PDF."""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                print(f"📄 Reading PDF: {num_pages} pages")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    self.content += f"\n\n--- Page {page_num + 1} ---\n\n{text}"
                
                print(f"✓ Extracted {len(self.content)} characters")
                return self.content
        except Exception as e:
            print(f"✗ PDF extraction error: {str(e)}")
            return ""
    
    def break_into_sections(self) -> List[Dict[str, str]]:
        """
        Break PDF content into logical sections based on headings and structure.
        
        Returns:
            List of sections with title and content
        """
        sections = []
        lines = self.content.split('\n')
        current_section = {"title": "Introduction", "content": ""}
        
        # Pattern to detect headings (all caps, numbered sections, etc.)
        heading_patterns = [
            r'^[0-9]+\.[\s]*[A-Z]',  # 1. HEADING
            r'^[A-Z][A-Z\s]{10,}$',  # ALL CAPS HEADING
            r'^[0-9]+\.[0-9]+[\s]*[A-Z]',  # 1.1 Subheading
        ]
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('---'):
                continue
            
            # Check if line is a heading
            is_heading = any(re.match(pattern, line) for pattern in heading_patterns)
            
            if is_heading and len(line) < 100:
                # Save previous section if it has content
                if current_section["content"].strip():
                    sections.append(current_section.copy())
                
                # Start new section
                current_section = {
                    "title": line,
                    "content": ""
                }
            else:
                current_section["content"] += line + "\n"
        
        # Add the last section
        if current_section["content"].strip():
            sections.append(current_section)
        
        print(f"✓ Broke content into {len(sections)} sections")
        return sections


class TaskBreakdown:
    """Breaks down PDF content into actionable Jira tasks."""
    
    @staticmethod
    def create_tasks_from_sections(sections: List[Dict[str, str]], max_content_length: int = 1500) -> List[Dict[str, str]]:
        """
        Create task breakdown from sections.
        
        Args:
            sections: List of content sections
            max_content_length: Maximum content length per task
        
        Returns:
            List of tasks with summary and description
        """
        tasks = []
        
        for idx, section in enumerate(sections, 1):
            title = section['title'].strip()
            content = section['content'].strip()
            
            # Skip very short sections
            if len(content) < 50:
                continue
            
            # Clean up the title
            title = re.sub(r'^[0-9]+\.[\s]*', '', title)  # Remove numbering
            title = title[:100]  # Limit length
            
            # If content is too long, split it
            if len(content) > max_content_length:
                # Split into chunks
                chunks = [content[i:i+max_content_length] for i in range(0, len(content), max_content_length)]
                
                for chunk_idx, chunk in enumerate(chunks, 1):
                    task_summary = f"{title} (Part {chunk_idx}/{len(chunks)})"
                    tasks.append({
                        "summary": task_summary,
                        "description": chunk,
                        "section": idx,
                        "part": chunk_idx
                    })
            else:
                tasks.append({
                    "summary": title,
                    "description": content,
                    "section": idx,
                    "part": 1
                })
        
        print(f"✓ Created {len(tasks)} task breakdowns")
        return tasks
    
    @staticmethod
    def create_intelligent_breakdown(content: str, num_tasks: int = 10) -> List[Dict[str, str]]:
        """
        Create intelligent task breakdown using simple heuristics.
        
        Args:
            content: Full PDF content
            num_tasks: Target number of tasks to create
        
        Returns:
            List of tasks
        """
        # Split content into roughly equal parts
        words = content.split()
        words_per_task = max(len(words) // num_tasks, 100)
        
        tasks = []
        current_words = []
        task_num = 1
        
        for word in words:
            current_words.append(word)
            
            # Check if we have enough words and are at a sentence boundary
            if len(current_words) >= words_per_task and word.endswith('.'):
                task_content = ' '.join(current_words)
                
                # Create summary from first sentence or first N words
                first_sentence = task_content.split('.')[0][:100]
                
                tasks.append({
                    "summary": f"Requirement Task {task_num}: {first_sentence}",
                    "description": task_content,
                    "section": task_num,
                    "part": 1
                })
                
                current_words = []
                task_num += 1
        
        # Add remaining content as last task
        if current_words:
            task_content = ' '.join(current_words)
            first_sentence = task_content.split('.')[0][:100]
            tasks.append({
                "summary": f"Requirement Task {task_num}: {first_sentence}",
                "description": task_content,
                "section": task_num,
                "part": 1
            })
        
        return tasks


def main():
    """Main execution function."""
    print("=" * 60)
    print("PDF to Jira Tasks Creator")
    print("=" * 60)
    
    # Configuration - Use environment variables or update these values
    JIRA_URL = os.environ.get('JIRA_URL', "https://your-domain.atlassian.net")
    JIRA_EMAIL = os.environ.get('JIRA_EMAIL', "your-email@example.com")
    JIRA_TOKEN = os.environ.get('JIRA_TOKEN', "YOUR_API_TOKEN_HERE")
    PROJECT_KEY = os.environ.get('JIRA_PROJECT_KEY', "PROJ")
    PDF_PATH = "/Users/bmnoorishah/Documents/WAREHOUSE/intellibin/requirements/Part 4 - Activity areas.pdf"
    
    # Step 1: Initialize Jira client
    print("\n[1] Initializing Jira connection...")
    jira = JiraTaskCreator(JIRA_URL, JIRA_EMAIL, JIRA_TOKEN, PROJECT_KEY)
    
    if not jira.test_connection():
        print("\n❌ Failed to connect to Jira. Please check your credentials.")
        return
    
    # Get project info
    project_info = jira.get_project_info()
    if project_info:
        print(f"✓ Project: {project_info.get('name', PROJECT_KEY)}")
    else:
        print("⚠ Could not fetch project info. Trying alternative project keys...")
        # Try common variations
        for alt_key in ["INTEL", "IB", "INTELLIB"]:
            jira.project_key = alt_key
            if jira.get_project_info():
                print(f"✓ Using project key: {alt_key}")
                break
    
    # Step 2: Process PDF
    print("\n[2] Processing PDF...")
    pdf_processor = PDFProcessor(PDF_PATH)
    content = pdf_processor.extract_text()
    
    if not content:
        print("\n❌ Failed to extract PDF content.")
        return
    
    # Step 3: Break down into sections/tasks
    print("\n[3] Breaking down content into tasks...")
    sections = pdf_processor.break_into_sections()
    
    if not sections:
        print("⚠ Could not detect sections. Using intelligent breakdown...")
        tasks = TaskBreakdown.create_intelligent_breakdown(content, num_tasks=15)
    else:
        tasks = TaskBreakdown.create_tasks_from_sections(sections)
    
    print(f"\n📋 Prepared {len(tasks)} tasks for creation")
    
    # Step 4: Create tasks in Jira
    print("\n[4] Creating tasks in Jira...")
    print("=" * 60)
    
    created_tasks = []
    failed_tasks = []
    
    for idx, task in enumerate(tasks, 1):
        print(f"\nTask {idx}/{len(tasks)}:")
        issue_key = jira.create_task(
            summary=task['summary'],
            description=task['description'],
            issue_type="Task"
        )
        
        if issue_key:
            created_tasks.append(issue_key)
        else:
            failed_tasks.append(task)
        
        # Add small delay to avoid rate limiting
        import time
        time.sleep(0.5)
    
    # Step 5: Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Successfully created: {len(created_tasks)} tasks")
    print(f"✗ Failed to create: {len(failed_tasks)} tasks")
    
    if created_tasks:
        print(f"\n🎉 Created tasks: {', '.join(created_tasks)}")
        print(f"\nView in Jira: {JIRA_URL}/browse/{created_tasks[0]}")
    
    if failed_tasks:
        print(f"\n⚠ Failed tasks:")
        for task in failed_tasks:
            print(f"  - {task['summary'][:60]}...")
    
    print("\n✅ Process completed!")


if __name__ == "__main__":
    main()
