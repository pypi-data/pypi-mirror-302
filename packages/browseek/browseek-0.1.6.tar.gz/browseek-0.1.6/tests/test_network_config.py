import unittest

from browseek import NetworkConfig

class TestNetworkConfig(unittest.TestCase):
    def test_network_config_initialization(self):
        vpn_config = {
            "provider": "nordvpn",
            "country": "us"
        }
        speed_limit = 1000000

        config = NetworkConfig(vpn_config, speed_limit)

        self.assertEqual(config.vpn_config, vpn_config)
        self.assertEqual(config.speed_limit, speed_limit)

if __name__ == '__main__':
    unittest.main()
