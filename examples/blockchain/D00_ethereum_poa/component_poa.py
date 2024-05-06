#!/usr/bin/env python3
# encoding: utf-8

from seedemu import *
from examples.internet.B03_hybrid_internet import hybrid_internet

def run(dumpfile=None, total_eth_nodes=20, total_accounts_per_node=2) -> list:
    # Create the Ethereum layer, return a list of vnodes

    emu = Emulator()

    eth = EthereumService()
    blockchain = eth.createBlockchain(chainName="POA", consensus=ConsensusMechanism.POA)

    # Change the default account balance to 1000
    mnemonic, _, _= blockchain.getEmuAccountParameters()
    blockchain.setEmuAccountParameters(mnemonic=mnemonic, balance=1000, \
            total_per_node = total_accounts_per_node)

    # Create 10 accounts, each with 100 Ethers. We will use these accounts to
    # generate background traffic (sending random transactions from them).
    words = "great amazing fun seed lab protect network system security prevent attack future"
    blockchain.setLocalAccountParameters(mnemonic=words, total=10, balance=100) 

    # These 3 accounts are generated from the following phrase:
    # "gentle always fun glass foster produce north tail security list example gain"
    # They are for users. We will use them in MetaMask, as well as in our sample code.  
    blockchain.addLocalAccount(address='0xF5406927254d2dA7F7c28A61191e3Ff1f2400fe9',
                            balance=30)
    blockchain.addLocalAccount(address='0x2e2e3a61daC1A2056d9304F79C168cD16aAa88e9', 
                            balance=9999999)
    blockchain.addLocalAccount(address='0xCBF1e330F0abD5c1ac979CF2B2B874cfD4902E24', 
                            balance=10)


    # Create the Ethereum servers. 
    vnodes_list = [] 
    signers  = []
    for i in range(total_eth_nodes):
       vnode = 'eth{}'.format(i)
       vnodes_list.append(vnode)
       e = blockchain.createNode(vnode)

       displayName = 'Ethereum-POA-%.2d'
       e.enableGethHttp()  # Enable HTTP on all nodes
       e.enableGethWs()    # Enable WebSocket on all nodes
       e.unlockAccounts()
       if i%2  == 0:
           e.startMiner()
           signers.append(vnode)
           displayName = displayName + '-Signer'
           emu.getVirtualNode(vnode).appendClassName("Signer")
       if i%3 == 0:
           e.setBootNode(True)
           displayName = displayName + '-BootNode'
           emu.getVirtualNode(vnode).appendClassName("BootNode")

       emu.getVirtualNode(vnode).setDisplayName(displayName%(i))
                
    # Create the Faucet server
    vnodes_list.append('faucet')
    faucet:FaucetServer = blockchain.createFaucetServer(
               vnode='faucet', 
               port=80, 
               linked_eth_node='eth5',
               balance=10000,
               max_fund_amount=10)

    # Add the Ethereum layer
    emu.addLayer(eth)

    if dumpfile is not None:
        emu.dump(dumpfile)
    else:
        emu.dump("component_poa.bin")

    return vnodes_list

if __name__ == "__main__":
    vlist = run()
    print(vlist)
