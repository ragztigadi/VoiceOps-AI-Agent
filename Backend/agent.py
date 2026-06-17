from __future__ import annotations
import os
from dotenv import load_dotenv
load_dotenv()
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.agents import AgentSession
from livekit.plugins import google
from prompts import WELCOME_MESSAGE
from api import AssistantFnc

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    model = google.beta.realtime.RealtimeModel(
        voice="Puck",
        temperature=0.8,
        modalities=["AUDIO"],
        language="en-US"
    )
    session = AgentSession(llm=model)
    await session.start(
        room=ctx.room,
        agent=AssistantFnc()
    )
    await session.generate_reply(
        instructions=WELCOME_MESSAGE
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))