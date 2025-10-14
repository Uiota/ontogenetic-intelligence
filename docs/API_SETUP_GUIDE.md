# API Setup Guide: Medium & LinkedIn Integration

This guide will help you set up automated posting to your Medium account (`@uniqstic`) and LinkedIn profile for your OGI framework content.

## 🔧 Prerequisites

- Python 3.7+
- Medium account: https://medium.com/@uniqstic
- LinkedIn account: https://www.linkedin.com/in/michael-gibson-216641244/
- GitHub repository: https://github.com/Uiota/ontogenetic-intelligence

## 📝 Medium API Setup

### Step 1: Get Your Integration Token

1. **Go to Medium Settings**: https://medium.com/me/settings
2. **Scroll down to "Integration tokens"**
3. **Click "Get integration token"**
4. **Enter description**: "OGI Framework Auto-Publishing"
5. **Copy the token** (you'll only see it once!)

### Step 2: Test Your Token

```bash
# Test your Medium token
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.medium.com/v1/me
```

Expected response:
```json
{
  "data": {
    "id": "your_user_id",
    "username": "uniqstic",
    "name": "Michael Gibson",
    "url": "https://medium.com/@uniqstic"
  }
}
```

## 🔗 LinkedIn API Setup

LinkedIn's API is more complex as it requires OAuth 2.0. Here are two approaches:

### Option A: LinkedIn Developer App (Recommended)

1. **Create LinkedIn App**: https://www.linkedin.com/developers/
2. **Fill in app details**:
   - App name: "OGI Framework Publisher"
   - LinkedIn Page: Your company page (if any)
   - App use: Content publishing
3. **Request access to "Share on LinkedIn" API**
4. **Get OAuth 2.0 access token**

### Option B: Personal Access Token (Simpler)

For personal use, you can use LinkedIn's OAuth playground:

1. **LinkedIn OAuth Helper**: https://www.linkedin.com/developers/tools/oauth
2. **Select scopes**: `w_member_social`, `r_liteprofile`
3. **Generate access token**
4. **Copy token** (valid for 60 days)

## ⚙️ Installation & Configuration

### Step 1: Install Dependencies

```bash
# Navigate to your repository
cd ontogenetic-intelligence

# Install additional dependencies for API integration
pip install python-dotenv requests
```

### Step 2: Set Up Credentials

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your tokens
nano .env
```

Add your credentials to `.env`:

```bash
# Medium API Credentials
MEDIUM_INTEGRATION_TOKEN=your_medium_token_here

# LinkedIn API Credentials
LINKEDIN_ACCESS_TOKEN=your_linkedin_token_here

# Optional settings
MEDIUM_DEFAULT_STATUS=draft
LINKEDIN_DEFAULT_VISIBILITY=PUBLIC
```

### Step 3: Test the Integration

```bash
# Test Medium connection
python src/social_api_integration.py

# Test full publishing (draft mode)
python scripts/publish_ogi_content.py --medium-draft
```

## 🚀 Usage Examples

### Publish Draft to Medium

```bash
python scripts/publish_ogi_content.py --medium-draft
```

### Publish Public Article to Medium

```bash
python scripts/publish_ogi_content.py --medium-public
```

### Share on LinkedIn Only

```bash
python scripts/publish_ogi_content.py --linkedin
```

### Publish to Medium + Share on LinkedIn

```bash
python scripts/publish_ogi_content.py --all
```

## 🔐 Security Best Practices

### 1. Environment Variables

Never commit `.env` to Git:

```bash
# Add to .gitignore (already included)
echo ".env" >> .gitignore
```

### 2. Token Management

- **Medium tokens**: Don't expire, but can be revoked
- **LinkedIn tokens**: Expire every 60 days (need refresh)
- **Keep tokens secret**: Never share in code or screenshots

### 3. Permissions

Grant minimal required permissions:
- **Medium**: Create and publish posts
- **LinkedIn**: Share content, read basic profile

## 🐛 Troubleshooting

### Medium API Issues

**Error 401 (Unauthorized)**
```bash
# Check your token
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.medium.com/v1/me
```

**Error 400 (Bad Request)**
- Check content format (markdown vs HTML)
- Verify all required fields are present
- Check tag limits (max 5 tags)

### LinkedIn API Issues

**Error 403 (Forbidden)**
- Check OAuth scopes: need `w_member_social`
- Verify app permissions in LinkedIn Developer Portal

**Error 422 (Unprocessable Entity)**
- Content may be too long (3000 char limit)
- Check if sharing the same content repeatedly (LinkedIn blocks duplicates)

### General Issues

**ModuleNotFoundError**
```bash
pip install python-dotenv requests
```

**File not found errors**
```bash
# Run from repository root
cd ontogenetic-intelligence
python scripts/publish_ogi_content.py --help
```

## 📊 Expected Output

### Successful Medium Publication

```
📝 Publishing to Medium as draft...
✅ Medium article saved as draft!
📖 URL: https://medium.com/@uniqstic/beyond-babyagi-ogi-123456
📊 ID: abc123def456
```

### Successful LinkedIn Share

```
🔗 Sharing on LinkedIn...
✅ Shared on LinkedIn!
📊 Post ID: urn:li:share:7890123456
```

## 🎯 Next Steps

Once set up, you can:

1. **Automate with GitHub Actions**: Trigger publishing on repository updates
2. **Schedule posts**: Use cron jobs for timed publishing
3. **Cross-platform analytics**: Track engagement across platforms
4. **Content variations**: Create platform-specific versions

## 📞 Support

If you encounter issues:

1. **Check the logs**: Error messages provide specific guidance
2. **Verify credentials**: Test API tokens independently
3. **Review permissions**: Ensure proper OAuth scopes
4. **API documentation**:
   - Medium: https://github.com/Medium/medium-api-docs
   - LinkedIn: https://docs.microsoft.com/en-us/linkedin/

---

**Ready to automate your OGI content publishing!** 🚀

Your research deserves to reach the AI community efficiently across all platforms.