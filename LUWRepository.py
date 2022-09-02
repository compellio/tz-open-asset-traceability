# Schema Registry Contract

import smartpy as sp

class LUWRepository(sp.Contract):
    def __init__(self, luw_contract, certifier):
        self.init_type(
            sp.TRecord(
                luw_contract = sp.TAddress,
                certifier = sp.TAddress,
                states = sp.TBigMap(
                    sp.TNat,
                    sp.TString
                ),
                repo_states = sp.TBigMap(
                    sp.TNat,
                    sp.TString
                ),
            )
        )
        self.init(
            luw_contract = luw_contract,
            certifier = certifier,
            states = sp.big_map({
                1: "active",
                2: "prepare_to_commit",
                3: "commited",
                4: "aborted"
            }),
            repo_states = sp.big_map({
                1: "open",
                2: "ready",
                3: "commited",
                4: "rollbacked"
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

    # Verify state of LUW is active
    @sp.private_lambda(with_storage="read-only")
    def verify_luw_active(self, params):
        sp.set_type(params.luw_state_id, sp.TNat)

        sp.if (params.luw_state_id == 1):
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

    # Get LUW active state
    def get_luw_state(self, luw_id):
        luw_last_state_id = sp.view(
            "get_active_luw_state",
            self.data.luw_contract,
            luw_id,
            t = sp.TNat
        ).open_some("Invalid view");

        return luw_last_state_id

    # Get LUW repositories
    def get_luw_repositories(self, luw_id):
        luw_repositories = sp.view(
            "get_luw_repositories",
            self.data.luw_contract,
            luw_id,
            t = sp.TMap(
                sp.TString,
                sp.TNat
            )
        ).open_some("Invalid view");

        return luw_repositories

    #############################
    # Repo Entry points / Views #
    #############################

    @sp.entry_point
    def create_luw(self, provider_id, luw_service_endpoint):
        sp.set_type(provider_id, sp.TString)
        sp.set_type(luw_service_endpoint, sp.TAddress)

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(provider_id = sp.TString, luw_service_endpoint = sp.TAddress)

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

    @sp.entry_point
    def add_repository(self, luw_id, repository_id):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(repository_id, sp.TString)

        owner_address = self.get_luw_owner_address(luw_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

        luw_state_id = self.get_luw_state(luw_id)
        sp.verify(self.verify_luw_active(
            sp.record(
                luw_state_id = luw_state_id,
            )
        ), message = "LUW is not Active")

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(luw_id = sp.TNat, repository_id = sp.TString, state_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.luw_contract, "add_repository").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            luw_id = luw_id,
            repository_id = repository_id,
            state_id = 1
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), luw_contract)

    @sp.entry_point
    def change_repository_state(self, luw_id, repository_id, state_id):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(repository_id, sp.TString)
        sp.set_type(state_id, sp.TNat)

        owner_address = self.get_luw_owner_address(luw_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

        luw_repositories = self.get_luw_repositories(luw_id)
        sp.verify(luw_repositories.contains(repository_id), message = "Repository ID does not exist")

        # Verify state ID exists
        sp.verify(self.data.repo_states.contains(state_id), message = "Incorrect state")

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(luw_id = sp.TNat, repository_id = sp.TString, state_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.luw_contract, "change_repository_state").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            luw_id = luw_id,
            repository_id = repository_id,
            state_id = state_id
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), luw_contract)

    @sp.entry_point
    def update_storage_contract_with_address(self):
        # Update is allowed only from certifier
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")

        # Defining the data expected by the Storage contract
        contract_data = sp.TAddress

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.luw_contract, "change_logic_contract_address").open_some()

        # The contract's own address will be passed as a parameter
        logic_contract_adrress = sp.self_address

        # Calling the Storage contract with the parameters we defined
        sp.transfer(logic_contract_adrress, sp.mutez(0), storage_contract)



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
        ).open_some("Invalid view");

        formatted_state_history = {}

        sp.for x in luw.state_history.items():
            current_len = sp.len(formatted_state_history)
            formatted_state_history[current_len] = self.data.states[x]

        formatted_luw = sp.record(
            creator_wallet_address = luw.creator_wallet_address,
            provider_id = luw.provider_id,
            luw_service_endpoint = luw.luw_service_endpoint,
            state_history = formatted_state_history,
            repository_endpoints = luw.repository_endpoints
        )

        sp.result(luw)

    @sp.onchain_view()
    def get_active_luw_state(self, luw_id):
        # Defining the parameters' types
        sp.set_type(luw_id, sp.TNat)
        
        # Defining the parameters' types
        luw_last_state_id = sp.view(
            "get_active_luw_state",
            self.data.luw_contract,
            luw_id,
            t = sp.TNat
        ).open_some("Invalid view");

        formatted_state = self.data.states[luw_last_state_id]

        sp.result(formatted_state)

    @sp.onchain_view()
    def get_luw_repository_state(self, params):
        # Defining the parameters' types
        sp.set_type(params.luw_id, sp.TNat)
        sp.set_type(params.repository_id, sp.TString)
        
        repository_state_id = sp.view(
            "get_luw_repository_state",
            self.data.luw_contract,
            sp.record(
                luw_id = params.luw_id,
                repository_id = params.repository_id,
            ),
            t = sp.TNat
        ).open_some("Invalid view");

        formatted_state = self.data.repo_states[repository_state_id]

        sp.result(formatted_state)

@sp.add_test(name = "LUWRepository")
def test():
    sp.add_compilation_target("luwRepository",
        LUWRepository(sp.address("KT1_contract_address"),sp.address('tz1_certifier_address'))
    )
