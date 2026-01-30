#!/usr/bin/env python3
"""
PDF to Jira - GUI Application
Standalone GUI for importing PDF requirements into Jira.
"""

import os
import sys
import json
import threading
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import Optional, Dict

# Import our existing modules
from pdf_to_jira_advanced import JiraClient, PDFAnalyzer, TaskGenerator


class PDFToJiraGUI:
    """GUI Application for PDF to Jira import."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Jira Task Importer")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.pdf_path = StringVar()
        self.jira_url = StringVar(value="https://mdnoorishah.atlassian.net")
        self.jira_email = StringVar(value="mdnoorishah@gmail.com")
        self.jira_token = StringVar()
        self.project_key = StringVar(value="KAN")
        self.max_tasks = StringVar(value="")
        self.issue_type = StringVar(value="Task")
        self.priority = StringVar(value="Medium")
        self.labels = StringVar(value="pdf-import,requirements")
        
        # State
        self.jira_client: Optional[JiraClient] = None
        self.is_processing = False
        
        # Load saved config
        self.load_config()
        
        # Build UI
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(N, W, E, S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Title
        title = ttk.Label(main_frame, text="📄 PDF to Jira Task Importer", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # PDF Selection Section
        self.create_section_header(main_frame, row, "1. Select PDF File")
        row += 1
        
        ttk.Label(main_frame, text="PDF File:").grid(row=row, column=0, sticky=W, pady=5)
        pdf_entry = ttk.Entry(main_frame, textvariable=self.pdf_path, width=50)
        pdf_entry.grid(row=row, column=1, sticky=(W, E), pady=5, padx=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse...", command=self.browse_pdf)
        browse_btn.grid(row=row, column=2, pady=5)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient=HORIZONTAL).grid(row=row, column=0, 
                                                          columnspan=3, sticky=(W, E), pady=15)
        row += 1
        
        # Jira Configuration Section
        self.create_section_header(main_frame, row, "2. Jira Configuration")
        row += 1
        
        # Jira URL
        ttk.Label(main_frame, text="Jira URL:").grid(row=row, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.jira_url, width=50).grid(
            row=row, column=1, columnspan=2, sticky=(W, E), pady=5, padx=5)
        row += 1
        
        # Email
        ttk.Label(main_frame, text="Email:").grid(row=row, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.jira_email, width=50).grid(
            row=row, column=1, columnspan=2, sticky=(W, E), pady=5, padx=5)
        row += 1
        
        # API Token
        ttk.Label(main_frame, text="API Token:").grid(row=row, column=0, sticky=W, pady=5)
        token_entry = ttk.Entry(main_frame, textvariable=self.jira_token, 
                               width=50, show="*")
        token_entry.grid(row=row, column=1, columnspan=2, sticky=(W, E), pady=5, padx=5)
        row += 1
        
        # Test Connection Button
        test_btn = ttk.Button(main_frame, text="Test Connection", 
                             command=self.test_connection)
        test_btn.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        row += 1
        
        # Project Key
        ttk.Label(main_frame, text="Project Key:").grid(row=row, column=0, sticky=W, pady=5)
        project_frame = ttk.Frame(main_frame)
        project_frame.grid(row=row, column=1, columnspan=2, sticky=(W, E), pady=5, padx=5)
        
        ttk.Entry(project_frame, textvariable=self.project_key, width=15).pack(side=LEFT)
        ttk.Button(project_frame, text="List Projects", 
                  command=self.list_projects).pack(side=LEFT, padx=5)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient=HORIZONTAL).grid(row=row, column=0, 
                                                          columnspan=3, sticky=(W, E), pady=15)
        row += 1
        
        # Task Settings Section
        self.create_section_header(main_frame, row, "3. Task Settings")
        row += 1
        
        # Issue Type
        ttk.Label(main_frame, text="Issue Type:").grid(row=row, column=0, sticky=W, pady=5)
        issue_combo = ttk.Combobox(main_frame, textvariable=self.issue_type, 
                                   values=["Task", "Story", "Bug", "Epic"], width=15)
        issue_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        row += 1
        
        # Priority
        ttk.Label(main_frame, text="Priority:").grid(row=row, column=0, sticky=W, pady=5)
        priority_combo = ttk.Combobox(main_frame, textvariable=self.priority, 
                                      values=["Highest", "High", "Medium", "Low", "Lowest"], 
                                      width=15)
        priority_combo.grid(row=row, column=1, sticky=W, pady=5, padx=5)
        row += 1
        
        # Labels
        ttk.Label(main_frame, text="Labels:").grid(row=row, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.labels, width=30).grid(
            row=row, column=1, sticky=W, pady=5, padx=5)
        ttk.Label(main_frame, text="(comma-separated)", 
                 font=('Arial', 8)).grid(row=row, column=2, sticky=W)
        row += 1
        
        # Max Tasks
        ttk.Label(main_frame, text="Max Tasks:").grid(row=row, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.max_tasks, width=15).grid(
            row=row, column=1, sticky=W, pady=5, padx=5)
        ttk.Label(main_frame, text="(leave empty for auto)", 
                 font=('Arial', 8)).grid(row=row, column=2, sticky=W)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient=HORIZONTAL).grid(row=row, column=0, 
                                                          columnspan=3, sticky=(W, E), pady=15)
        row += 1
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=10)
        
        self.preview_btn = ttk.Button(button_frame, text="Preview Tasks", 
                                      command=self.preview_tasks, width=15)
        self.preview_btn.pack(side=LEFT, padx=5)
        
        self.import_btn = ttk.Button(button_frame, text="Import to Jira", 
                                     command=self.import_to_jira, width=15)
        self.import_btn.pack(side=LEFT, padx=5)
        
        save_btn = ttk.Button(button_frame, text="Save Config", 
                             command=self.save_config, width=15)
        save_btn.pack(side=LEFT, padx=5)
        row += 1
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, columnspan=3, sticky=(W, E), pady=10)
        row += 1
        
        # Output Log
        ttk.Label(main_frame, text="Output Log:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=W, pady=(10, 5))
        row += 1
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=12, width=70)
        self.log_text.grid(row=row, column=0, columnspan=3, sticky=(W, E, N, S), pady=5)
        main_frame.rowconfigure(row, weight=1)
        row += 1
        
        # Status Bar
        self.status = StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status, 
                              relief=SUNKEN, anchor=W)
        status_bar.grid(row=row, column=0, columnspan=3, sticky=(W, E))
    
    def create_section_header(self, parent, row, text):
        """Create a section header label."""
        label = ttk.Label(parent, text=text, font=('Arial', 11, 'bold'))
        label.grid(row=row, column=0, columnspan=3, sticky=W, pady=(10, 5))
    
    def browse_pdf(self):
        """Open file dialog to select PDF."""
        filename = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
            initialdir=str(Path(__file__).parent)
        )
        if filename:
            self.pdf_path.set(filename)
            self.log(f"Selected PDF: {Path(filename).name}")
    
    def log(self, message: str, level: str = "INFO"):
        """Add message to log."""
        prefix = {"INFO": "ℹ️", "SUCCESS": "✓", "ERROR": "✗", "WARNING": "⚠️"}.get(level, "•")
        self.log_text.insert(END, f"{prefix} {message}\n")
        self.log_text.see(END)
        self.root.update_idletasks()
    
    def set_status(self, message: str):
        """Update status bar."""
        self.status.set(message)
        self.root.update_idletasks()
    
    def get_config(self) -> Dict:
        """Get current configuration as dict."""
        return {
            "jira": {
                "url": self.jira_url.get().strip(),
                "email": self.jira_email.get().strip(),
                "api_token": self.jira_token.get().strip(),
                "project_key": self.project_key.get().strip()
            },
            "pdf": {
                "path": self.pdf_path.get().strip()
            },
            "task_settings": {
                "issue_type": self.issue_type.get(),
                "priority": self.priority.get(),
                "add_labels": [l.strip() for l in self.labels.get().split(',') if l.strip()],
                "target_tasks": int(self.max_tasks.get()) if self.max_tasks.get().strip() else 15
            }
        }
    
    def load_config(self):
        """Load configuration from file."""
        config_path = Path(__file__).parent.parent / "config.json"
        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
                jira_config = config.get('jira', {})
                self.jira_url.set(jira_config.get('url', ''))
                self.jira_email.set(jira_config.get('email', ''))
                self.jira_token.set(jira_config.get('api_token', ''))
                self.project_key.set(jira_config.get('project_key', ''))
                
                pdf_config = config.get('pdf', {})
                self.pdf_path.set(pdf_config.get('path', ''))
                
                task_settings = config.get('task_settings', {})
                self.issue_type.set(task_settings.get('issue_type', 'Task'))
                self.priority.set(task_settings.get('priority', 'Medium'))
                labels = task_settings.get('add_labels', [])
                self.labels.set(','.join(labels))
                
        except Exception as e:
            pass  # Silent fail, use defaults
    
    def save_config(self):
        """Save configuration to file."""
        config_path = Path(__file__).parent.parent / "config.json"
        try:
            config = self.get_config()
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log("Configuration saved", "SUCCESS")
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            self.log(f"Failed to save config: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
    
    def validate_inputs(self) -> bool:
        """Validate all required inputs."""
        if not self.pdf_path.get().strip():
            messagebox.showerror("Error", "Please select a PDF file")
            return False
        
        if not Path(self.pdf_path.get()).exists():
            messagebox.showerror("Error", "Selected PDF file does not exist")
            return False
        
        if not self.jira_url.get().strip():
            messagebox.showerror("Error", "Please enter Jira URL")
            return False
        
        if not self.jira_email.get().strip():
            messagebox.showerror("Error", "Please enter email")
            return False
        
        if not self.jira_token.get().strip():
            messagebox.showerror("Error", "Please enter API token")
            return False
        
        if not self.project_key.get().strip():
            messagebox.showerror("Error", "Please enter project key")
            return False
        
        return True
    
    def test_connection(self):
        """Test Jira connection."""
        if not all([self.jira_url.get(), self.jira_email.get(), self.jira_token.get()]):
            messagebox.showerror("Error", "Please fill in Jira URL, email, and API token")
            return
        
        self.log("Testing Jira connection...")
        self.set_status("Testing connection...")
        
        try:
            config = self.get_config()
            jira = JiraClient(config)
            
            success, user_info = jira.test_connection()
            if success:
                self.log(f"Connected as: {user_info.get('displayName', 'User')}", "SUCCESS")
                messagebox.showinfo("Success", 
                    f"Connected to Jira!\n\nUser: {user_info.get('displayName', 'Unknown')}")
                self.set_status("Connection successful")
                self.jira_client = jira
            else:
                self.log("Connection failed", "ERROR")
                messagebox.showerror("Error", "Failed to connect to Jira. Check credentials.")
                self.set_status("Connection failed")
        except Exception as e:
            self.log(f"Connection error: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Connection error:\n{str(e)}")
            self.set_status("Error")
    
    def list_projects(self):
        """List available Jira projects."""
        if not self.jira_client:
            messagebox.showinfo("Info", "Please test connection first")
            return
        
        try:
            projects = self.jira_client.list_projects()
            if projects:
                project_list = "\n".join([f"• {p.get('key')}: {p.get('name')}" 
                                         for p in projects[:20]])
                messagebox.showinfo("Available Projects", 
                    f"Projects you have access to:\n\n{project_list}")
            else:
                messagebox.showinfo("No Projects", "No projects found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list projects:\n{str(e)}")
    
    def preview_tasks(self):
        """Preview tasks that would be created."""
        if not self.validate_inputs():
            return
        
        self.set_buttons_state(False)
        self.progress.start()
        self.log_text.delete(1.0, END)
        self.log("Starting task preview...")
        
        # Run in background thread
        thread = threading.Thread(target=self._preview_tasks_thread)
        thread.daemon = True
        thread.start()
    
    def _preview_tasks_thread(self):
        """Background thread for preview."""
        try:
            # Analyze PDF
            self.log(f"Analyzing PDF: {Path(self.pdf_path.get()).name}")
            analyzer = PDFAnalyzer(self.pdf_path.get())
            
            if not analyzer.extract_content():
                self.log("Failed to extract PDF content", "ERROR")
                return
            
            self.log(f"Extracted {len(analyzer.raw_content)} characters from {len(analyzer.pages)} pages")
            
            # Detect structure
            sections = analyzer.detect_structure()
            self.log(f"Detected {len(sections)} sections")
            
            # Generate tasks
            if sections and len(sections) > 2:
                tasks = TaskGenerator.from_sections(sections)
            else:
                target = int(self.max_tasks.get()) if self.max_tasks.get().strip() else 15
                tasks = TaskGenerator.from_raw_content(analyzer.raw_content, target)
            
            if self.max_tasks.get().strip():
                tasks = tasks[:int(self.max_tasks.get())]
            
            self.log(f"\n{'='*60}", "INFO")
            self.log(f"PREVIEW: Would create {len(tasks)} tasks", "SUCCESS")
            self.log(f"{'='*60}\n", "INFO")
            
            for i, task in enumerate(tasks[:10], 1):
                self.log(f"{i}. {task['summary']}")
                self.log(f"   {task['description'][:80]}...\n")
            
            if len(tasks) > 10:
                self.log(f"... and {len(tasks) - 10} more tasks")
            
            self.log(f"\n{'='*60}", "INFO")
            self.log("Preview complete. Click 'Import to Jira' to create tasks.", "SUCCESS")
            
        except Exception as e:
            self.log(f"Preview error: {str(e)}", "ERROR")
        finally:
            self.progress.stop()
            self.set_buttons_state(True)
            self.set_status("Ready")
    
    def import_to_jira(self):
        """Import tasks to Jira."""
        if not self.validate_inputs():
            return
        
        # Confirm action
        if not messagebox.askyesno("Confirm Import", 
            "This will create tasks in Jira.\n\nContinue?"):
            return
        
        self.set_buttons_state(False)
        self.progress.start()
        self.log_text.delete(1.0, END)
        self.log("Starting Jira import...")
        
        # Run in background thread
        thread = threading.Thread(target=self._import_to_jira_thread)
        thread.daemon = True
        thread.start()
    
    def _import_to_jira_thread(self):
        """Background thread for import."""
        created = []
        failed = []
        
        try:
            # Initialize Jira client
            config = self.get_config()
            jira = JiraClient(config)
            
            self.log("Connecting to Jira...")
            success, user_info = jira.test_connection()
            if not success:
                self.log("Connection failed", "ERROR")
                return
            
            self.log(f"Connected as: {user_info.get('displayName')}", "SUCCESS")
            
            # Verify project
            project = jira.get_project()
            if not project:
                self.log(f"Project '{jira.project_key}' not found", "ERROR")
                return
            
            self.log(f"Project: {project.get('name')}", "SUCCESS")
            
            # Analyze PDF
            self.log(f"\nAnalyzing PDF...")
            analyzer = PDFAnalyzer(self.pdf_path.get())
            
            if not analyzer.extract_content():
                self.log("Failed to extract PDF content", "ERROR")
                return
            
            # Detect structure and generate tasks
            sections = analyzer.detect_structure()
            
            if sections and len(sections) > 2:
                tasks = TaskGenerator.from_sections(sections)
            else:
                target = int(self.max_tasks.get()) if self.max_tasks.get().strip() else 15
                tasks = TaskGenerator.from_raw_content(analyzer.raw_content, target)
            
            if self.max_tasks.get().strip():
                tasks = tasks[:int(self.max_tasks.get())]
            
            self.log(f"\nCreating {len(tasks)} tasks in Jira...")
            self.log(f"{'='*60}\n")
            
            # Create tasks
            labels = [l.strip() for l in self.labels.get().split(',') if l.strip()]
            
            for i, task in enumerate(tasks, 1):
                issue_key = jira.create_issue(
                    summary=task['summary'],
                    description=task['description'],
                    issue_type=self.issue_type.get(),
                    labels=labels,
                    priority=self.priority.get()
                )
                
                if issue_key:
                    self.log(f"[{i}/{len(tasks)}] Created {issue_key}: {task['summary'][:50]}", "SUCCESS")
                    created.append(issue_key)
                else:
                    self.log(f"[{i}/{len(tasks)}] Failed: {task['summary'][:50]}", "ERROR")
                    failed.append(task)
                
                # Small delay for rate limiting
                if i % 10 == 0:
                    import time
                    time.sleep(1)
            
            # Summary
            self.log(f"\n{'='*60}")
            self.log(f"IMPORT COMPLETE", "SUCCESS")
            self.log(f"{'='*60}")
            self.log(f"✓ Created: {len(created)} tasks")
            self.log(f"✗ Failed:  {len(failed)} tasks")
            
            if created:
                self.log(f"\nView in Jira: {jira.jira_url}/browse/{created[0]}")
                messagebox.showinfo("Success!", 
                    f"Created {len(created)} tasks!\n\nFirst task: {created[0]}")
            
        except Exception as e:
            self.log(f"Import error: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Import failed:\n{str(e)}")
        finally:
            self.progress.stop()
            self.set_buttons_state(True)
            self.set_status(f"Completed: {len(created)} created, {len(failed)} failed")
    
    def set_buttons_state(self, enabled: bool):
        """Enable or disable action buttons."""
        state = NORMAL if enabled else DISABLED
        self.preview_btn.config(state=state)
        self.import_btn.config(state=state)


def main():
    """Main entry point."""
    root = Tk()
    app = PDFToJiraGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
