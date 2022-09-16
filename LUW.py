# Schema Registry Contract

import smartpy as sp

class LUW(sp.Contract):
    def __init__(self, certifier):
        self.init_type(
            sp.TRecord(
                luw_map = sp.TBigMap(
                    sp.TNat,
                    sp.TRecord(
                        creator_wallet_address = sp.TAddress,
                        provider_id = sp.TString,
                        luw_service_endpoint = sp.TAddress,
                        state_history = sp.TMap(
                            sp.TNat,
                            sp.TNat
                        ),
                        repository_endpoints = sp.TMap(
                            sp.TString,
                            sp.TNat
                        ),
                    )
                ),
                luw_last_id = sp.TNat,
                logic_contract_address = sp.TOption(sp.TAddress),
                certifier = sp.TAddress
            )
        )
        self.init(
            luw_map = sp.big_map(),
            luw_last_id = 0,
            logic_contract_address = sp.none,
            certifier = certifier
        )

    @sp.entry_point
    def add(self, provider_id, luw_service_endpoint):
        sp.set_type(provider_id, sp.TString)
        sp.set_type(luw_service_endpoint, sp.TAddress)

        # Verifying whether the calling contract address is the logic contract
        sp.verify(self.data.logic_contract_address.open_some(message="Empty logic_contract_address") == sp.sender,
                  message="Incorrect caller")

        new_luw_record = sp.record(
            creator_wallet_address = sp.source,
            provider_id = provider_id,
            luw_service_endpoint = luw_service_endpoint,
            state_history = {1: 1},
            repository_endpoints = {},
        )

        self.data.luw_map[self.data.luw_last_id] = new_luw_record
        self.data.luw_last_id += 1

    @sp.entry_point
    def add_state(self, luw_id, state_id):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(state_id, sp.TNat)

        # Verifying whether the calling contract address is the logic contract
        sp.verify(self.data.logic_contract_address.open_some(message="Empty logic_contract_address") == sp.sender,
                  message="Incorrect caller")

        sp.verify(self.data.luw_map.contains(luw_id), message = "LUW ID does not exist")

        luw = self.data.luw_map[luw_id]

        luw_new_state_key = sp.len(luw.state_history) + 1
        luw_state_history = luw.state_history

        luw_state_history[luw_new_state_key] = state_id

        new_luw_record = sp.record(
            creator_wallet_address = luw.creator_wallet_address,
            provider_id = luw.provider_id,
            luw_service_endpoint = luw.luw_service_endpoint,
            state_history = luw_state_history,
            repository_endpoints = luw.repository_endpoints
        )

        self.data.luw_map[luw_id] = new_luw_record

    @sp.entry_point
    def add_repository(self, luw_id, repository_id, state_id = 1):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(repository_id, sp.TString)
        sp.set_type(state_id, sp.TNat)

        # Verifying whether the calling contract address is the logic contract
        sp.verify(self.data.logic_contract_address.open_some(message="Empty logic_contract_address") == sp.sender,
                  message="Incorrect caller")

        sp.verify(self.data.luw_map.contains(luw_id), message = "LUW ID does not exist")

        luw = self.data.luw_map[luw_id]

        luw_repository_endpoints = luw.repository_endpoints

        sp.verify(luw_repository_endpoints.contains(repository_id) == False, message = "Repository ID already exists")

        luw_repository_endpoints[repository_id] = state_id

        new_luw_record = sp.record(
            creator_wallet_address = luw.creator_wallet_address,
            provider_id = luw.provider_id,
            luw_service_endpoint = luw.luw_service_endpoint,
            state_history = luw.state_history,
            repository_endpoints = luw_repository_endpoints
        )

        self.data.luw_map[luw_id] = new_luw_record

    @sp.entry_point
    def change_repository_state(self, luw_id, repository_id, state_id):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(repository_id, sp.TString)
        sp.set_type(state_id, sp.TNat)

        # Verifying whether the calling contract address is the logic contract
        sp.verify(self.data.logic_contract_address.open_some(message="Empty logic_contract_address") == sp.sender,
                  message="Incorrect caller")

        sp.verify(self.data.luw_map.contains(luw_id), message = "LUW ID does not exist")

        luw = self.data.luw_map[luw_id]

        luw_repository_endpoints = luw.repository_endpoints

        luw_repository_endpoints[repository_id] = state_id

        new_luw_record = sp.record(
            creator_wallet_address = luw.creator_wallet_address,
            provider_id = luw.provider_id,
            luw_service_endpoint = luw.luw_service_endpoint,
            state_history = luw.state_history,
            repository_endpoints = luw_repository_endpoints
        )

        self.data.luw_map[luw_id] = new_luw_record


    @sp.entry_point
    def change_logic_contract_address(self, new_logic_contract_address):
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")

        # Update logic contract address
        self.data.logic_contract_address = sp.some(new_logic_contract_address)


    @sp.onchain_view()
    def fetch(self, luw_id):
        sp.result(self.data.luw_map[luw_id])

    @sp.onchain_view()
    def get_active_luw_state(self, luw_id):
        sp.set_type(luw_id, sp.TNat)
        
        luw = self.data.luw_map[luw_id]
        last_state = luw.state_history[sp.len(luw.state_history)]
        sp.result(last_state)

    @sp.onchain_view()
    def get_luw_owner_address(self, luw_id):
        sp.result(self.data.luw_map[luw_id].creator_wallet_address)

    @sp.onchain_view()
    def get_luw_repositories(self, luw_id):
        sp.result(self.data.luw_map[luw_id].repository_endpoints)

    @sp.onchain_view()
    def get_luw_repository_state(self, params):
        sp.result(self.data.luw_map[params.luw_id].repository_endpoints[params.repository_id])

@sp.add_test(name = "LUW")
def test():
    sp.add_compilation_target("luw",
        LUW(sp.address('tz1_certifier_address'))
    )
