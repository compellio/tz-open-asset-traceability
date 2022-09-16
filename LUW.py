# Schema Registry Contract

import smartpy as sp

class LUW(sp.Contract):
    def __init__(self):
        self.init_type(
            sp.TRecord(
                luw_map = sp.TBigMap(
                    sp.TNat,
                    sp.TRecord(
                        creator_wallet_address = sp.TAddress,
                        provider_id = sp.TString,
                        service_endpoint = sp.TString,
                        state_history = sp.TMap(
                            sp.TNat,
                            sp.TNat
                        ),
                    )
                ),
                luw_last_id = sp.TNat,
            )
        )
        self.init(
            luw_map = sp.big_map(),
            luw_last_id = 0,
        )

    @sp.entry_point
    def add(self, provider_id, luw_service_endpoint):
        sp.set_type(provider_id, sp.TString)
        sp.set_type(luw_service_endpoint, sp.TString)

        new_luw_record = sp.record(
            creator_wallet_address = sp.source,
            provider_id = provider_id,
            service_endpoint = luw_service_endpoint,
            state_history = {1: 1},
        )

        self.data.luw_map[self.data.luw_last_id] = new_luw_record
        self.data.luw_last_id += 1

    @sp.entry_point
    def add_state(self, luw_id, state_id):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(state_id, sp.TNat)

        sp.verify(self.data.luw_map.contains(luw_id), message = "LUW ID does not exist")

        luw = self.data.luw_map[luw_id]

        luw_new_state_key = sp.len(luw.state_history) + 1
        luw_state_history = luw.state_history

        luw_state_history[luw_new_state_key] = state_id

        new_luw_record = sp.record(
            creator_wallet_address = luw.creator_wallet_address,
            provider_id = luw.provider_id,
            service_endpoint = luw.service_endpoint,
            state_history = luw_state_history
        )

        self.data.luw_map[luw_id] = new_luw_record

    @sp.onchain_view()
    def fetch(self, luw_id):
        sp.verify(self.data.luw_map.contains(luw_id), message = "LUW ID does not exist")

        sp.result(self.data.luw_map[luw_id])

    @sp.onchain_view()
    def get_active_state(self, luw_id):
        sp.set_type(luw_id, sp.TNat)
        sp.verify(self.data.luw_map.contains(luw_id), message = "LUW ID does not exist")
        
        luw = self.data.luw_map[luw_id]
        last_state = luw.state_history[sp.len(luw.state_history)]
        sp.result(last_state)

    @sp.onchain_view()
    def get_luw_owner_address(self, luw_id):
        sp.verify(self.data.luw_map.contains(luw_id), message = "LUW ID does not exist")
        sp.result(self.data.luw_map[luw_id].creator_wallet_address)

@sp.add_test(name = "LUW")
def test():
    sp.add_compilation_target("luw",
        LUW()
    )
