from __future__ import annotations
from seedemu import *

class SampleServer(Server):
    """!
    @brief The sample server class
    """

    def __init__(self):
        """!
        @brief Constructor.
        """
        super().__init__()

    def configure(self, node:Node, service: SampleService, emulator: Emulator):
        """!
        @brief configure the server if needed. If configuration is not 
        needed, there is no need to override this method from the Server class. 

        It is invoked by Service::_doConfigure()
        See a complicated example in DomainNameServer. 
        """
        
        # This example shows how to get the IP address of the node
        ifaces = node.getInterfaces()
        assert len(ifaces) > 0, 'SampleServer::configure(): node has no interface'
        addr = ifaces[0].getAddress()
       
        # In some cases, the information from this server is needed for
        # other servers. We will call Service APIs to store the information
        # in the service object, so other servers can use it.

        return 

    def install(self, node: Node, service: Service, emulator: Emulator):
        """!
        @brief Install the service. This method must be implemented. 

        It is invoked by Service::_doInstall()
        """
        
        # Install software 
        node.addSoftware('openvpn')

        # Set files (e.g., configuration files for the software)
        node.setFile('/tmp/hello', "hello")

        # Add commands to the start script 
        node.appendStartCommand('echo Hello')


        # Add the class label 
        node.appendClassName("SampleService")

    
    def print(self, indent: int) -> str:
        out = ' ' * indent
        out += 'Sample server object.\n'

        return out


class SampleService(Service):
    """!
    @brief The sample service class.
    """

    def __init__(self):
        """!
        @brief constructor
        """

        super().__init__()


    def _createServer(self) -> Server:
        """!
        @brief Create a server.

        Invoked by Service::install() to install a service on a virtual node.

        All services must implement this method. This call takes no parameter,
        and should create and return an instance of the Server of the Service.
        This instance will eventually be returned to the user.
        """

        return SampleServer()


    def _doConfigure(self, node: Node, server: Server, emulator: Emulator):
        """!
        @brief configure the node. If a service needs to do additional 
        configuration beyond the ones defined in the super class, it 
        can override this method. This is optional. 

        @param node physical node. When this is called,  the virtual node
        for the server is already bound to a physical node.
        @param server server.
        @param emulator the instance of the emulator.
        """

        # Do service-wide configuration here if necessary; otherwise,
        # there is no need to override this method from the Service class.


        # Always invoke the super-class's _doConfigure(), 
        # which will invoke server.configure(node, self, emulator)
        super()._doConfigure(node, server, emulator)


    def _doInstall(self, node: Node, server: Server, emulator: Emulator):
        """!
        @brief install the server on node. This can be overridden by service
        implementations.

        @param node node.
        @param server server.
        """

        # Do service-wide installation here if necessary; otherwise,
        # there is no need to override this method from the Service class
        # ...

        # Always invoke the super-class's _doInstall(), 
        # which will invoke server.install(node, self, emulator)
        super()._doInstall(node, server, emulator)


    def getName(self) -> str:
        return 'SampleService'

    def print(self, indent: int) -> str:
        out = ' ' * indent
        out += 'SampleServiceLayer\n'

        return out
