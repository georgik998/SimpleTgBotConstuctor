import shlex
import asyncio
import os
import signal

from src.application.deployment.service import IDeployService


class ProcessDeployService(IDeployService):

    def __init__(self):
        self.processes: dict[int, int] = {}

    async def start(
            self,
            bot_id: int,
            cmd: str,
            depend_on_main_process: bool = False,
    ) -> bool:
        if self.processes.get(bot_id) is not None:
            return False

        process = await asyncio.create_subprocess_exec(
            *shlex.split(cmd),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
            stdin=asyncio.subprocess.DEVNULL,
            start_new_session=depend_on_main_process
        )
        self.processes[bot_id] = process.pid
        return True

    async def stop(self, bot_id: int) -> bool:
        if self.processes.get(bot_id) is None:
            return False
        try:
            os.kill(self.processes[bot_id], signal.SIGTERM)  # SIGTERM - нежное убийство, дадим допить кофе
            del self.processes[bot_id]
            return True
        except ProcessLookupError:
            return False

