#!/bin/bash
#
# Complete Insight-Bot Setup with Node 22
# ADHD-friendly: One command setup
#

echo "🚀 Setting up Insight-Bot with Node 22 + Devvit CLI"
echo ""

cd ~/insight-bot || exit 1

# Install Node 22 if needed
echo "📦 Checking Node version..."
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)

if [ "$NODE_VERSION" -lt 22 ]; then
    echo "⚠️  Node $NODE_VERSION detected. Installing Node 22..."
    
    # Install nvm if not present
    if ! command -v nvm &> /dev/null; then
        echo "Installing nvm..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
    fi
    
    # Install and use Node 22
    nvm install 22
    nvm use 22
    nvm alias default 22
else
    echo "✓ Node $NODE_VERSION detected (meets requirement)"
fi

# Clean install
echo ""
echo "🧹 Cleaning previous installation..."
rm -rf node_modules package-lock.json

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Install Devvit CLI locally
echo ""
echo "📦 Installing Devvit CLI..."
npm install devvit@latest

# Verify
echo ""
echo "✅ Verifying installation..."
./node_modules/.bin/devvit --version

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Ready to deploy to Reddit."
    echo ""
    echo "Add to PATH for easier use:"
    echo "  echo 'export PATH="./node_modules/.bin:$PATH"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""
    echo "Then you can run:"
    echo "  devvit login"
    echo "  npm run dev"
    echo "  npm run deploy"
    echo ""
else
    echo "❌ Installation failed. Check logs above."
fi