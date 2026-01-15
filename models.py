import enum

from pydantic import BaseModel, Field


class SpotifyCommandType(enum.StrEnum):
    NEXT = "Play the next song"
    PREVIOUS = "Play the previous song"
    PAUSE = "Pause playback"
    RESUME = "Resume playback"

    CURRENT = "What is the track that's currently playing?"
    DESCRIBE_ARTIST = "Describe the currently playing artist"
    DESCRIBE_TRACK = "Describe the currently playing track"
    DESCRIBE_GENRE = "Describe the currently playing genre"
    SIMILAR_MUSIC = "Recommend me music similar to the currently playing"

    PLAY_BY_NAME = "Find and play content by title, artist, playlist or genre"
    SEARCH_BY_NAME = "Find by title, artist or playlist name - without playing"
    SEARCH_BY_LYRICS = "Find by lyrics - without playing"


class SpotifyOperation(BaseModel):
    type: SpotifyCommandType
    search_phrase: str | None = Field(
        description="Phrase to put into Spotify search bar."
    )
    verbal_response: str = Field(
        description="Response of the friendly assistant describing their next action."
    )
