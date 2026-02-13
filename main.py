import typer
import asyncio
from rich.console import Console

# Modules
from modules.offensive.ddos import DDoSStressor
from modules.offensive.scanner import PortScanner
from modules.defensive.audit import NetworkAuditor
from modules.utility.chat import BifrostChat
from modules.defensive.network import PacketSniffer

app = typer.Typer(help="Xenons: Advanced Security Tool")
console = Console()

@app.command()
def ddos(target: str, concurrency: int = 50, duration: int = 10):
    """Launch a DDoS Stress Test"""
    stressor = DDoSStressor(target, concurrency)
    asyncio.run(stressor.attack(duration))

@app.command()
def scan(target: str):
    """Scan open ports on a target"""
    scanner = PortScanner(target)
    asyncio.run(scanner.scan())

@app.command()
def audit(target: str):
    """Audit SSL/TLS security"""
    auditor = NetworkAuditor(target)
    auditor.check_ssl()

@app.command()
def sniff(interface: str = "en0", count: int = 20):
    """Sniff network packets"""
    sniffer = PacketSniffer(interface)
    sniffer.start(count)

@app.command()
def chat():
    """Start Bifrost Secure Chat Node"""
    chat_node = BifrostChat()
    console.print("[bold red]Feature Work In Progress: Secure Chat needs peer exchange logic.[/bold red]")

@app.command()
def interactive():
    """Start Interactive Mode"""
    console.print(r"""[bold cyan]
██╗  ██╗███████╗███╗   ██╗ ██████╗ ███╗   ██╗███████╗
╚██╗██╔╝██╔════╝████╗  ██║██╔═══██╗████╗  ██║██╔════╝
 ╚███╔╝ █████╗  ██╔██╗ ██║██║   ██║██╔██╗ ██║███████╗
 ██╔██╗ ██╔══╝  ██║╚██╗██║██║   ██║██║╚██╗██║╚════██║
██╔╝ ██╗███████╗██║ ╚████║╚██████╔╝██║ ╚████║███████║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝[/bold cyan]""")
    console.print("[yellow]Welcome to Xenons Interactive Shell[/yellow]")
    console.print("Run [bold]python3 main.py --help[/bold] for commands.")

if __name__ == "__main__":
    app()
