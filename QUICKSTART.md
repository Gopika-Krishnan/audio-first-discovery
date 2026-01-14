# Quick Reference: Enhanced Music Descriptions

## 🚀 Quick Start (3 steps)

```bash
# 1. Install
./setup_enrichment.sh

# 2. Configure (edit .env)
LASTFM_API_KEY=your_key_here

# 3. Use
./music "describe this song"
```

## 📝 Commands

| Command | Description | Enrichment |
|---------|-------------|------------|
| `./music "describe this song"` | Full enhanced description | ✅ Yes |
| `./music "describe this track"` | Full enhanced description | ✅ Yes |
| `./music "what's playing"` | Basic track info | ❌ No |
| `./music sync` | Standard analysis | ❌ No |

## 🔑 API Keys

### Last.fm (Required)
```bash
# Get from: https://www.last.fm/api/account/create
LASTFM_API_KEY=abc123...
```

### OpenAI (Optional)
```bash
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-...
```

## 📊 What You Get

### With Last.fm Only
- ✅ Artist biography
- ✅ Community tags
- ✅ Similar artists
- ✅ Inferred instruments

### With Last.fm + OpenAI
- ✅ Everything above, plus:
- ✅ AI-generated descriptions
- ✅ Detailed instrument analysis
- ✅ Mood and audience insights

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "musicbrainzngs not installed" | `pip install musicbrainzngs` |
| "LASTFM_API_KEY not set" | Add key to `.env` file |
| No enrichment data | Check API keys, internet connection |
| Slow first request | Normal - data is being fetched and cached |

## 📖 Full Documentation

- **User Guide**: [ENRICHMENT.md](ENRICHMENT.md)
- **Implementation**: [IMPLEMENTATION.md](IMPLEMENTATION.md)
- **Main README**: [README.md](README.md)

## 💡 Examples

### Example 1: Basic Usage
```bash
# Play a song
./music "play bohemian rhapsody"

# Get enhanced description
./music "describe this song"
```

### Example 2: With Caching
```bash
# First time (slow - fetches data)
./music "describe this song"  # 5-10 seconds

# Second time (fast - uses cache)
./music "describe this song"  # <100ms
```

### Example 3: Without OpenAI
```bash
# Still works, just no AI descriptions
# Set only LASTFM_API_KEY in .env
./music "describe this song"
```

## 🎯 Tips

1. **Cache is your friend** - First request is slow, subsequent ones are instant
2. **OpenAI is optional** - System works great with just Last.fm
3. **Check logs** - Run daemon in foreground to see what's happening
4. **Test first** - Run `python3 test_enrichment.py` to verify setup

## 📞 Need Help?

1. Check [ENRICHMENT.md](ENRICHMENT.md) for detailed docs
2. Run `python3 test_enrichment.py` to diagnose issues
3. Check daemon logs for errors
4. Verify API keys are correct in `.env`
