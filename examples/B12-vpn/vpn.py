
vpn = VPNService()

vpn.install('vpn-server')

emu.addBinding(Binding('vpn-server', filter=Filter(asn=151), action=Action.FIRST))


