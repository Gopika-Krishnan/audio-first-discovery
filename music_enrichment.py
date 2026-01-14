#!/usr/bin/env python3
"""
Music Enrichment Module
Provides enhanced song descriptions including:
- Instrument detection from MusicBrainz
- Artist biographies from Wikipedia/MusicBrainz
- User-generated tags from Last.fm
- AI-powered descriptions from audio features
"""

import requests
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import musicbrainzngs
    MUSICBRAINZ_AVAILABLE = True
except ImportError:
    MUSICBRAINZ_AVAILABLE = False
    print("⚠️  musicbrainzngs not installed. Run: pip install musicbrainzngs")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class MusicEnrichment:
    """Enriches music metadata with additional information from multiple sources"""
    
    def __init__(self):
        """Initialize the enrichment service"""
        if MUSICBRAINZ_AVAILABLE:
            musicbrainzngs.set_useragent("IntelligentMusicAgent", "1.0", "https://github.com/tomcanham/intelligent-music-agent")
        
        # API keys from environment
        self.lastfm_key = os.getenv('LASTFM_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        if self.openai_key and OPENAI_AVAILABLE:
            openai.api_key = self.openai_key
        
        print("✅ Music enrichment service initialized")
        if not self.lastfm_key:
            print("⚠️  LASTFM_API_KEY not set - Last.fm features disabled")
        if not self.openai_key or not OPENAI_AVAILABLE:
            print("⚠️  OpenAI not available - AI descriptions disabled")
    
    def get_track_instruments(self, track_name: str, artist_name: str) -> List[str]:
        """Get instrument information from MusicBrainz"""
        if not MUSICBRAINZ_AVAILABLE:
            return []
        
        try:
            print(f"🔍 Searching MusicBrainz for instruments: {track_name} by {artist_name}")
            
            # Search for the recording
            result = musicbrainzngs.search_recordings(
                recording=track_name,
                artist=artist_name,
                limit=1
            )
            
            if not result.get('recording-list'):
                return []
            
            recording = result['recording-list'][0]
            recording_id = recording['id']
            
            # Get detailed recording info with relationships
            detailed = musicbrainzngs.get_recording_by_id(
                recording_id,
                includes=['artist-rels', 'work-rels']
            )
            
            instruments = []
            recording_data = detailed.get('recording', {})
            
            # Extract instrument credits from artist relationships
            for rel in recording_data.get('artist-relation-list', []):
                if 'attribute-list' in rel:
                    for attr in rel['attribute-list']:
                        if attr not in instruments:
                            instruments.append(attr)
            
            print(f"✅ Found {len(instruments)} instruments")
            return instruments
            
        except Exception as e:
            print(f"⚠️  MusicBrainz instrument search failed: {e}")
            return []
    
    def get_track_credits(self, track_name: str, artist_name: str) -> Dict[str, Any]:
        """Get production credits from MusicBrainz"""
        if not MUSICBRAINZ_AVAILABLE:
            return {}
        
        try:
            print(f"🔍 Searching MusicBrainz for credits: {track_name} by {artist_name}")
            
            result = musicbrainzngs.search_recordings(
                recording=track_name,
                artist=artist_name,
                limit=1
            )
            
            if not result.get('recording-list'):
                return {}
            
            recording = result['recording-list'][0]
            
            credits = {
                'recording_date': recording.get('first-release-date', ''),
                'length': recording.get('length', ''),
                'isrc': recording.get('isrc-list', [])
            }
            
            # Get release info for more details
            if 'release-list' in recording:
                release = recording['release-list'][0]
                credits['label'] = release.get('label-info-list', [{}])[0].get('label', {}).get('name', '')
            
            return credits
            
        except Exception as e:
            print(f"⚠️  MusicBrainz credits search failed: {e}")
            return {}
    
    def get_artist_bio(self, artist_name: str) -> str:
        """Get artist biography from Last.fm"""
        if not self.lastfm_key:
            return ""
        
        try:
            print(f"🔍 Fetching artist bio from Last.fm: {artist_name}")
            
            url = "http://ws.audioscrobbler.com/2.0/"
            params = {
                'method': 'artist.getinfo',
                'artist': artist_name,
                'api_key': self.lastfm_key,
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'artist' in data and 'bio' in data['artist']:
                    bio = data['artist']['bio'].get('summary', '')
                    # Clean up HTML tags
                    bio = bio.replace('<a href=', '\n<a href=')
                    bio = bio.split('<a href=')[0].strip()
                    print(f"✅ Found artist bio ({len(bio)} chars)")
                    return bio
            
            return ""
            
        except Exception as e:
            print(f"⚠️  Last.fm bio fetch failed: {e}")
            return ""
    
    def get_artist_info_musicbrainz(self, artist_name: str) -> Dict[str, Any]:
        """Get detailed artist info from MusicBrainz"""
        if not MUSICBRAINZ_AVAILABLE:
            return {}
        
        try:
            print(f"🔍 Searching MusicBrainz for artist: {artist_name}")
            
            result = musicbrainzngs.search_artists(artist=artist_name, limit=1)
            
            if not result.get('artist-list'):
                return {}
            
            artist = result['artist-list'][0]
            artist_id = artist['id']
            
            # Get detailed artist info
            detailed = musicbrainzngs.get_artist_by_id(
                artist_id,
                includes=['tags', 'ratings']
            )
            
            artist_data = detailed.get('artist', {})
            
            info = {
                'name': artist_data.get('name', artist_name),
                'type': artist_data.get('type', ''),
                'country': artist_data.get('country', ''),
                'life_span': artist_data.get('life-span', {}),
                'tags': [tag['name'] for tag in artist_data.get('tag-list', [])[:5]]
            }
            
            print(f"✅ Found artist info from MusicBrainz")
            return info
            
        except Exception as e:
            print(f"⚠️  MusicBrainz artist search failed: {e}")
            return {}
    
    def get_lastfm_tags(self, track_name: str, artist_name: str) -> List[str]:
        """Get user-generated tags from Last.fm"""
        if not self.lastfm_key:
            return []
        
        try:
            print(f"🔍 Fetching Last.fm tags: {track_name} by {artist_name}")
            
            url = "http://ws.audioscrobbler.com/2.0/"
            params = {
                'method': 'track.gettoptags',
                'artist': artist_name,
                'track': track_name,
                'api_key': self.lastfm_key,
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'toptags' in data and 'tag' in data['toptags']:
                    tags = [tag['name'] for tag in data['toptags']['tag'][:10]]
                    print(f"✅ Found {len(tags)} Last.fm tags")
                    return tags
            
            return []
            
        except Exception as e:
            print(f"⚠️  Last.fm tags fetch failed: {e}")
            return []
    
    def get_similar_artists(self, artist_name: str, limit: int = 5) -> List[Dict[str, str]]:
        """Get similar artists from Last.fm"""
        if not self.lastfm_key:
            return []
        
        try:
            print(f"🔍 Fetching similar artists from Last.fm: {artist_name}")
            
            url = "http://ws.audioscrobbler.com/2.0/"
            params = {
                'method': 'artist.getsimilar',
                'artist': artist_name,
                'api_key': self.lastfm_key,
                'format': 'json',
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'similarartists' in data and 'artist' in data['similarartists']:
                    similar = [
                        {
                            'name': artist['name'],
                            'match': artist.get('match', '0')
                        }
                        for artist in data['similarartists']['artist']
                    ]
                    print(f"✅ Found {len(similar)} similar artists")
                    return similar
            
            return []
            
        except Exception as e:
            print(f"⚠️  Last.fm similar artists fetch failed: {e}")
            return []
    
    def generate_ai_description(self, audio_features: Dict[str, Any], track_info: Dict[str, Any]) -> str:
        """Use AI to generate a rich description from audio features"""
        if not self.openai_key or not OPENAI_AVAILABLE:
            return ""
        
        try:
            print(f"🤖 Generating AI description for: {track_info.get('name', 'track')}")
            
            prompt = f"""Based on these audio characteristics for the song "{track_info.get('name', 'Unknown')}" by {track_info.get('artist', 'Unknown')}:

- Energy: {audio_features.get('energy', 0):.2f} (0=low, 1=high)
- Valence: {audio_features.get('valence', 0):.2f} (0=sad, 1=happy)
- Danceability: {audio_features.get('danceability', 0):.2f}
- Acousticness: {audio_features.get('acousticness', 0):.2f}
- Instrumentalness: {audio_features.get('instrumentalness', 0):.2f}
- Tempo: {audio_features.get('tempo', 0):.0f} BPM
- Key: {audio_features.get('key', -1)}
- Mode: {'Major' if audio_features.get('mode', 0) == 1 else 'Minor'}
- Loudness: {audio_features.get('loudness', 0):.1f} dB

Provide a brief (2-3 sentences) description of:
1. What instruments are likely featured
2. The overall mood and feel of the song
3. What kind of listener would enjoy this

Be specific and vivid, but concise."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a music expert who describes songs based on their audio characteristics."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            description = response.choices[0].message.content.strip()
            print(f"✅ Generated AI description ({len(description)} chars)")
            return description
            
        except Exception as e:
            print(f"⚠️  AI description generation failed: {e}")
            return ""
    
    def infer_instruments_from_features(self, audio_features: Dict[str, Any]) -> List[str]:
        """Infer likely instruments based on audio features (rule-based)"""
        instruments = []
        
        acousticness = audio_features.get('acousticness', 0)
        instrumentalness = audio_features.get('instrumentalness', 0)
        energy = audio_features.get('energy', 0)
        
        # High acousticness suggests acoustic instruments
        if acousticness > 0.7:
            instruments.extend(['acoustic guitar', 'piano'])
        elif acousticness > 0.4:
            instruments.append('acoustic guitar')
        
        # Low acousticness + high energy suggests electric/electronic
        if acousticness < 0.3 and energy > 0.7:
            instruments.extend(['electric guitar', 'synthesizer', 'drums'])
        
        # High instrumentalness suggests focus on instruments
        if instrumentalness > 0.5:
            instruments.append('instrumental focus')
        
        # Energy level suggests percussion
        if energy > 0.6:
            if 'drums' not in instruments:
                instruments.append('drums')
        
        return instruments
    
    def get_enhanced_description(self, track_info: Dict[str, Any], audio_features: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Combine all enrichment sources into a comprehensive description
        
        Args:
            track_info: Basic track info (name, artist, album, etc.)
            audio_features: Spotify audio features (optional)
        
        Returns:
            Dictionary with enriched information
        """
        track_name = track_info.get('name', '')
        artist_name = track_info.get('artist', '')
        
        print(f"\n🎵 Enriching: {track_name} by {artist_name}")
        print("=" * 60)
        
        enriched = {
            'track_name': track_name,
            'artist_name': artist_name,
            'enriched_at': datetime.now().isoformat(),
            'sources': []
        }
        
        # Get instruments from MusicBrainz
        instruments = self.get_track_instruments(track_name, artist_name)
        if instruments:
            enriched['instruments'] = instruments
            enriched['sources'].append('musicbrainz_instruments')
        
        # Get production credits
        credits = self.get_track_credits(track_name, artist_name)
        if credits:
            enriched['credits'] = credits
            enriched['sources'].append('musicbrainz_credits')
        
        # Get artist biography
        bio = self.get_artist_bio(artist_name)
        if bio:
            enriched['artist_bio'] = bio
            enriched['sources'].append('lastfm_bio')
        
        # Get artist info from MusicBrainz
        artist_info = self.get_artist_info_musicbrainz(artist_name)
        if artist_info:
            enriched['artist_info'] = artist_info
            enriched['sources'].append('musicbrainz_artist')
        
        # Get Last.fm tags
        tags = self.get_lastfm_tags(track_name, artist_name)
        if tags:
            enriched['lastfm_tags'] = tags
            enriched['sources'].append('lastfm_tags')
        
        # Get similar artists
        similar = self.get_similar_artists(artist_name)
        if similar:
            enriched['similar_artists'] = similar
            enriched['sources'].append('lastfm_similar')
        
        # Infer instruments from audio features if available
        if audio_features:
            inferred_instruments = self.infer_instruments_from_features(audio_features)
            if inferred_instruments:
                enriched['inferred_instruments'] = inferred_instruments
                enriched['sources'].append('audio_analysis')
            
            # Generate AI description
            ai_description = self.generate_ai_description(audio_features, track_info)
            if ai_description:
                enriched['ai_description'] = ai_description
                enriched['sources'].append('openai')
        
        print("=" * 60)
        print(f"✅ Enrichment complete - {len(enriched['sources'])} sources used")
        
        return enriched
    
    def format_enriched_description(self, enriched: Dict[str, Any]) -> str:
        """Format enriched data into a human-readable description"""
        lines = []
        
        lines.append(f"🎵 **{enriched['track_name']}** by **{enriched['artist_name']}**")
        lines.append("")
        
        # AI Description (if available)
        if 'ai_description' in enriched:
            lines.append("🤖 **AI Analysis:**")
            lines.append(enriched['ai_description'])
            lines.append("")
        
        # Instruments
        if 'instruments' in enriched and enriched['instruments']:
            lines.append(f"🎸 **Instruments**: {', '.join(enriched['instruments'])}")
        elif 'inferred_instruments' in enriched and enriched['inferred_instruments']:
            lines.append(f"🎸 **Likely Instruments**: {', '.join(enriched['inferred_instruments'])}")
        
        # Credits
        if 'credits' in enriched:
            credits = enriched['credits']
            if credits.get('recording_date'):
                lines.append(f"📅 **Recorded**: {credits['recording_date']}")
            if credits.get('label'):
                lines.append(f"🏢 **Label**: {credits['label']}")
        
        # Artist Info
        if 'artist_info' in enriched:
            info = enriched['artist_info']
            if info.get('country'):
                lines.append(f"🌍 **Origin**: {info['country']}")
            if info.get('life_span'):
                span = info['life_span']
                if span.get('begin'):
                    lines.append(f"📆 **Active Since**: {span['begin']}")
        
        # Artist Bio
        if 'artist_bio' in enriched:
            bio = enriched['artist_bio']
            if len(bio) > 300:
                bio = bio[:297] + "..."
            lines.append("")
            lines.append("👤 **About the Artist:**")
            lines.append(bio)
        
        # Last.fm Tags
        if 'lastfm_tags' in enriched and enriched['lastfm_tags']:
            lines.append("")
            lines.append(f"🏷️  **Tags**: {', '.join(enriched['lastfm_tags'][:8])}")
        
        # Similar Artists
        if 'similar_artists' in enriched and enriched['similar_artists']:
            similar_names = [a['name'] for a in enriched['similar_artists'][:5]]
            lines.append("")
            lines.append(f"🎭 **Similar Artists**: {', '.join(similar_names)}")
        
        # Data sources
        lines.append("")
        lines.append(f"📊 **Data from**: {', '.join(enriched['sources'])}")
        
        return "\n".join(lines)


def test_enrichment():
    """Test the enrichment service"""
    enrichment = MusicEnrichment()
    
    # Test with a well-known track
    track_info = {
        'name': 'Bohemian Rhapsody',
        'artist': 'Queen',
        'album': 'A Night at the Opera'
    }
    
    # Mock audio features
    audio_features = {
        'energy': 0.65,
        'valence': 0.45,
        'danceability': 0.50,
        'acousticness': 0.30,
        'instrumentalness': 0.15,
        'tempo': 144,
        'key': 3,
        'mode': 0,
        'loudness': -8.5
    }
    
    enriched = enrichment.get_enhanced_description(track_info, audio_features)
    formatted = enrichment.format_enriched_description(enriched)
    
    print("\n" + "=" * 60)
    print("FORMATTED OUTPUT:")
    print("=" * 60)
    print(formatted)


if __name__ == "__main__":
    test_enrichment()
