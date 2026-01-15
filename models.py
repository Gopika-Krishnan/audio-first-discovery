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

    PLAY_BY_TITLE = "Find and play content by song title"
    PLAY_BY_ARTIST = "Find and play content by artist"
    PLAY_BY_GENRE = "Find and play content by genre"


class SpotifyOperation(BaseModel):
    type: SpotifyCommandType
    search_phrase: str | None
    verbal_response: str = Field(
        description="Response of the friendly assistant describing their next action."
    )
