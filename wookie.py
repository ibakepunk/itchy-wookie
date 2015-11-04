from subprocess import check_call, CalledProcessError

from args_parser import parser


class FirewallConfigurer:
    def __init__(self, firewall_binary):
        self.firewall_binary = firewall_binary

    def open_ports(self, ports):
        pass

    def close_ports(self, ports):
        pass

    def clear_rules(self):
        pass


class IptablesConfigurer(FirewallConfigurer):
    MAX_PORTS = 15

    # iptables -A INPUT -p tcp -m multiport --dports "22,443,80,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16" -j ACCEPT
    def open_ports(self, ports):
        for chunk in chunks(ports, self.MAX_PORTS):
            try:
                check_call([self.firewall_binary,
                            '-A', 'INPUT',
                            '-p', 'tcp',
                            '-m', 'multiport',
                            '--dports', str(chunk)[1:-1],
                            '-j', 'ACCEPT'])
            except CalledProcessError as e:
                print e
                exit(e.returncode)

    def close_ports(self, ports):
        for chunk in chunks(ports, self.MAX_PORTS):
            try:
                check_call([self.firewall_binary,
                            '-A', 'INPUT',
                            '-p', 'tcp',
                            '-m', 'multiport',
                            '--dports', str(chunk)[1:-1],
                            '-j', 'DROP'])
            except CalledProcessError as e:
                print e
                exit(e.returncode)

    def clear_rules(self):
        try:
            check_call([self.firewall_binary, '--flush'])
        except CalledProcessError as e:
            print e
            exit(e.returncode)


class FirewalldConfigurer(FirewallConfigurer):
    pass


def chunks(iterable, chunk_size):
    for i in xrange(0, len(iterable), chunk_size):
        yield iterable[i:i + chunk_size]


if __name__ == '__main__':
    args = parser.parse_args()
    c = IptablesConfigurer(firewall_binary='/sbin/iptables')
    if args.action == 'clear':
        c.clear_rules()
    elif args.action == 'open':
        c.open_ports(args.ports)
    elif args.action == 'close':
        c.close_ports(args.ports)
