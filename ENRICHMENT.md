# 🌟 Music Enrichment Features

## Overview

The Music Enrichment module extends the Intelligent Music Agent with rich, detailed song descriptions including:

- 🎸 **Instrument Detection** - Identifies instruments used in tracks
- 👤 **Artist Biographies** - Detailed artist background and history
- 🏷️ **User-Generated Tags** - Community tags from Last.fm
- 🎭 **Similar Artists** - Discover related musicians
- 🤖 **AI-Powered Descriptions** - Intelligent analysis of musical characteristics
- 📊 **Production Credits** - Recording dates, producers, studios, labels
- 🌍 **Artist Origins** - Country, formation year, band members

## Installation

### 1. Run the Setup Script

```bash
./setup_enrichment.sh
```

### 2. Configure API Keys

Edit `.env` and add your API keys:

```bash
# Last.fm API Key (Required for most features)
LASTFM_API_KEY=your_actual_key_here

# OpenAI API Key (Optional, for AI descriptions)
OPENAI_API_KEY=your_actual_key_here
```

### 3. Get API Keys

#### Last.fm API Key (Free)
1. Go to https://www.last.fm/api/account/create
2. Fill in the application details
3. Copy the API key to your `.env` file

#### OpenAI API Key (Optional, Paid)
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy it to your `.env` file

**Note:** OpenAI is optional. The system works without it, but AI-powered descriptions won't be available.

## Usage

### Basic Command

```bash
./music "describe this song"
```

This command provides an **enhanced description** with:
- All standard Spotify metadata
- Instruments (from MusicBrainz or inferred from audio features)
- Artist biography (from Last.fm)
- User-generated tags (from Last.fm)
- Similar artists (from Last.fm)
- AI-generated description (if OpenAI is configured)

### Example Output

```
🎵 **Bohemian Rhapsody** by **Queen**

🎤 **Album**: A Night at the Opera
📅 **Released**: 1975
🎸 **Genres**: rock, classic rock, glam rock
⚡ **Energy**: energetic
😊 **Mood**: neutral/balanced
💃 **Danceability**: danceable
🥁 **Tempo**: medium tempo (144 BPM)

============================================================
🌟 **ENHANCED DESCRIPTION** 🌟
============================================================

🤖 **AI Analysis:**
This track likely features piano, electric guitar, and drums with orchestral 
elements. The song has a theatrical, operatic quality with dramatic shifts in 
mood and energy. Perfect for listeners who enjoy progressive rock and complex 
musical arrangements.

🎸 **Likely Instruments**: piano, electric guitar, drums, vocals

📅 **Recorded**: 1975-08-24
🏢 **Label**: EMI

👤 **About the Artist:**
Queen were a British rock band formed in London in 1970. The band comprised 
Freddie Mercury (lead vocals, piano), Brian May (guitar, vocals), Roger Taylor 
(drums, vocals) and John Deacon (bass)...

🏷️ **Tags**: rock, classic rock, progressive rock, british, 70s, glam rock

🎭 **Similar Artists**: David Bowie, Led Zeppelin, The Who, Pink Floyd, Elton John

📊 **Data from**: musicbrainz_instruments, musicbrainz_credits, lastfm_bio, 
lastfm_tags, lastfm_similar, audio_analysis, openai
```

## Features Breakdown

### 1. Instrument Detection

**Sources:**
- **MusicBrainz** - Actual instrument credits from recordings
- **Audio Analysis** - Inferred from Spotify audio features

**Example:**
```
🎸 **Instruments**: acoustic guitar, piano, drums
🎸 **Likely Instruments**: synthesizer, bass guitar
```

### 2. Artist Information

**Sources:**
- **Last.fm** - Biography, similar artists
- **MusicBrainz** - Formation year, country, members, tags

**Example:**
```
👤 **About the Artist:**
Pink Floyd were an English rock band formed in London in 1965...

🌍 **Origin**: United Kingdom
📆 **Active Since**: 1965
```

### 3. User-Generated Tags

**Source:** Last.fm community tags

**Example:**
```
🏷️ **Tags**: psychedelic rock, progressive rock, classic rock, 
british, 70s, concept albums, art rock, space rock
```

### 4. Similar Artists

**Source:** Last.fm similarity algorithm

**Example:**
```
🎭 **Similar Artists**: David Gilmour, Roger Waters, Genesis, 
Yes, King Crimson
```

### 5. AI-Powered Descriptions

**Source:** OpenAI GPT-3.5/4 (optional)

Generates natural language descriptions based on audio features:
- Likely instruments
- Overall mood and feel
- Target audience

**Example:**
```
🤖 **AI Analysis:**
This track features prominent acoustic guitar and piano with subtle 
electronic elements. The melancholic mood and slow tempo create an 
introspective atmosphere. Ideal for listeners who enjoy contemplative, 
emotionally resonant music.
```

### 6. Production Credits

**Source:** MusicBrainz

**Example:**
```
📅 **Recorded**: 1973-06-01
🏢 **Label**: Harvest Records
🎙️ **Producer**: Alan Parsons
🏠 **Studio**: Abbey Road Studios
```

## Caching

All enrichment data is cached in the SQLite database to:
- Minimize API calls
- Improve response time
- Work offline after initial fetch

**Database Tables:**
- `track_enrichment` - Track-specific data
- `artist_enrichment` - Artist-specific data

## API Rate Limits

### Last.fm
- **Free tier**: Unlimited requests
- **Rate limit**: ~5 requests/second

### MusicBrainz
- **Free**: 1 request/second
- **Respectful usage**: Built-in delays

### OpenAI
- **Paid**: Based on your plan
- **Cost**: ~$0.002 per description (GPT-3.5-turbo)

## Troubleshooting

### "⚠️ musicbrainzngs not installed"

```bash
pip install musicbrainzngs
```

### "⚠️ LASTFM_API_KEY not set"

1. Get a key from https://www.last.fm/api/account/create
2. Add to `.env`: `LASTFM_API_KEY=your_key`
3. Restart the daemon

### "⚠️ OpenAI not available"

Either:
1. Install: `pip install openai`
2. Add key to `.env`: `OPENAI_API_KEY=your_key`

Or simply skip - AI descriptions are optional.

### No enrichment data showing

1. Check API keys are configured
2. Verify internet connection
3. Try: `python3 music_enrichment.py` to test
4. Check logs for specific errors

## Commands

### Get Enhanced Description
```bash
./music "describe this song"
./music "describe this track"
./music "describe this"
```

### Standard Analysis (No Enrichment)
```bash
./music "what's playing"
./music "what kind of music is this"
./music sync
```

## Privacy & Data

- **No personal data** is sent to external APIs
- Only **track names and artist names** are queried
- All data is **cached locally** in SQLite
- **No tracking** or analytics

## Performance

- **First request**: 3-10 seconds (fetching from APIs)
- **Cached requests**: <100ms
- **Storage**: ~1-5KB per track

## Extending

Want to add more data sources? Edit `music_enrichment.py`:

```python
def get_custom_data(self, track_name, artist_name):
    # Your custom API integration
    pass

def get_enhanced_description(self, track_info, audio_features):
    # Add your custom data
    enriched['custom_data'] = self.get_custom_data(...)
    return enriched
```

## Credits

- **MusicBrainz** - Open music encyclopedia
- **Last.fm** - Music discovery and statistics
- **OpenAI** - AI-powered descriptions
- **Spotify** - Audio features and metadata

## License

MIT License - Same as the main project
