import asyncio

from agents import SQLiteSession, Runner
from dotenv import load_dotenv

from llm_agents import spotify_agent
from models import SpotifyOperation
from music_agent import ComprehensiveMusicAgent
from voice import WhisperListener, read_text


async def main():
    load_dotenv()
    spotify_handler = ComprehensiveMusicAgent()
    listener = WhisperListener(model_name="base")
    session = SQLiteSession("voice_app")
    openai_runner = Runner()

    print("🎵 Voice-enabled Music Agent")
    print("🎙️ Say a command, or type it.")
    print("🛑 Say 'quit' to exit\n")

    while True:
        try:
            mode = input("⌨️  Press Enter to speak, or type a command: ").strip()

            if mode == "":
                command = listener.listen(duration=2)
            else:
                command = mode

            if not command:
                continue

            if command.lower() in ["quit", "exit", "stop"]:
                break

            load_dotenv()

            result = await openai_runner.run(spotify_agent, command, session=session)
            response = result.final_output
            print(response.verbal_response)
            await read_text(response.verbal_response)

            response = spotify_handler.handle_command(response)
            print(response)
            await read_text(response)
            print()

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())
