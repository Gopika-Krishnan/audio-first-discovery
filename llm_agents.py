from agents import Agent

from models import SpotifyOperation


spotify_agent = Agent(
    name="Spotify Agent",
    handoff_description="Chooses which Spotify API call to perform",
    instructions="You are a friendly assistant facilitating a voice interaction with Spotify."
                 "Choose among the predetermined actions to perform, "
                 "specify the search phrase if necessary, "
                 "and describe your course of actions in a verbal response to the user.",
    output_type=SpotifyOperation,
    model="gpt-4.1-mini",
)
