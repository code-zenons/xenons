from rich.console import Console
try:
    from scapy.all import sniff
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

console = Console()

class PacketSniffer:
    def __init__(self, interface: str = "en0"):
        self.interface = interface

    def start(self, count=10):
        if not SCAPY_AVAILABLE:
            console.print("[red]Scapy not installed. Cannot sniff packets.[/red]")
            return

        console.print(f"[bold yellow]Sniffing {count} packets on {self.interface}...[/bold yellow]")
        
        def packet_callback(packet):
            console.print(packet.summary())

        try:
            sniff(iface=self.interface, prn=packet_callback, count=count)
        except Exception as e:
            console.print(f"[red]Sniffing failed: {e}[/red]")
            console.print("[yellow]Try running with sudo.[/yellow]")
