# Registry Contract

import smartpy as sp

class Registry(sp.Contract):
    def __init__(self, contract_addresses, certifier):
        self.init_type(
            sp.TRecord(
                contracts = sp.TRecord(
                    asset_provider_contract = sp.TAddress,
                    asset_twin_contract = sp.TAddress,
                    luw_contract = sp.TAddress,
                ),
                certifier = sp.TAddress
            )
        )
        self.init(
            contracts = sp.record(
                asset_provider_contract = contract_addresses.asset_provider_contract,
                asset_twin_contract = contract_addresses.asset_twin_contract,
                luw_contract = contract_addresses.luw_contract,
            ),
            certifier = certifier
        )

    @sp.entry_point
    def update_contract_address(self, contract, address):
        # Defining the parameters' types
        sp.set_type(address, sp.TAddress)

        sp.verify(self.data.certifier == sp.source, message = "Incorrect certifier")
        self.data.contracts.asset_provider_contract = address

    @sp.entry_point
    def create_asset_provider(self, provider_id, provider_data):
        # Defining the parameters' types
        sp.set_type(provider_id, sp.TString)
        sp.set_type(provider_data, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(provider_id = sp.TString, provider_data = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.contracts.asset_provider_contract, "create_asset_provider").open_some()
        
        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            provider_id = provider_id,
            provider_data = provider_data
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_provider_data(self, provider_id, provider_data):
        # Defining the parameters' types
        sp.set_type(provider_id, sp.TString)
        sp.set_type(provider_data, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(provider_id = sp.TString, provider_data = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.contracts.asset_provider_contract, "set_provider_data").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            provider_id = provider_id,
            provider_data = provider_data
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_provider_active(self, provider_id):
        # Defining the parameters' types
        sp.set_type(provider_id, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(provider_id = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.contracts.asset_provider_contract, "set_provider_active").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            provider_id = provider_id,
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_provider_deprecated(self, provider_id):
        # Defining the parameters' types
        sp.set_type(provider_id, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(provider_id = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.contracts.asset_provider_contract, "set_provider_deprecated").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            provider_id = provider_id,
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_provider_status(self, provider_id, status):
        # Defining the parameters' types
        sp.set_type(provider_id, sp.TString)
        sp.set_type(status, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(provider_id = sp.TString, status = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.contracts.asset_provider_contract, "set_provider_status").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            provider_id = provider_id,
            status = status
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_provider_owner(self, provider_id, new_owner_address):
        # Defining the parameters' types
        sp.set_type(provider_id, sp.TString)
        sp.set_type(new_owner_address, sp.TAddress)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(provider_id = sp.TString, new_owner_address = sp.TAddress)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.contracts.asset_provider_contract, "set_provider_owner").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            provider_id = provider_id,
            new_owner_address = new_owner_address
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def get_asset_provider(self, provider_id):
        # Defining the parameters' types
        sp.set_type(provider_id, sp.TString)
        
        # Defining the parameters' types
        provider = sp.view(
            "get_asset_provider",
            self.data.contracts.asset_provider_contract,
            provider_id,
            t = sp.TRecord(
                provider_id = sp.TString,
                provider_data = sp.TString,
                creator_wallet_address = sp.TAddress,
                status = sp.TString
            )
        ).open_some("Invalid view");
        
        sp.result(provider)

    @sp.entry_point
    def register_asset_twin(self, anchor_hash, provider_id, repo_end_point):
        # Defining the parameters' types
        sp.set_type(anchor_hash, sp.TString)
        sp.set_type(provider_id, sp.TString)
        sp.set_type(repo_end_point, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(anchor_hash = sp.TString, provider_id = sp.TString, repo_end_point = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.contracts.asset_twin_contract, "register").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            anchor_hash = anchor_hash,
            provider_id = provider_id,
            repo_end_point = repo_end_point,
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def change_at_calling_contract(self):
        # Only call from certifier is allowed
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")

        # Changes the calling contract address in the asset twin contract
        contract_data=sp.TAddress

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.contracts.asset_twin_contract, "change_calling_contract_address").open_some(message="Erron in loading option contract")

        # Defining the parameters that will be passed to the Storage contract
        params = sp.self_address
        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)


    @sp.onchain_view()
    def fetch_asset_twin(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.anchor_hash, sp.TString)
        sp.set_type(parameters.provider_id, sp.TString)
        
        # Defining the parameters' types
        asset_twin = sp.view(
            "fetch_asset_twin",
            self.data.contracts.asset_twin_contract,
            sp.record(
                anchor_hash = parameters.anchor_hash,
                provider_id = parameters.provider_id,
            ),
            t = sp.TRecord(
                asset_repository_endpoint = sp.TString,
                creator_wallet_address = sp.TAddress,
            )
        ).open_some("Invalid view");
        
        sp.result(asset_twin)

    @sp.entry_point
    def create_luw(self, provider_id, luw_service_endpoint):
        sp.set_type(provider_id, sp.TString)
        sp.set_type(luw_service_endpoint, sp.TAddress)

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(provider_id = sp.TString, luw_service_endpoint = sp.TAddress)

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.contracts.luw_contract, "create_luw").open_some()
        
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

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(luw_id = sp.TNat, state_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.contracts.luw_contract, "change_luw_state").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            luw_id = luw_id,
            state_id = state_id
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), luw_contract)

    @sp.entry_point
    def add_luw_repository(self, luw_id, repository_id):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(repository_id, sp.TString)

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(luw_id = sp.TNat, repository_id = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.contracts.luw_contract, "add_repository").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            luw_id = luw_id,
            repository_id = repository_id,
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), luw_contract)

    @sp.entry_point
    def change_luw_repository_state(self, luw_id, repository_id, state_id):
        sp.set_type(luw_id, sp.TNat)
        sp.set_type(repository_id, sp.TString)
        sp.set_type(state_id, sp.TNat)

        # Defining the data that we expect as a return from the Logic contract
        data_schema = sp.TRecord(luw_id = sp.TNat, repository_id = sp.TString, state_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.contracts.luw_contract, "change_repository_state").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            luw_id = luw_id,
            repository_id = repository_id,
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
            "fetch_luw",
            self.data.contracts.luw_contract,
            luw_id,
            t = sp.TRecord(
                luw_id = sp.TNat,
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

        sp.result(luw)

    @sp.onchain_view()
    def get_active_luw_state(self, luw_id):
        # Defining the parameters' types
        sp.set_type(luw_id, sp.TNat)
        
        # Defining the parameters' types
        luw_last_state = sp.view(
            "get_active_luw_state",
            self.data.contracts.luw_contract,
            luw_id,
            t = sp.TString
        ).open_some("Invalid view");

        sp.result(luw_last_state)

    @sp.onchain_view()
    def get_luw_repository_state(self, params):
        # Defining the parameters' types
        sp.set_type(params.luw_id, sp.TNat)
        sp.set_type(params.repository_id, sp.TString)
        
        repository_state = sp.view(
            "get_luw_repository_state",
            self.data.contracts.luw_contract,
            sp.record(
                luw_id = params.luw_id,
                repository_id = params.repository_id,
            ),
            t = sp.TString
        ).open_some("Invalid view");

        sp.result(repository_state)

    @sp.onchain_view()
    def get_storage_contracts(self):
        luw_contract_address = sp.view(
            "get_storage_contract",
            self.data.contracts.luw_contract,
            sp.unit,
            t = sp.TAddress
        ).open_some("Invalid view");

        provider_contract_address = sp.view(
            "get_storage_contract",
            self.data.contracts.asset_provider_contract,
            sp.unit,
            t = sp.TAddress
        ).open_some("Invalid view");

        result = sp.record(
            luw_storage_contract_address = luw_contract_address,
            provider_storage_contract_address = provider_contract_address,
            asset_twin_storage_contract_address = self.data.contracts.asset_twin_contract
        )

        sp.result(result)

@sp.add_test(name = "Registry")
def test():

    sp.add_compilation_target("registry",
        Registry(
            sp.record(
                asset_provider_contract = sp.address('KT1_contract_address'),
                asset_twin_contract = sp.address('KT1_contract_address'),
                luw_contract = sp.address('KT1_contract_address'),
            ),
            sp.address('tz1_certifier_address')
        )
    )