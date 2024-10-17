from ttlinks.ipservice.ip_configs import IPv4WildCardConfig, IPv4SubnetConfig
from ttlinks.protocol_stack.network_layer.ICMP.icmp_manager import ICMPPingManager

if __name__ == '__main__':
    manager = ICMPPingManager()
    ips = IPv4SubnetConfig('8.8.8.8/31').get_hosts()
    responses = manager.ping_multiple(ips, timeout=2, interval=1, count=2, verbose=True)
    print(responses)