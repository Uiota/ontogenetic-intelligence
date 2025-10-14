#!/bin/bash
# OGI Dashboard Setup and Launch Script

echo "🧬 OGI Interactive Dashboard Setup"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "web-interface/package.json" ]; then
    echo "❌ Please run this script from the ontogenetic-intelligence root directory"
    exit 1
fi

cd web-interface

echo "📦 Installing dependencies..."

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first:"
    echo "   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "   sudo apt-get install -y nodejs"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first"
    exit 1
fi

echo "📋 Node version: $(node --version)"
echo "📋 npm version: $(npm --version)"

# Install dependencies
echo "📦 Installing React and dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🚀 Starting OGI Dashboard..."
    echo "📊 Dashboard will open at: http://localhost:3000"
    echo "⚡ Features:"
    echo "   • Interactive OGI vs FL simulation"
    echo "   • Real-time CCI metrics visualization"
    echo "   • Export CSV and logs"
    echo "   • Generate Python simulation code"
    echo ""
    echo "🔧 Press Ctrl+C to stop the server"
    echo ""

    # Start the development server
    npm start
else
    echo "❌ Failed to install dependencies"
    echo "💡 Try running:"
    echo "   cd web-interface"
    echo "   npm install --legacy-peer-deps"
    echo "   npm start"
fi