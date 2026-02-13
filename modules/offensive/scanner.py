import asyncio
import socket
from rich.console import Console
from rich.table import Table

console = Console()

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    8080: "HTTP-Alt"
}

class PortScanner:
    def __init__(self, target: str):
        self.target = target
        self.open_ports = []

    async def scan_port(self, port):
        conn = asyncio.open_connection(self.target, port)
        try:
            reader, writer = await asyncio.wait_for(conn, timeout=1.0)
            self.open_ports.append(port)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False

    async def scan(self):
        console.print(f"[bold blue]Scanning {self.target}...[/bold blue]")
        tasks = [self.scan_port(p) for p in COMMON_PORTS.keys()]
        await asyncio.gather(*tasks)
        self.report()

    def report(self):
        table = Table(title=f"Scan Results: {self.target}")
        table.add_column("Port", style="cyan")
        table.add_column("Service", style="magenta")
        table.add_column("Status", style="green")

        for port in self.open_ports:
            table.add_row(str(port), COMMON_PORTS.get(port, "Unknown"), "OPEN")

        if not self.open_ports:
            console.print("[yellow]No open ports found.[/yellow]")
        else:
            console.print(table)
