from typing import Optional, Dict
from pydantic import BaseModel, Field


FUNCTION_DESCR = {
    "dependencies": ["json", "os", "asyncio", "pathlib", "glob",
        "datetime", "halerium.utilities.board", 
        "halerium.utilities.collab", 
        "halerium.utilities.prompt.agents",
        "halerium_utilities.board.navigator"],
    "category": None,
    "pip_install_runner": []
}


class BotArgument(BaseModel):
    board_path: str = Field(description="Path of the board file defining the subagent.")
    task: str = Field(description="The instructions for the bot.")


async def execute_subagent(data: BotArgument):
    """
    Executes the board with the given name from the given 
    source_path and returns the output.
    Expects dictionary "data" to have the keys "name", "source_path" and "task".
    """
    import json
    from datetime import datetime
    from pathlib import Path
    import asyncio
    from halerium_utilities.collab import CollabBoard
    from halerium_utilities.prompt.agents import call_agent_async
    from halerium_utilities.board.navigator import BoardNavigator
    from halerium_utilities.board.board import Board

    board_path: str = data.get("board_path")
    board_path = Path(board_path)
    log_path = Path(board_path.parent) / "logs"

    task: str = data.get("task")

    if not board_path or not task:
        return "Please specify the subagents board_path and task!"

    try:
        log_path.mkdir(exist_ok=True, parents=True)
    except Exception as e:
        return f"failed to setup directories: {str(e)}"

    if not board_path.exists():
        return f"Board path does not exist: {board_path}."

    try:
        b = Board.from_json(board_path)

        run_filename = log_path / f"{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}_{board_path.name}"
        b.to_json(run_filename)

        # hook into the collab object
        c = CollabBoard(run_filename)
        nav = BoardNavigator(c.to_dict())

        # execute agent
        ex_ord = nav.get_execution_order(nav.cards)

        c.update_card({
            "id": ex_ord[0],
            "type_specific": {
                "prompt_input": task
            }
        })
        await asyncio.to_thread(c.push)

        res = ""
        for ex in ex_ord:
            async for e in call_agent_async(c.to_dict(), ex):
                if e.event == 'chunk':
                    res += json.loads(e.data).get('chunk', '')

            # Update the card with the agent response
            c.update_card({
                "id": ex,
                "type_specific": {
                    "prompt_output": res
                }
            })
            await asyncio.to_thread(c.push)

    except Exception as e:
        return str(e)

    return res


class GetAssistantsArgument(BaseModel):
    source_path: str = Field(description="Path of the folder in which the subagent boards are.")


async def get_subagents(data: GetAssistantsArgument):
    """
    This function collects boards files defining subagents.
    It will return the subagents paths and descriptions.
    """
    from pathlib import Path
    from halerium_utilities.board import Board
    import json

    s_path: str = data.get("source_path")
    source_path = Path(s_path)

    if not source_path.exists():
        return f"Source directory does not exist: {source_path}"

    assistants = {}

    for board_file in source_path.glob("*.board"):
        board = Board.from_json(board_file)

        table = [n for n in board.cards if n.type == "note"]
        description = None

        for note in table:
            if note.type_specific.title.lower().startswith("description"):
                description = note.type_specific.message
        assistants[str(board_file)] = {
            "description": description,
        }

    return json.dumps(assistants, indent=4)

