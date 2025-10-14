#!/bin/bash
# Deploy OGI Dashboard to GitHub Pages

echo "🚀 Deploying OGI Dashboard to GitHub Pages"
echo "==========================================="

# Check if we're in the right directory
if [ ! -f "web-interface/package.json" ]; then
    echo "❌ Please run this script from the ontogenetic-intelligence root directory"
    exit 1
fi

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Committing changes..."
    git add .
    git commit -m "🚀 Deploy OGI Interactive Dashboard to GitHub Pages

Complete React dashboard with:
• Real-time OGI vs Traditional FL simulation
• Interactive CCI metrics visualization
• Multiple view modes and export features
• Professional UI with Tailwind CSS
• Mobile-responsive design

Live demo will be available at:
https://Uiota.github.io/ontogenetic-intelligence

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push origin main

# Enable GitHub Pages if not already enabled
echo "🌐 GitHub Pages will auto-deploy from the workflow"
echo "📊 Dashboard will be live at: https://Uiota.github.io/ontogenetic-intelligence"
echo ""
echo "🔧 To enable GitHub Pages manually:"
echo "   1. Go to: https://github.com/Uiota/ontogenetic-intelligence/settings/pages"
echo "   2. Set Source: 'GitHub Actions'"
echo "   3. The workflow will auto-deploy on push to main"
echo ""
echo "⏱️  Deployment typically takes 2-5 minutes"
echo "✅ Once live, add this link to your Medium article!"

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo ""
    echo "🔗 Opening repository settings..."
    gh repo view --web
fi