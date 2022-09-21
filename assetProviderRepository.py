# Schema Registry Contract

import smartpy as sp

class AssetProviderRepository(sp.Contract):
    def __init__(self, storage_contract, certifier):
        self.init_type(
            sp.TRecord(
                storage_contract = sp.TAddress,
                certifier = sp.TAddress,
                provider_statuses = sp.TBigMap(
                    sp.TNat,
                    sp.TString
                ),
            )
        )
        self.init(
            storage_contract = storage_contract,
            provider_statuses = sp.big_map({
                1: "active",
                2: "deprecated"
            }),
            certifier = certifier
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

    # Verify Provider existence
    def verify_provider_exists(self, provider_id):
        provider_existance = sp.view(
            "verify_provider_exists",
            self.data.storage_contract,
            provider_id,
            t = sp.TBool
        ).open_some("Invalid view");

        return provider_existance

    # Get Provider owner address
    def get_provider_owner_address(self, provider_id):
        provider_owner_address = sp.view(
            "get_provider_owner_address",
            self.data.storage_contract,
            provider_id,
            t = sp.TAddress
        ).open_some("Invalid view");

        return provider_owner_address

    @sp.entry_point
    def create_asset_provider(self, provider_id, provider_data):
        sp.set_type(provider_id, sp.TString)
        sp.set_type(provider_data, sp.TString)

        # Check if provider does not exist, does not allow add call otherwise
        sp.verify(~self.verify_provider_exists(provider_id), message = "Provider ID already exists")

        data_schema = sp.TRecord(
            provider_id = sp.TString,
            provider_data = sp.TString,
            status = sp.TNat,
            creator_wallet_address = sp.TAddress,
        )

        # Defining the Logic contract itself and its entry point for the call
        storage_contract = sp.contract(data_schema, self.data.storage_contract, "create_asset_provider").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_id = provider_id,
            provider_data = provider_data,
            status = 1,
            creator_wallet_address = sp.source,
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.entry_point
    def set_provider_active(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)

        # Update is allowed only from owner
        owner_address = self.get_provider_owner_address(parameters.provider_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Non-matching owner address")

        # Defining the data expected by the Storage contract
        contract_data = sp.TRecord(provider_id = sp.TString, status = sp.TNat)

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.storage_contract, "change_status").open_some()

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_id = parameters.provider_id,
            status = 1
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.entry_point
    def set_provider_deprecated(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)

        # Update is allowed only from owner
        owner_address = self.get_provider_owner_address(parameters.provider_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Non-matching owner address")

        # Defining the data expected by the Storage contract
        contract_data = sp.TRecord(provider_id = sp.TString, status = sp.TNat)

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.storage_contract, "change_status").open_some()

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_id = parameters.provider_id,
            status = 2
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.entry_point
    def set_provider_status(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.status, sp.TNat)

        # Update is allowed only from owner
        owner_address = self.get_provider_owner_address(parameters.provider_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Non-matching owner address")

        # Defining the data expected by the Storage contract
        contract_data = sp.TRecord(provider_id = sp.TString, status = sp.TNat)

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.storage_contract, "change_status").open_some()

        # Verify status ID exists
        sp.verify(self.data.provider_statuses.contains(parameters.status), message = "Incorrect status")

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_id = parameters.provider_id,
            status = parameters.status
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.entry_point
    def set_provider_data(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.provider_data, sp.TString)

        # Check if provider exists, does not allow call otherwise
        sp.verify(self.verify_provider_exists(parameters.provider_id), message = "Provider ID does not exist")

        # Update is allowed only from owner
        owner_address = self.get_provider_owner_address(parameters.provider_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Non-matching owner address")

        # Defining the data expected by the Storage contract
        contract_data = sp.TRecord(provider_id = sp.TString, provider_data = sp.TString)

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.storage_contract, "change_data").open_some()

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_id = parameters.provider_id,
            provider_data = parameters.provider_data,
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.entry_point
    def set_provider_owner(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.new_owner_address, sp.TAddress)

        # Update is allowed only from owner
        owner_address = self.get_provider_owner_address(parameters.provider_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Non-matching owner address")

        # Defining the data expected by the Storage contract
        contract_data = sp.TRecord(provider_id = sp.TString, new_owner_address = sp.TAddress)

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.storage_contract, "change_owner").open_some()

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_id = parameters.provider_id,
            new_owner_address = parameters.new_owner_address
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.entry_point
    def update_storage_contract_with_address(self):
        # Update is allowed only from certifier
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")

        # Defining the data expected by the Storage contract
        contract_data = sp.TAddress

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.storage_contract, "change_logic_contract_address").open_some()

        # The contract's own address will be passed as a parameter
        logic_contract_adrress = sp.self_address

        # Calling the Storage contract with the parameters we defined
        sp.transfer(logic_contract_adrress, sp.mutez(0), storage_contract)

    @sp.onchain_view()
    def get_asset_provider(self, provider_id):
        # Defining the parameters' types
        sp.set_type(provider_id, sp.TString)
        
        # Defining the parameters' types
        provider = sp.view(
            "get_asset_provider",
            self.data.storage_contract,
            provider_id,
            t = sp.TRecord(
                provider_id = sp.TString,
                provider_data = sp.TString,
                status = sp.TNat,
                creator_wallet_address = sp.TAddress,
            )
        ).open_some("Invalid view");

        # Format result
        result_provider = sp.record(
            provider_id = provider_id,
            provider_data = provider.provider_data,
            status = self.data.provider_statuses[provider.status],
            creator_wallet_address = provider.creator_wallet_address,
        )

        # Calling the Storage contract with the parameters we defined
        sp.result(result_provider)

    @sp.onchain_view()
    def get_storage_contract(self):
        sp.result(self.data.storage_contract)

@sp.add_test(name = "AssetProviderRepository")
def test():
    sp.add_compilation_target("assetProviderRepository",
        AssetProviderRepository(sp.address("KT1_contract_address"),
            sp.address('tz1_certifier_address'))
    )
