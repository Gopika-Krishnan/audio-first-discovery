#!/bin/bash
# Setup script for Music Enrichment features

echo "🎵 Setting up Music Enrichment Features"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "music_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv music_env
fi

# Activate virtual environment
source music_env/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""

# Check for API keys
echo "🔑 Checking API key configuration..."
echo ""

if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your API keys:"
    echo "   - LASTFM_API_KEY (get from https://www.last.fm/api/account/create)"
    echo "   - OPENAI_API_KEY (optional, get from https://platform.openai.com/api-keys)"
    echo ""
else
    echo "✅ .env file exists"
    
    # Check if keys are configured
    if grep -q "your_lastfm_api_key_here" .env; then
        echo "⚠️  Last.fm API key not configured in .env"
    else
        echo "✅ Last.fm API key configured"
    fi
    
    if grep -q "your_openai_api_key_here" .env; then
        echo "⚠️  OpenAI API key not configured (optional)"
    else
        echo "✅ OpenAI API key configured"
    fi
fi

echo ""
echo "🧪 Testing enrichment module..."
python3 -c "from music_enrichment import MusicEnrichment; print('✅ Music enrichment module loaded successfully')" 2>/dev/null || echo "⚠️  Music enrichment module has issues"

echo ""
echo "📚 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run: source music_env/bin/activate"
echo "3. Test with: python3 music_enrichment.py"
echo "4. Try the new 'describe' command: ./music 'describe this song'"
echo ""
