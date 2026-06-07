"""Network scanner for host and port discovery"""

import nmap
import socket
from typing import List, Dict

class NetworkScanner:
    """Performs network scanning and reconnaissance"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def scan_host(self, host: str, ports: str = "1-65535") -> Dict:
        """Scan a single host for open ports"""
        try:
            self.nm.scan(host, ports)
            return self.nm[host].all_tcp()
        except Exception as e:
            return {"error": str(e)}
    
    def scan_network(self, network: str) -> List[str]:
        """Scan a network for active hosts"""
        active_hosts = []
        try:
            self.nm.scan(network, arguments="-sn")
            for host in self.nm.all_hosts():
                if self.nm[host].state() == "up":
                    active_hosts.append(host)
        except Exception as e:
            print(f"Error scanning network: {e}")
        return active_hosts
