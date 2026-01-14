import asyncio

from agents import SQLiteSession, Runner
from dotenv import load_dotenv

from llm_agents import principal_agent
from models import SpotifyOperation
from music_agent import ComprehensiveMusicAgent
from voice import WhisperListener, read_text


async def main():
    load_dotenv()
    agent = ComprehensiveMusicAgent()
    listener = WhisperListener(model_name="base")
    session = SQLiteSession("voice_app")
    runner = Runner()

    print("🎵 Voice-enabled Music Agent")
    print("🎙️ Say a command, or type it.")
    print("🛑 Say 'quit' to exit\n")

    while True:
        try:
            mode = input("⌨️  Press Enter to speak, or type a command: ").strip()

            if mode == "":
                command = listener.listen(duration=5)
            else:
                command = mode

            if not command:
                continue

            if command.lower() in ["quit", "exit", "stop"]:
                break

            load_dotenv()
            result = await runner.run(principal_agent, command, session=session)

            if isinstance(result, SpotifyOperation):
                response = agent.handle_command(result.final_output)
                runner.run_sync(
                    principal_agent,
                    response,
                    session=session
                )
            else:
                response = result.final_output

            print(response)
            await read_text(response)
            print()

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())
