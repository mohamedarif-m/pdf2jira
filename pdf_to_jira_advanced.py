#!/usr/bin/env python3
"""
Advanced PDF to Jira Tasks Creator
Reads PDF files, uses intelligent content breakdown, and creates structured tasks in Jira.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

try:
    import PyPDF2
except ImportError:
    print("Installing PyPDF2...")
    os.system(f"{sys.executable} -m pip install PyPDF2")
    import PyPDF2


class Config:
    """Handles configuration loading and validation."""
    
    @staticmethod
    def load_config(config_path: str = "config.json") -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠ Config file not found: {config_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"⚠ Invalid JSON in config: {e}")
            return {}


class JiraClient:
    """Enhanced Jira API client with better error handling."""
    
    def __init__(self, config: Dict):
        """Initialize Jira client from config."""
        jira_config = config.get('jira', {})
        self.jira_url = jira_config.get('url', '').rstrip('/')
        self.email = jira_config.get('email', '')
        self.api_token = jira_config.get('api_token', '')
        self.project_key = jira_config.get('project_key', '')
        
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        self.task_settings = config.get('task_settings', {})
    
    def validate_config(self) -> bool:
        """Validate that all required config is present."""
        if not all([self.jira_url, self.email, self.api_token, self.project_key]):
            print("❌ Missing required Jira configuration")
            return False
        return True
    
    def test_connection(self) -> Tuple[bool, Optional[Dict]]:
        """Test Jira connection and return user info."""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/myself",
                headers=self.headers,
                auth=self.auth,
                timeout=10
            )
            
            if response.status_code == 200:
                user_info = response.json()
                return True, user_info
            else:
                print(f"✗ Auth failed: {response.status_code}")
                try:
                    error_data = response.json()
                    error_msg = error_data.get('errorMessages', [response.text[:200]])
                    print(f"  {error_msg}")
                except:
                    print(f"  {response.text[:200]}")
                return False, {'error': response.text, 'status_code': response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {str(e)}")
            return False, {'error': str(e)}
    
    def get_project(self) -> Optional[Dict]:
        """Get project information and validate access."""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/project/{self.project_key}",
                headers=self.headers,
                auth=self.auth,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"✗ Project '{self.project_key}' not found")
                return None
            else:
                print(f"✗ Project fetch failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Error fetching project: {str(e)}")
            return None
    
    def list_projects(self) -> List[Dict]:
        """List all accessible projects."""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/project/search",
                headers=self.headers,
                auth=self.auth,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('values', [])
            return []
        except Exception as e:
            print(f"✗ Error listing projects: {str(e)}")
            return []
    
    def create_issue(self, summary: str, description: str, 
                    issue_type: Optional[str] = None, 
                    labels: Optional[List[str]] = None,
                    priority: Optional[str] = None) -> Optional[str]:
        """
        Create a Jira issue with enhanced formatting.
        
        Args:
            summary: Issue summary/title
            description: Issue description
            issue_type: Type of issue (defaults to config)
            labels: Labels to add (defaults to config)
            priority: Priority level (defaults to config)
        
        Returns:
            Created issue key or None
        """
        issue_type = issue_type or self.task_settings.get('issue_type', 'Task')
        labels = labels or self.task_settings.get('add_labels', [])
        priority_name = priority or self.task_settings.get('priority', 'Medium')
        
        # Build description in Jira format (Atlassian Document Format)
        description_content = self._format_description(description)
        
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": summary[:255],  # Jira limit
                "description": description_content,
                "issuetype": {"name": issue_type}
            }
        }
        
        # Add optional fields
        if labels:
            payload["fields"]["labels"] = labels
        
        if priority_name:
            payload["fields"]["priority"] = {"name": priority_name}
        
        try:
            response = requests.post(
                f"{self.jira_url}/rest/api/3/issue",
                headers=self.headers,
                auth=self.auth,
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                return issue_data.get('key')
            else:
                print(f"✗ Failed ({response.status_code}): {summary[:50]}...")
                error_detail = response.json() if response.text else {}
                if 'errors' in error_detail:
                    print(f"  Errors: {error_detail['errors']}")
                return None
        except Exception as e:
            print(f"✗ Exception creating issue: {str(e)}")
            return None
    
    def _format_description(self, text: str) -> Dict:
        """Format description text into Atlassian Document Format."""
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        content = []
        for para in paragraphs:
            if para:
                content.append({
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": para
                        }
                    ]
                })
        
        return {
            "type": "doc",
            "version": 1,
            "content": content if content else [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": text[:30000]}]  # Fallback
                }
            ]
        }


class PDFAnalyzer:
    """Advanced PDF content analyzer."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.raw_content = ""
        self.pages = []
    
    def extract_content(self) -> bool:
        """Extract content from PDF with page tracking."""
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                
                print(f"📄 PDF: {Path(self.pdf_path).name}")
                print(f"   Pages: {num_pages}")
                
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    
                    self.pages.append({
                        'number': page_num + 1,
                        'text': text,
                        'char_count': len(text)
                    })
                    self.raw_content += f"\n{text}"
                
                total_chars = sum(p['char_count'] for p in self.pages)
                print(f"   Characters: {total_chars:,}")
                return True
                
        except Exception as e:
            print(f"❌ PDF extraction failed: {str(e)}")
            return False
    
    def detect_structure(self) -> List[Dict]:
        """Detect document structure based on headings and content patterns."""
        sections = []
        current_section = None
        
        lines = self.raw_content.split('\n')
        
        # Patterns for detecting headings
        heading_patterns = [
            (r'^(\d+\.)+\s+[A-Z]', 'numbered'),           # 1.2.3 Heading
            (r'^[A-Z][A-Z\s]{5,}$', 'uppercase'),         # ALL CAPS
            (r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$', 'title'),  # Title Case
            (r'^\*\*.*\*\*$', 'bold'),                     # **Bold**
        ]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this looks like a heading
            is_heading = False
            for pattern, style in heading_patterns:
                if re.match(pattern, line) and len(line) < 120:
                    is_heading = True
                    
                    # Save previous section
                    if current_section and current_section['content'].strip():
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        'title': line,
                        'style': style,
                        'content': '',
                        'word_count': 0
                    }
                    break
            
            if not is_heading and current_section is not None:
                current_section['content'] += line + '\n'
                current_section['word_count'] = len(current_section['content'].split())
        
        # Add final section
        if current_section and current_section['content'].strip():
            sections.append(current_section)
        
        print(f"📑 Detected {len(sections)} sections")
        return sections


