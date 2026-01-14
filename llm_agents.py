from agents import Agent

from models import SpotifyOperation


spotify_agent = Agent(
    name="Spotify Agent",
    handoff_description="Chooses which Spotify API call to perform",
    instructions="Choose among the available actions "
                 + "and specify a search phrase if applicable",
    output_type=SpotifyOperation,
    model="gpt-4.1-mini",
)

wikipedia_agent = Agent(
    name="Wikipedia Agent",
    handoff_description="Calls Wikipedia API",
    instructions="Search Wikipedia for information requested about a song, band or instrument. Summarize it in two sentences.",
    model="gpt-4.1-mini",
)

principal_agent = Agent(
    name="Principal Agent",
    instructions="Choose whether to perform a Spotify control action or to retrieve requested information from Wikipedia.",
    handoffs=[spotify_agent, wikipedia_agent],
    model="gpt-4.1-mini",
)
