#!/usr/bin/env python2
# Copyright (c) 2018 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, start_nodes

# Test wallet address behaviour across network upgradesa\
class WalletAddressesTest(BitcoinTestFramework):

    def setup_nodes(self):
        return start_nodes(4, self.options.tmpdir, [[
            '-nuparams=5ba81b19:202', # Overwinter
            '-nuparams=76b809bb:204', # Sapling
        ]] * 4)

    def run_test(self):
        def addr_checks(default_type):
            # Check default type
            addr = self.nodes[0].z_getnewaddress()
            res = self.nodes[0].z_validateaddress(addr)
            assert(res['isvalid'])
            assert(res['ismine'])
            assert_equal(res['type'], default_type)
            assert(addr in self.nodes[0].z_listaddresses())

            # Check explicit Sprout type
            addr = self.nodes[0].z_getnewaddress('sprout')
            res = self.nodes[0].z_validateaddress(addr)
            assert(res['isvalid'])
            assert(res['ismine'])
            assert_equal(res['type'], 'sprout')
            assert(addr in self.nodes[0].z_listaddresses())

            # Check explicit Sapling type
            addr = self.nodes[0].z_getnewaddress('sapling')
            res = self.nodes[0].z_validateaddress(addr)
            assert(res['isvalid'])
            assert(res['ismine'])
            assert_equal(res['type'], 'sapling')
            assert(addr in self.nodes[0].z_listaddresses())

        # Sanity-check the test harness
        assert_equal(self.nodes[0].getblockcount(), 200)

        # Current height = 200 -> Sprout
        # Default address type is Sprout
        print "Testing height 200 (Sprout)"
        addr_checks('sprout')

        self.nodes[0].generate(1)
        self.sync_all()

        # Current height = 201 -> Sprout
        # Default address type is Sprout
        print "Testing height 201 (Sprout)"
        addr_checks('sprout')

        self.nodes[0].generate(1)
        self.sync_all()

        # Current height = 202 -> Overwinter
        # Default address type is Sprout
        print "Testing height 202 (Overwinter)"
        addr_checks('sprout')

        self.nodes[0].generate(1)
        self.sync_all()

        # Current height = 203 -> Overwinter
        # Default address type is Sprout
        print "Testing height 203 (Overwinter)"
        addr_checks('sprout')

        self.nodes[0].generate(1)
        self.sync_all()

        # Current height = 204 -> Sapling
        # Default address type is Sprout
        print "Testing height 204 (Sapling)"
        addr_checks('sprout')

if __name__ == '__main__':
    WalletAddressesTest().main()
