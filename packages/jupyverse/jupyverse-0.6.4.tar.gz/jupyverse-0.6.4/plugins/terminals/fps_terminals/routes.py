from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Type

from fastapi import Response

from jupyverse_api.app import App
from jupyverse_api.auth import Auth, User
from jupyverse_api.terminals import Terminal, Terminals, TerminalServer

TERMINALS: Dict[str, Dict[str, Any]] = {}


class _Terminals(Terminals):
    def __init__(self, app: App, auth: Auth, _TerminalServer: Type[TerminalServer]) -> None:
        super().__init__(app=app, auth=auth)
        self.TerminalServer = _TerminalServer

    async def get_terminals(
        self,
        user: User,
    ):
        return [terminal["info"] for terminal in TERMINALS.values()]

    async def create_terminal(
        self,
        user: User,
    ):
        name_int = 1
        while True:
            if str(name_int) not in TERMINALS:
                break
            name_int += 1
        name = str(name_int)
        terminal = Terminal(
            name=name,
            last_activity=datetime.utcnow().isoformat() + "Z",
        )
        server = self.TerminalServer()
        TERMINALS[name] = {"info": terminal, "server": server}
        return terminal

    async def delete_terminal(
        self,
        name: str,
        user: User,
    ):
        await TERMINALS[name]["server"].exit(TERMINALS, name)
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    async def terminal_websocket(
        self,
        name,
        websocket_permissions,
    ):
        if websocket_permissions is None:
            return
        websocket, permissions = websocket_permissions
        await websocket.accept()
        await TERMINALS[name]["server"].serve(websocket, permissions, TERMINALS, name)
