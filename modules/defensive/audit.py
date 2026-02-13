import ssl
import socket
from rich.console import Console

console = Console()

class NetworkAuditor:
    def __init__(self, target: str):
        self.target = target

    def check_ssl(self):
        console.print(f"[bold cyan]Auditing SSL/TLS for {self.target}...[/bold cyan]")
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((self.target, 443)) as sock:
                with ctx.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    console.print(f"[green]✓ Certificate Valid[/green]")
                    console.print(f"  Issuer: {cert.get('issuer', 'Unknown')}")
                    console.print(f"  Version: {ssock.version()}")
                    console.print(f"  Cipher: {ssock.cipher()[0]}")
        except Exception as e:
            console.print(f"[red]✕ SSL Audit Failed: {e}[/red]")
