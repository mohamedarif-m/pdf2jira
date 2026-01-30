# PDF to Jira Web Application 🚀

A modern web application that converts PDF requirement documents into Jira tasks automatically.

## 🌟 Features

- **Web-Based Interface**: No installation required, access from any browser
- **Drag & Drop Upload**: Easy PDF file upload with drag and drop support
- **Jira Integration**: Direct connection to your Jira instance
- **Test Connection**: Verify your Jira credentials before processing
- **Preview Mode**: See what tasks will be created before committing
- **Real-Time Progress**: Visual feedback during processing
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Secure**: Credentials are never stored on the server

## 🚀 Quick Start

### Option 1: Run Locally

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the App**
   - Open your browser to: http://localhost:5000

### Option 2: Deploy to Render (Recommended)

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for complete deployment instructions.

**Quick Steps:**
1. Push your code to GitHub
2. Connect to Render
3. Deploy with one click
4. Your app is live!

## 📋 How to Use

1. **Upload PDF**
   - Click or drag & drop your PDF requirements document

2. **Configure Jira**
   - Enter your Jira URL (e.g., `https://yourcompany.atlassian.net`)
   - Enter your email
   - Enter your API token ([Generate here](https://id.atlassian.com/manage-profile/security/api-tokens))
   - Enter your project key (e.g., `PROJ`)
   - Click "Test Connection" to verify

3. **Configure Task Settings**
   - Select issue type (Task, Story, Bug, Epic)
   - Choose priority level
   - Add labels (comma-separated)
   - Set max tasks (optional)
   - Enable "Preview Only" to test without creating tasks

4. **Process**
   - Click "Process PDF & Create Tasks"
   - View results with direct links to created Jira tasks

## 🔧 Configuration

### Environment Variables

Set these in production (Render dashboard):

- `SECRET_KEY`: Flask session secret (auto-generated if not set)
- `PORT`: Port number (default: 5000)

### File Structure

```
.
├── app.py                      # Main Flask application
├── templates/
│   └── index.html              # Web interface
├── pdf_to_jira_advanced.py     # PDF processing logic
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
├── runtime.txt                 # Python version
├── .gitignore                  # Git ignore rules
└── RENDER_DEPLOYMENT.md        # Deployment guide
```

## 🛠️ Technical Stack

- **Backend**: Flask 3.0
- **PDF Processing**: PyPDF2
- **HTTP Client**: Requests
- **Production Server**: Gunicorn
- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)

## 📊 API Endpoints

### `POST /api/test-connection`
Test Jira credentials and project access.

**Request:**
```json
{
  "jira_url": "https://company.atlassian.net",
  "jira_email": "user@company.com",
  "jira_token": "your-api-token",
  "project_key": "PROJ"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Connected successfully as John Doe",
  "user": "John Doe",
  "project": "Project Name"
}
```

### `POST /api/upload`
Upload PDF and create Jira tasks.

**Request:** Multipart form data with:
- `pdf_file`: PDF file
- `jira_url`, `jira_email`, `jira_token`, `project_key`: Jira config
- `issue_type`, `priority`, `labels`: Task settings
- `max_tasks`: Optional limit
- `dry_run`: Preview mode flag

**Response:**
```json
{
  "success": true,
  "total_tasks": 5,
  "created": 5,
  "failed": 0,
  "message": "Created 5 of 5 tasks",
  "tasks": [
    {
      "summary": "Task title",
      "issue_key": "PROJ-123",
      "status": "created",
      "url": "https://company.atlassian.net/browse/PROJ-123"
    }
  ]
}
```

### `GET /health`
Health check endpoint for monitoring.

## 🔒 Security

- ✅ API tokens never stored on server
- ✅ HTTPS enforced in production (via Render)
- ✅ Secure file upload handling
- ✅ File size limits (16MB max)
- ✅ File type validation
- ✅ Session security with secret key

## 🐛 Troubleshooting

### "Connection Failed"
- Verify Jira URL is correct (include `https://`)
- Check API token is valid
- Ensure email matches Jira account

### "Project Not Found"
- Verify project key is correct (case-sensitive)
- Ensure you have access to the project

### "Could Not Extract Text"
- PDF might be image-based (needs OCR)
- PDF might be encrypted
- Try with a different PDF

### Upload Fails
- Check file size (max 16MB)
- Ensure file is actually a PDF
- Check browser console for errors

## 🚀 Deployment

### Render (Recommended)
1. Follow [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
2. Free tier available
3. Automatic HTTPS
4. Easy GitHub integration

### Other Platforms
The app is compatible with:
- **Heroku**: Use Procfile and runtime.txt
- **Railway**: Auto-detected Flask app
- **Google Cloud Run**: Add Dockerfile
- **AWS Elastic Beanstalk**: Use eb cli

## 📝 Development

### Local Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in debug mode
export FLASK_DEBUG=1
python app.py
```

### Testing
```bash
# Test with preview mode enabled
# Upload a PDF and check "Preview Only"

# Test connection before processing
# Click "Test Connection" button
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and commercial use.

## 🆘 Support

For issues or questions:
1. Check the [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) guide
2. Review error messages in browser console
3. Check Render logs (if deployed)
4. Verify Jira credentials and permissions

## 🎉 Success!

Your PDF to Jira web application is ready to use! Enjoy automating your requirement imports.

---

**Note**: This is the web version. For desktop GUI, see `pdf_to_jira_gui.py`. For command-line, see `pdf_to_jira_advanced.py`.