class TaskGenerator:
    """Generates well-structured Jira tasks from content."""
    
    @staticmethod
    def from_sections(sections: List[Dict], max_words: int = 500) -> List[Dict]:
        """Generate tasks from detected sections."""
        tasks = []
        
        for section in sections:
            title = section['title']
            content = section['content'].strip()
            word_count = section['word_count']
            
            # Skip tiny sections
            if word_count < 30:
                continue
            
            # Clean title
            title = re.sub(r'^[\d\.]+\s*', '', title)  # Remove numbering
            title = title.strip()[:100]
            
            # Split large sections
            if word_count > max_words:
                chunks = TaskGenerator._split_content(content, max_words)
                for i, chunk in enumerate(chunks, 1):
                    tasks.append({
                        'summary': f"{title} - Part {i}/{len(chunks)}",
                        'description': f"Section: {section['title']}\n\n{chunk}",
                        'type': 'Task'
                    })
            else:
                tasks.append({
                    'summary': title,
                    'description': f"Section: {section['title']}\n\n{content}",
                    'type': 'Task'
                })
        
        return tasks
    
    @staticmethod
    def _split_content(text: str, max_words: int) -> List[str]:
        """Split content into chunks at sentence boundaries."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_words = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            if current_words + sentence_words > max_words and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_words = sentence_words
            else:
                current_chunk.append(sentence)
                current_words += sentence_words
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    @staticmethod
    def from_raw_content(content: str, num_tasks: int = 10) -> List[Dict]:
        """Generate tasks from raw content without structure detection."""
        words = content.split()
        words_per_task = max(len(words) // num_tasks, 100)
        
        tasks = []
        current_words = []
        task_num = 1
        
        for word in words:
            current_words.append(word)
            
            if len(current_words) >= words_per_task and word.endswith('.'):
                task_content = ' '.join(current_words)
                first_sentence = task_content.split('.')[0][:80]
                
                tasks.append({
                    'summary': f"Requirement {task_num}: {first_sentence}",
                    'description': task_content,
                    'type': 'Task'
                })
                
                current_words = []
                task_num += 1
                
                if task_num > num_tasks:
                    break
        
        # Add remaining
        if current_words and task_num <= num_tasks:
            task_content = ' '.join(current_words)
            first_sentence = task_content.split('.')[0][:80]
            tasks.append({
                'summary': f"Requirement {task_num}: {first_sentence}",
                'description': task_content,
                'type': 'Task'
            })
        
        return tasks


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description='Create Jira tasks from PDF requirements')
    parser.add_argument('--config', default='config.json', help='Config file path')
    parser.add_argument('--pdf', help='PDF file path (overrides config)')
    parser.add_argument('--dry-run', action='store_true', help='Preview tasks without creating')
    parser.add_argument('--max-tasks', type=int, help='Maximum number of tasks to create')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print(" PDF to Jira Requirements Import")
    print("=" * 70)
    
    # Load configuration
    config = Config.load_config(args.config)
    if not config:
        print("❌ Could not load configuration")
        return 1
    
    # Override PDF path if provided
    if args.pdf:
        config.setdefault('pdf', {})['path'] = args.pdf
    
    pdf_path = config.get('pdf', {}).get('path')
    if not pdf_path or not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return 1
    
    # Initialize Jira client
    print("\n[1/5] Connecting to Jira...")
    jira = JiraClient(config)
    
    if not jira.validate_config():
        return 1
    
    success, user_info = jira.test_connection()
    if not success:
        return 1
    
    print(f"✓ Connected as: {user_info.get('displayName', jira.email)}")
    
    # Verify project
    project = jira.get_project()
    if not project:
        print("\n📋 Available projects:")
        projects = jira.list_projects()
        for p in projects[:10]:
            print(f"  - {p.get('key')}: {p.get('name')}")
        return 1
    
    print(f"✓ Project: {project.get('name')} ({project.get('key')})")
    
    # Extract PDF content
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
        target = args.max_tasks or config.get('task_settings', {}).get('target_tasks', 15)
        tasks = TaskGenerator.from_raw_content(analyzer.raw_content, target)
        print(f"✓ Generated {len(tasks)} tasks from content analysis")
    
    if args.max_tasks:
        tasks = tasks[:args.max_tasks]
        print(f"  Limited to {len(tasks)} tasks")
    
    # Preview or create
    if args.dry_run:
        print(f"\n[DRY RUN] Would create {len(tasks)} tasks:")
        for i, task in enumerate(tasks[:5], 1):
            print(f"\n  {i}. {task['summary']}")
            print(f"     Description: {task['description'][:100]}...")
        if len(tasks) > 5:
            print(f"\n  ... and {len(tasks) - 5} more tasks")
        return 0
    
    # Create in Jira
    print(f"\n[5/5] Creating {len(tasks)} tasks in Jira...")
    print("-" * 70)
    
    created = []
    failed = []
    
    for i, task in enumerate(tasks, 1):
        print(f"[{i}/{len(tasks)}] ", end='')
        
        issue_key = jira.create_issue(
            summary=task['summary'],
            description=task['description']
        )
        
        if issue_key:
            print(f"✓ {issue_key}: {task['summary'][:50]}")
            created.append(issue_key)
        else:
            failed.append(task)
        
        # Rate limiting
        if i % 10 == 0:
            import time
            time.sleep(1)
    
    # Summary
    print("\n" + "=" * 70)
    print(" SUMMARY")
    print("=" * 70)
    print(f"✓ Created: {len(created)} tasks")
    print(f"✗ Failed:  {len(failed)} tasks")
    
    if created:
        print(f"\n🎉 View tasks: {jira.jira_url}/browse/{created[0]}")
        print(f"\n📋 Created issues:")
        for key in created[:10]:
            print(f"  - {key}")
        if len(created) > 10:
            print(f"  ... and {len(created) - 10} more")
    
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
