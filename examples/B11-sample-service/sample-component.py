#!/usr/bin/env python3
# encoding: utf-8

from seedemu.core import Emulator, Binding, Filter, Action
from seedemu.services import SampleService
from seedemu.compiler import Docker


emu = Emulator()
emu.load('../B00-mini-internet/base-component.bin')

###########################################################
# Create a service layer
sample = SampleService()

# Create two servers
sample.install('sample-server-1')
sample.install('sample-server-2')

# Customize the display names (for visualization purpose)
emu.getVirtualNode('sample-server-1').setDisplayName('Sample-1')
emu.getVirtualNode('sample-server-2').setDisplayName('Sample-2')

emu.addBinding(Binding('sample-server-1', filter=Filter(asn=151), action=Action.FIRST))
emu.addBinding(Binding('sample-server-2', filter=Filter(asn=161), action=Action.FIRST))

###########################################################
emu.addLayer(sample)

#emu.dump('sample-component.bin')

emu.render()
emu.compile(Docker(), './output')

