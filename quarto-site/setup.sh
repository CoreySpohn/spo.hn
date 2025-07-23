#!/bin/bash

# Quarto Personal Website & CV System - Setup Script

echo "🚀 Setting up Quarto Personal Website & CV System..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create directories if they don't exist
mkdir -p _data assets scripts _site

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install --user pyyaml

# Download and install Quarto
if [ ! -d "quarto-1.7.31" ]; then
    echo "📥 Downloading Quarto..."
    wget -q https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.31/quarto-1.7.31-linux-amd64.tar.gz
    tar -xzf quarto-1.7.31-linux-amd64.tar.gz
    rm quarto-1.7.31-linux-amd64.tar.gz
    echo "✅ Quarto installed"
else
    echo "✅ Quarto already installed"
fi

# Download and install Typst for CV generation
if [ ! -d "typst-x86_64-unknown-linux-musl" ]; then
    echo "📥 Downloading Typst for CV generation..."
    wget -q https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz
    tar -xf typst-x86_64-unknown-linux-musl.tar.xz
    rm typst-x86_64-unknown-linux-musl.tar.xz
    echo "✅ Typst installed"
else
    echo "✅ Typst already installed"
fi

# Add to PATH
export PATH="$PWD/quarto-1.7.31/bin:$PWD/typst-x86_64-unknown-linux-musl:$PATH"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit your information in the _data/ directory"
echo "2. Run: export PATH=\"$PWD/quarto-1.7.31/bin:$PWD/typst-x86_64-unknown-linux-musl:\$PATH\""
echo "3. Preview your site: quarto preview"
echo "4. Build your site: quarto render"
echo ""
echo "📖 See USER_GUIDE.md for detailed instructions"