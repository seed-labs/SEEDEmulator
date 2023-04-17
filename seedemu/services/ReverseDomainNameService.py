# This service is not used by any official examples. 
# It has not been fully tested.

from .DomainNameService import DomainNameService, DomainNameServer
from seedemu.core import Node, Emulator, Service, Server


class ReverseDomainNameServer(Server):
    """!
    @brief Reverse DNS server. 
    """

    def install(self, node: Node, service: Service, emulator: Emulator):
        """
        @brief Overriding this method is mandatory. 
        """
        pass


class ReverseDomainNameService(Service):
    """!
    @brief Reverse DNS. This service hosts the in-addr.arpa. zone and resolve
    IP addresses to nodename-netname.nodetype.asn.net.

    In the current implementation, this is not a real service, 
    i.e., it does not have its own server. The purpose of 
    this service (layer) is to modify the zone information 
    in the DNS service. 

    This is not a recommended practice, because cross-layer modification
    is not a good idea. 
    """

    __dns: DomainNameService

    def __init__(self):
        """!
        @brief ReverseDomainNameService constructor
        """
        super().__init__()
        self.addDependency('DomainNameService', True, False)
        self.addDependency('Base', False, False)

    def getName(self) -> str:
        return 'ReverseDomainNameService'

    def _createServer(self) -> Server:
        return ReverseDomainNameServer()

    def install(self, vnode: str) -> Server:
        assert False, 'ReverseDomainNameService is not a real service and should not be installed this way. Please install a DomainNameService on the node and host the zone "in-addr.arpa." yourself.'

    def configure(self, emulator: Emulator):
        reg = emulator.getRegistry()

        self._log('Creating "in-addr.arpa." zone...')
        self.__dns = reg.get('seedemu', 'layer', 'DomainNameService')
        zone = self.__dns.getZone('in-addr.arpa.')

        self._log('Collecting IP addresses...')
        for ([scope, type, name], obj) in reg.getAll().items():
            if type != 'rnode' and type != 'hnode': continue
            self._log('Collecting {}/{}/{}...'.format(scope, type, name))

            if scope == 'ix':
                scope = name
                name = 'rs'
            else: scope = 'as' + scope

            node: Node = obj
            for iface in node.getInterfaces():
                addr = '.'.join(reversed(str(iface.getAddress()).split('.')))
                netname = iface.getNet().getName()
                record = '{} PTR {}-{}.{}.{}.net.'.format(addr, name, netname, type, scope).replace('_', '-')
                zone.addRecord(record)

        return super().configure(emulator)

    def print(self, indent: int) -> str:
        out = ' ' * indent
        out += 'ReverseDomainNameService\n'

        return out
    
