#!/usr/bin/env python3
"""
PDF to Jira - Web Application
Flask web app for importing PDF requirements into Jira.
"""

import os
import json
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import secrets
import requests
from typing import List, Dict

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not installed. AI-powered task generation will not be available.")
    print("   Install with: pip install openai")

# Import existing modules
from pdf_to_jira_advanced import JiraClient, PDFAnalyzer, TaskGenerator


class OllamaTaskGenerator:
    """Local AI-powered task generator using Ollama (FREE)."""
    
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def is_available(self) -> bool:
        """Check if Ollama is running locally."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate_tasks(self, content: str, max_tasks: int = 10) -> List[Dict]:
        """Generate intelligent tasks from PDF content using Ollama."""
        if not self.is_available():
            return []
        
        try:
            prompt = f"""You are a requirements analyst. Analyze the following content from a requirements document and break it down into clear, actionable Jira tasks.

For each task:
1. Create a clear, concise summary (max 100 characters)
2. Provide a detailed description with all relevant information
3. Aim to create {max_tasks} tasks

Return the tasks as a JSON array with this structure:
[{{"summary": "Task summary", "description": "Detailed description"}}]

Content:
{content[:3000]}

Return ONLY the JSON array, no other text."""
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"Ollama error: {response.status_code}")
                return []
            
            result = response.json()
            generated_text = result.get('response', '')
            
            # Try to parse JSON from response
            try:
                # Clean up the response
                if generated_text.startswith('```json'):
                    generated_text = generated_text[7:-3].strip()
                elif generated_text.startswith('```'):
                    generated_text = generated_text[3:-3].strip()
                
                tasks = json.loads(generated_text)
                return tasks if isinstance(tasks, list) else []
            except json.JSONDecodeError:
                print(f"Failed to parse Ollama response as JSON")
                return []
            
        except requests.exceptions.Timeout:
            print("Ollama request timed out")
            return []
        except Exception as e:
            print(f"Ollama task generation error: {str(e)}")
            return []


class AITaskGenerator:
    """AI-powered task generator using OpenAI."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.client = None
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def is_available(self) -> bool:
        """Check if AI task generation is available."""
        return OPENAI_AVAILABLE and self.client is not None
    
    def generate_tasks(self, content: str, max_tasks: int = 10) -> List[Dict]:
        """Generate intelligent tasks from PDF content using AI."""
        if not self.is_available():
            return []
        
        try:
            prompt = f"""You are a requirements analyst. Analyze the following content from a requirements document and break it down into clear, actionable Jira tasks.

For each task:
1. Create a clear, concise summary (max 100 characters)
2. Provide a detailed description with all relevant information
3. Aim to create {max_tasks} tasks

Return the tasks as a JSON array with this structure:
[
  {{
    "summary": "Task summary",
    "description": "Detailed description with all context"
  }}
]

Content:
{content[:4000]}  

Return ONLY the JSON array, no other text."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a requirements analyst that creates well-structured Jira tasks. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            if result.startswith('```json'):
                result = result[7:-3].strip()
            elif result.startswith('```'):
                result = result[3:-3].strip()
            
            tasks = json.loads(result)
            return tasks
            
        except Exception as e:
            print(f"AI task generation error: {str(e)}")
            return []

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/get-projects', methods=['POST'])
def get_projects():
    """Fetch available Jira projects for the user."""
    try:
        data = request.json
        
        # Validate required fields for authentication
        jira_url = data.get('jira_url', '').strip()
        jira_email = data.get('jira_email', '').strip()
        jira_token = data.get('jira_token', '').strip()
        
        if not all([jira_url, jira_email, jira_token]):
            return jsonify({
                'success': False,
                'message': 'Jira URL, email, and API token are required to fetch projects.'
            }), 400
        
        # Create config
        config = {
            'jira': {
                'url': jira_url,
                'email': jira_email,
                'api_token': jira_token,
                'project_key': ''  # Not needed for listing projects
            }
        }
        
        # Get projects
        jira_client = JiraClient(config)
        projects = jira_client.list_projects()
        
        if projects:
            # Format projects for response
            project_list = [
                {
                    'key': p.get('key'),
                    'name': p.get('name'),
                    'id': p.get('id')
                }
                for p in projects
            ]
            
            return jsonify({
                'success': True,
                'projects': project_list,
                'count': len(project_list)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No projects found or unable to fetch projects. Please check your credentials.'
            }), 404
            
    except requests.exceptions.ConnectionError as e:
        return jsonify({
            'success': False,
            'message': 'Cannot connect to Jira. Please check the URL and your internet connection.'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching projects: {str(e)}'
        }), 500


@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Test Jira connection with provided credentials."""
    try:
        data = request.json
        
        # Validate required fields
        jira_url = data.get('jira_url', '').strip()
        jira_email = data.get('jira_email', '').strip()
        jira_token = data.get('jira_token', '').strip()
        project_key = data.get('project_key', '').strip()
        
        if not all([jira_url, jira_email, jira_token, project_key]):
            return jsonify({
                'success': False,
                'message': 'All fields are required. Please fill in Jira URL, email, API token, and project key.'
            }), 400
        
        # Validate URL format
        if not jira_url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'message': 'Jira URL must start with http:// or https://'
            }), 400
        
        # Create config from provided data
        config = {
            'jira': {
                'url': jira_url,
                'email': jira_email,
                'api_token': jira_token,
                'project_key': project_key
            }
        }
        
        # Test connection
        jira_client = JiraClient(config)
        success, user_info = jira_client.test_connection()
        
        if success:
            # Also validate project access
            project = jira_client.get_project()
            if project:
                return jsonify({
                    'success': True,
                    'message': f"✓ Connected successfully as {user_info.get('displayName', 'User')} to project {project.get('name')}",
                    'user': user_info.get('displayName'),
                    'project': project.get('name')
                })
            else:
                return jsonify({
                    'success': False,
                    'message': f"Connected to Jira, but project '{project_key}' not found. Please check the project key is correct and you have access to it."
                }), 404
        else:
            # Provide specific error message based on response
            error_info = user_info or {}
            status_code = error_info.get('status_code', 401)
            
            if status_code == 401:
                message = (
                    "❌ Authentication Failed\n\n"
                    "Your email or API token is incorrect. Please verify:\n"
                    "• Email matches your Atlassian account exactly\n"
                    "• API token is valid and copied correctly\n"
                    "• Generate a new token at: https://id.atlassian.com/manage-profile/security/api-tokens"
                )
            elif status_code == 403:
                message = "❌ Access Denied: You don't have permission to access this Jira instance."
            else:
                message = f"❌ Authentication failed (Error {status_code}). Please check your credentials."
            
            return jsonify({
                'success': False,
                'message': message
            }), status_code
            
    except requests.exceptions.ConnectionError as e:
        error_msg = str(e)
        if 'Failed to resolve' in error_msg or 'Name or service not known' in error_msg:
            return jsonify({
                'success': False,
                'message': f"Cannot reach Jira server. Please check the URL is correct: {data.get('jira_url')}"
            }), 400
        else:
            return jsonify({
                'success': False,
                'message': f"Connection error: Unable to connect to Jira. Please check your network connection and URL."
            }), 500
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'message': 'Connection timeout. Please try again or check if the Jira server is responding.'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Unexpected error: {str(e)}'
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and processing."""
    try:
        # Check if file is in request
        if 'pdf_file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file uploaded'
            }), 400
        
        file = request.files['pdf_file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': 'Only PDF files are allowed'
            }), 400
        
        # Get form data
        jira_url = request.form.get('jira_url')
        jira_email = request.form.get('jira_email')
        jira_token = request.form.get('jira_token')
        project_key = request.form.get('project_key')
        issue_type = request.form.get('issue_type', 'Task')
        priority = request.form.get('priority', 'Medium')
        labels = request.form.get('labels', 'pdf-import,requirements').split(',')
        max_tasks = request.form.get('max_tasks', '')
        dry_run = request.form.get('dry_run', 'false').lower() == 'true'
        use_ai = request.form.get('use_ai', 'false').lower() == 'true'
        ai_provider = request.form.get('ai_provider', 'ollama')  # ollama or openai
        openai_key = request.form.get('openai_key', '')
        ollama_model = request.form.get('ollama_model', 'llama3')
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        try:
            # Create Jira config
            config = {
                'jira': {
                    'url': jira_url,
                    'email': jira_email,
                    'api_token': jira_token,
                    'project_key': project_key
                },
                'task_settings': {
                    'issue_type': issue_type,
                    'priority': priority,
                    'add_labels': [label.strip() for label in labels if label.strip()]
                }
            }
            
            # Analyze PDF
            analyzer = PDFAnalyzer(temp_path)
            
            # Extract content from PDF
            if not analyzer.extract_content():
                return jsonify({
                    'success': False,
                    'message': 'Could not extract text from PDF'
                }), 400
            
            text = analyzer.raw_content
            
            if not text or not text.strip():
                return jsonify({
                    'success': False,
                    'message': 'Could not extract text from PDF'
                }), 400
            
            # Generate tasks from PDF content
            tasks = []
            num_tasks = int(max_tasks) if max_tasks and max_tasks.isdigit() else 10
            
            # Try AI-powered generation first if enabled
            if use_ai:
                if ai_provider == 'ollama':
                    # Use Ollama (free, local)
                    ollama_gen = OllamaTaskGenerator(model=ollama_model)
                    if ollama_gen.is_available():
                        tasks = ollama_gen.generate_tasks(text, num_tasks)
                        if tasks:
                            print(f"✨ Ollama generated {len(tasks)} tasks")
                    else:
                        print("⚠️ Ollama not available. Make sure it's running on localhost:11434")
                        return jsonify({
                            'success': False,
                            'message': 'Ollama is not running. Please start Ollama with: ollama serve'
                        }), 400
                
                elif ai_provider == 'openai' and openai_key:
                    # Use OpenAI (paid)
                    ai_generator = AITaskGenerator(api_key=openai_key)
                    if ai_generator.is_available():
                        tasks = ai_generator.generate_tasks(text, num_tasks)
                        if tasks:
                            print(f"✨ OpenAI generated {len(tasks)} tasks")
            
            # Fallback to traditional methods if AI didn't work
            if not tasks:
                # Try to detect structure first
                sections = analyzer.detect_structure()
                
                if sections and len(sections) > 0:
                    # Use structured approach
                    tasks = TaskGenerator.from_sections(sections)
                else:
                    # Fallback to raw content splitting
                    tasks = TaskGenerator.from_raw_content(text, num_tasks)
            
            if not tasks:
                return jsonify({
                    'success': False,
                    'message': 'Could not generate tasks from PDF content'
                }), 400
            
            # Limit tasks if specified
            if max_tasks and max_tasks.isdigit():
                tasks = tasks[:int(max_tasks)]
            
            results = {
                'total_tasks': len(tasks),
                'tasks': [],
                'created': 0,
                'failed': 0
            }
            
            if dry_run:
                # Preview mode - don't create tasks
                results['tasks'] = [
                    {
                        'summary': task.get('summary', 'No summary'),
                        'description': task.get('description', 'No description')[:200] + '...',
                        'status': 'preview'
                    }
                    for task in tasks
                ]
                results['message'] = f'Preview: {len(tasks)} tasks would be created'
            else:
                # Create tasks in Jira
                jira_client = JiraClient(config)
                
                if not jira_client.validate_config():
                    return jsonify({
                        'success': False,
                        'message': 'Invalid Jira configuration'
                    }), 400
                
                for task in tasks:
                    issue_key = jira_client.create_issue(
                        summary=task.get('summary', 'Untitled Task'),
                        description=task.get('description', ''),
                        issue_type=issue_type,
                        labels=config['task_settings']['add_labels'],
                        priority=priority
                    )
                    
                    if issue_key:
                        results['created'] += 1
                        results['tasks'].append({
                            'summary': task.get('summary'),
                            'issue_key': issue_key,
                            'status': 'created',
                            'url': f"{jira_url}/browse/{issue_key}"
                        })
                    else:
                        results['failed'] += 1
                        results['tasks'].append({
                            'summary': task.get('summary'),
                            'status': 'failed'
                        })
                
                results['message'] = f"Created {results['created']} of {results['total_tasks']} tasks"
            
            return jsonify({
                'success': True,
                **results
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except requests.exceptions.ConnectionError as e:
        error_msg = str(e)
        if 'Failed to resolve' in error_msg or 'Name or service not known' in error_msg:
            return jsonify({
                'success': False,
                'message': f"Cannot reach Jira server at {request.form.get('jira_url')}. Please verify the URL is correct."
            }), 400
        else:
            return jsonify({
                'success': False,
                'message': 'Connection error: Unable to connect to Jira. Please check your network and URL.'
            }), 500
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'message': 'Request timeout. The Jira server is taking too long to respond. Please try again.'
        }), 500
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'message': 'PDF file not found or was deleted during processing.'
        }), 400
    except Exception as e:
        import traceback
        print(f"Error processing PDF: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Error processing PDF: {str(e)}'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
