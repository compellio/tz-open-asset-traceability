# Schema Registry Contract

import smartpy as sp

class LUWRepository(sp.Contract):
    def __init__(self, luw_contract):
        self.init_type(
            sp.TRecord(
                luw_contract = sp.TAddress,
                states = sp.TBigMap(
                    sp.TNat,
                    sp.TString
                ),
            )
        )
        self.init(
            luw_contract = luw_contract,
            states = sp.big_map({
                1: "active",
                2: "prepare_to_commit",
                3: "commited",
                4: "aborted"
            }),
        )

    ###########
    # Helpers #
    ###########

    # Verify source of transaction is owner or certifier
    @sp.private_lambda(with_storage="read-only")
    def verify_owner_source_address(self, params):
        sp.set_type(params.owner_address, sp.TAddress)

        sp.if (sp.source == params.owner_address):
            sp.result(True)
        sp.else:
            sp.result(False)

    # Get LUW owner address
    def get_luw_owner_address(self, luw_id):
        luw_owner_address = sp.view(
            "get_luw_owner_address",
            self.data.luw_contract,
            luw_id,
            t = sp.TAddress
        ).open_some("Invalid view");

        return luw_owner_address

    #############################
    # Repo Entry points / Views #
    #############################

    @sp.entry_point
    def create_luw(self, provider_id, luw_service_endpoint):
        sp.set_type(provider_id, sp.TString)
        sp.set_type(luw_service_endpoint, sp.TString)

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(provider_id = sp.TString, luw_service_endpoint = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.luw_contract, "add").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_id = provider_id,
            luw_service_endpoint = luw_service_endpoint
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), luw_contract)

    @sp.entry_point
    def change_luw_state(self, luw_id, state_id):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(state_id, sp.TNat)

        sp.verify(self.data.states.contains(state_id), message = "Incorrect state ID")

        owner_address = self.get_luw_owner_address(luw_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(luw_id = sp.TNat, state_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.luw_contract, "add_state").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            luw_id = luw_id,
            state_id = state_id
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), luw_contract)

    @sp.onchain_view()
    def fetch_luw(self, luw_id):
        # Defining the parameters' types
        sp.set_type(luw_id, sp.TNat)
        
        # Defining the parameters' types
        luw = sp.view(
            "fetch",
            self.data.luw_contract,
            luw_id,
            t = sp.TRecord(
                creator_wallet_address = sp.TAddress,
                provider_id = sp.TString,
                service_endpoint = sp.TString,
                state_history = sp.TMap(
                    sp.TNat,
                    sp.TNat
                ),
            )
        ).open_some("Invalid view");

        formatted_state_history = {}

        sp.for x in luw.state_history.items():
            current_len = sp.len(formatted_state_history)
            formatted_state_history[current_len] = self.data.states[x]

        formatted_luw = sp.record(
            creator_wallet_address = luw.creator_wallet_address,
            provider_id = luw.provider_id,
            service_endpoint = luw.service_endpoint,
            state_history = formatted_state_history,
        )

        sp.result(luw)

    @sp.onchain_view()
    def get_active_state(self, luw_id):
        # Defining the parameters' types
        sp.set_type(luw_id, sp.TNat)
        
        # Defining the parameters' types
        luw_last_state_id = sp.view(
            "get_active_state",
            self.data.luw_contract,
            luw_id,
            t = sp.TNat
        ).open_some("Invalid view");

        formatted_state = self.data.states[luw_last_state_id]

        sp.result(formatted_state)

@sp.add_test(name = "LUWRepository")
def test():
    sp.add_compilation_target("luwRepository",
        LUWRepository(sp.address("KT1MWPUKoU4FUVr1nBA4cwjMSoSsxqE3x9kc"))
    )
