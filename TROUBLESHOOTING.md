# Troubleshooting Guide

## Common Errors and Solutions

### 1. "Cannot reach Jira server" / DNS Resolution Error

**Error Messages:**
- `Failed to resolve 'yourcompany.atlassian.net'`
- `Name or service not known`
- `HTTPSConnectionPool: Max retries exceeded`

**Causes:**
- Incorrect Jira URL
- Typo in the domain name
- Network connectivity issues

**Solutions:**
✅ **Check your Jira URL format:**
- Correct: `https://yourcompany.atlassian.net`
- Incorrect: `yourcompany.atlassian.net` (missing https://)
- Incorrect: `https://yourcompany.atlassian.com` (wrong TLD)
- Incorrect: `https://www.atlassian.net/yourcompany` (wrong format)

✅ **Verify the URL in your browser:**
1. Open a new browser tab
2. Paste your Jira URL
3. Make sure it loads your Jira login page
4. Copy the exact URL from the browser

✅ **Check your internet connection:**
```bash
# Test if you can reach Jira
ping yourcompany.atlassian.net
```

---

### 2. "Authentication failed" / 401 Unauthorized

**Error Messages:**
- `401 Unauthorized`
- `Authentication failed`
- `Invalid credentials`

**Causes:**
- Incorrect email address
- Invalid or expired API token
- Wrong Atlassian account

**Solutions:**
✅ **Verify your email:**
- Use the email address you log into Jira with
- Must match your Atlassian account email exactly

✅ **Generate a new API token:**
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "PDF to Jira App")
4. Copy the token immediately (you won't see it again!)
5. Paste it into the application

✅ **Check token hasn't expired:**
- API tokens don't expire by default
- But they can be revoked manually
- Generate a fresh token if unsure

---

### 3. "Project not found" / 404 Error

**Error Messages:**
- `Project 'XYZ' not found`
- `404 Not Found`
- `Connected but project not found`

**Causes:**
- Wrong project key
- No access to the project
- Case sensitivity issue

**Solutions:**
✅ **Find your correct project key:**
1. Log into Jira
2. Go to your project
3. Look at the URL: `https://company.atlassian.net/browse/PROJ`
4. The project key is `PROJ` (after /browse/)
5. Or look for the prefix on issue numbers (e.g., `PROJ-123`)

✅ **Check project access:**
- Make sure you're a member of the project
- You need at least "Create Issues" permission
- Ask your Jira admin if unsure

✅ **Project key is case-sensitive:**
- `PROJ` ≠ `proj` ≠ `Proj`
- Use exact uppercase/lowercase as shown in Jira

---

### 4. "Could not extract text from PDF"

**Error Messages:**
- `Could not extract text from PDF`
- `No text found in PDF`
- `PDF extraction failed`

**Causes:**
- PDF contains only images (scanned document)
- PDF is encrypted/password protected
- Corrupted PDF file

**Solutions:**
✅ **Check if PDF has selectable text:**
1. Open PDF in a viewer
2. Try to select and copy text
3. If you can't select text, it's image-based

✅ **For image-based PDFs:**
- Use OCR software to convert to text-based PDF
- Try Adobe Acrobat's OCR feature
- Use online OCR tools

✅ **For encrypted PDFs:**
- Remove password protection first
- Use Adobe Acrobat or similar tool
- Re-save as unprotected PDF

✅ **Try a different PDF:**
- Test with a simple PDF to rule out file corruption
- Create a test PDF from Word/Google Docs

---

### 5. File Upload Errors

**Error Messages:**
- `File too large`
- `Invalid file type`
- `No file selected`

**Solutions:**
✅ **File size limit: 16MB**
- Compress large PDFs
- Split into multiple smaller PDFs
- Remove unnecessary images/pages

✅ **Only PDF files accepted:**
- Must be `.pdf` extension
- Word docs (.docx) won't work
- Images (.jpg, .png) won't work

✅ **Select a file:**
- Click the upload area or drag & drop
- Wait for "Selected: filename.pdf" confirmation

---

### 6. Network/Timeout Errors

**Error Messages:**
- `Connection timeout`
- `Request timeout`
- `Network error`

**Causes:**
- Slow internet connection
- Jira server is slow/down
- Processing large PDF

**Solutions:**
✅ **Check Atlassian Status:**
- Visit: https://status.atlassian.com/
- See if there are any outages

✅ **Retry the operation:**
- Wait a moment and try again
- Large PDFs may take longer

✅ **Try fewer tasks:**
- Set "Maximum Tasks" to 5-10 for testing
- Process in smaller batches

---

## Testing Connection

Before processing PDFs, always test your connection:

1. Fill in all Jira configuration fields
2. Click "Test Connection" button
3. Wait for success message
4. If successful, you'll see: ✓ Connected successfully as [Your Name] to project [Project Name]

## Preview Mode

Use preview mode to test without creating tasks:

1. ✅ Check "Preview Only (Don't create tasks)"
2. Upload your PDF
3. Click "Process PDF & Create Tasks"
4. Review what would be created
5. If satisfied, uncheck preview and run again

## Getting Help

### Check Browser Console
1. Press F12 (or Cmd+Option+I on Mac)
2. Click "Console" tab
3. Look for error messages
4. Share these if asking for help

### Check Application Logs
If self-hosting:
1. Look at terminal/console where app is running
2. Check for error stack traces
3. Note any specific error messages

### Verify Prerequisites
- ✅ Valid Jira Cloud account
- ✅ API token generated
- ✅ Project exists and you have access
- ✅ "Create Issues" permission in project
- ✅ Text-based PDF file

## Still Having Issues?

1. **Start fresh:**
   - Clear browser cache
   - Generate new API token
   - Try with a simple test PDF

2. **Test with curl:**
   ```bash
   curl -u your.email@company.com:YOUR_API_TOKEN \
     https://yourcompany.atlassian.net/rest/api/3/myself
   ```
   Should return your user info if credentials are correct

3. **Common mistakes checklist:**
   - [ ] URL includes `https://`
   - [ ] Email is correct Atlassian account
   - [ ] API token is fresh and copied correctly
   - [ ] Project key matches exactly (case-sensitive)
   - [ ] You have project access
   - [ ] PDF has selectable text
   - [ ] PDF is under 16MB

## Quick Fix Reference

| Error | Quick Fix |
|-------|-----------|
| DNS/Cannot reach | Check URL format, add `https://` |
| 401 Unauthorized | Generate fresh API token |
| 404 Project not found | Verify project key, check access |
| No text in PDF | Use text-based PDF, not scanned image |
| File too large | Compress or split PDF |
| Timeout | Try with fewer tasks, check network |

---

**Remember:** Most issues are due to incorrect URLs, credentials, or project keys. Double-check these first! ✅
