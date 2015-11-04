import sh

class FirewallConfigurer:
    def __init__(self, firewall_binary):
        self.firewall_binary = firewall_binary

    def open_ports(self, ports):
        pass

    def close_ports(self, ports):
        pass


class IptablesConfigurer(FirewallConfigurer):
    MAX_PORTS = 15
    # iptables -A INPUT -p tcp -m multiport --dports "22,443,80,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16" -j ACCEPT
    def open_ports(self, ports):
        print 'ports input: ', str(ports)
        for chunk in chunks(ports, self.MAX_PORTS):
            print 'chunk: ', str(chunk)
            sh.iptables(A='INPUT', p='tcp', m='multiport', dports='"'+str(chunk)[1:-1]+'"', j='ACCEPT')

class FirewalldConfigurer(FirewallConfigurer):
    pass

def chunks(iterable, chunk_size):
    for i in xrange(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]


if __name__ == '__main__':
    c = IptablesConfigurer(firewall_binary='asd')
    c.open_ports([22,80,666])
