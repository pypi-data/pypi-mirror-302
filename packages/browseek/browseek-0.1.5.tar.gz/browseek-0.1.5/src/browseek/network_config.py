from typing import Dict, Any
from . import DNS_OVER_HTTPS

class NetworkConfig:
    def __init__(self, vpn_config: Dict[str, Any] = None, speed_limit: int = None):
        """Initialize network configuration."""
        self.vpn_config = vpn_config
        self.speed_limit = speed_limit
        self.dns_over_https = DNS_OVER_HTTPS
