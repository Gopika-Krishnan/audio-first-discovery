import enum

from pydantic import BaseModel, Field


class SpotifyCommandType(enum.StrEnum):
    NEXT = "Play the next song"
    PREVIOUS = "Play the previous song"
    PAUSE = "Pause playback"
    RESUME = "Resume playback"

    CURRENT = "What's is the track that's currently playing?"
    LIKE_ARTIST = "Like the currently played artist"

    PLAY_BY_TAGS = "Find and play content by general description: mood, genre etc."
    PLAY_BY_NAME = "Find and play content by title, artist or playlist name"
    SEARCH_BY_NAME = "Find by title, artist or playlist name - without playing"
    SEARCH_BY_LYRICS = "Find by lyrics - without playing"


class SpotifyOperation(BaseModel):
    type: SpotifyCommandType
    search_phrase: str | None = Field(
        description="Phrase to put into Spotify search bar."
    )
