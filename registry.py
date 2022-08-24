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

@sp.add_test(name = "Registry")
def test():

    sp.add_compilation_target("registry",
        Registry(
            sp.record(
                asset_provider_contract = 'KT1_provider_address',
                asset_twin_contract = 'KT1_twin_address',
                luw_contract = 'KT1_luw_address',
            ),
            sp.address('tz1_certifier_address')
        )
    )