import asyncio
import signal
from typing import List, Callable, Awaitable
from rich.console import Console

console = Console()

class AsyncEngine:
    def __init__(self, concurrency: int = 100):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.sem = asyncio.Semaphore(concurrency)
        self.tasks: List[asyncio.Task] = []
        self._setup_signals()

    def _setup_signals(self):
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.loop.add_signal_handler(sig, self.stop)

    def stop(self):
        console.print("[bold red]Stopping engine...[/bold red]")
        for task in self.tasks:
            task.cancel()
        self.loop.stop()

    async def run_task(self, coro: Awaitable):
        async with self.sem:
            return await coro

    def run(self, coro: Awaitable):
        try:
            return self.loop.run_until_complete(coro)
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.loop.close()

engine = AsyncEngine()
