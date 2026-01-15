import os

import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic import hub
from langchain_core.tools import Tool
from langchain_classic.agents import AgentExecutor, create_react_agent


class MusicKnowledge:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://ws.audioscrobbler.com/2.0/"

    def get_artist_context(self, artist_name):
        """Searches artist info in Last.fm"""
        params = {
            "method": "artist.getinfo",
            "artist": artist_name,
            "api_key": self.api_key,
            "format": "json"
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            bio = data['artist']['bio']['content']
            clean_bio = bio.split('<a href')[0]
            return clean_bio
        except Exception:
            return "Could not find information about the artist."

    def get_track_context(self, artist_name: str, track_name: str):
        params = {
            "method": "track.getInfo",
            "artist": artist_name.strip(),
            "track": track_name.strip(),
            "api_key": self.api_key,
            "format": "json"
        }
        try:
            res = requests.get(self.base_url, params=params).json()
            if 'track' in res and 'wiki' in res['track']:
                wiki = res['track']['wiki'].get('summary', "No description..")
                return wiki.split('<a href')[0].strip()
            return "I could not find information about the song."
        except:
            return "I could not find information about the song."

    def get_genre_context(self, genre_name: str):
        params = {
            "method": "tag.getInfo",
            "tag": genre_name.strip(),
            "api_key": self.api_key,
            "format": "json"
        }
        try:
            res = requests.get(self.base_url, params=params).json()
            summary = res['tag']['wiki']['summary']
            return summary.split('<a href')[0].strip()
        except:
            return "I could not find info about the genre."

    def get_similar_artists(self, artist_name: str):
        params = {
            "method": "artist.getSimilar",
            "artist": artist_name.strip(),
            "api_key": self.api_key,
            "limit": 3,
            "format": "json"
        }
        try:
            # CORRECCIÓN: Era self.base_url
            res = requests.get(self.base_url, params=params).json()
            similar = [a['name'] for a in res['similarartists']['artist']]
            return f"If you like {artist_name}, you could also like: {', '.join(similar)}."
        except:
            return "Could not find similar artists for the moment."

class ModelResponse:
    def __init__(self):
        lastfm_key = os.environ.get("LASTFM_API_KEY")
        knowledge_service = MusicKnowledge(lastfm_key)
        grok_key = os.environ.get("GROQ_API_KEY")

        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            groq_api_key=grok_key,
            temperature=0
        )            
 
        tools = [
            Tool(
                name="Artist_Knowledge",
                func=knowledge_service.get_artist_context,
                description="Use this when the user asks who is an artist of asks about his/her life or bio",
            ),
            Tool(
                name="Track_Knowledge",
                func=lambda q: knowledge_service.get_track_context(q.split(',')[0], q.split(',')[1]),
                description="Use this to know what is the song about. Expected input: 'Artist name, Song name'",
            ),
            Tool(
                name="Genre_Explanation",
                func=knowledge_service.get_genre_context,
                description="Use this when the user wants to know about a music genre (ej. Rock, Folk, classing)",
            ),
            Tool(
                name="Suggest_Similar_Music",
                func=knowledge_service.get_similar_artists,
                description="Use this if the user asks recommendations based on an artist they like",
            )
        ]
        prompt = hub.pull("hwchase17/react")   
 
        agent = create_react_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=True,
            handle_parsing_errors=True
        )
    def get_info(self, input_prompt):
        response = self.agent_executor.invoke({"input": input_prompt})
        return response


if __name__ == "__main__":
    load_dotenv()
    while True:
        input_text = input("What's your question?\n")
        mr = ModelResponse()
        res = mr.get_info(input_text)
        print(res["output"])
