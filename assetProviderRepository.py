# Schema Registry Contract

import smartpy as sp

class AssetProviderRepository(sp.Contract):
    def __init__(self, data_contract):
        self.init_type(
            sp.TRecord(
                data_contract = sp.TAddress,
                provider_statuses = sp.TBigMap(
                    sp.TNat,
                    sp.TString
                ),
            )
        )
        self.init(
            data_contract = data_contract,
            provider_statuses = sp.big_map({
                1: "active",
                2: "deprecated",
                3: "in_conflict",
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

    # Verify Provider existence
    def check_provider_exists(self, provider_did):
        provider_existance = sp.view(
            "verify_provider_exists",
            self.data.data_contract,
            provider_did,
            t = sp.TBool
        ).open_some("Invalid view");

        return provider_existance

    # Get Provider owner address
    def get_provider_owner_address(self, provider_did):
        provider_owner_address = sp.view(
            "get_provider_owner_address",
            self.data.data_contract,
            provider_did,
            t = sp.TAddress
        ).open_some("Invalid view");

        return provider_owner_address

    #############################
    # Repo Entry points / Views #
    #############################

    @sp.entry_point
    def create_asset_provider(self, provider_did, provider_data):
        sp.set_type(provider_did, sp.TString)
        sp.set_type(provider_data, sp.TString)

        # Check if provider does not exist, does not allow add call otherwise
        sp.verify(self.check_provider_exists(provider_did) == sp.bool(False), message = "Provider did already exists")

        data_schema = sp.TRecord(
            provider_did = sp.TString,
            provider_data = sp.TString,
            status = sp.TNat,
            creator_wallet_address = sp.TAddress,
        )

        # Defining the Logic contract itself and its entry point for the call
        data_contract = sp.contract(data_schema, self.data.data_contract, "create_asset_provider").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_did = provider_did,
            provider_data = provider_data,
            status = 1,
            creator_wallet_address = sp.source,
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), data_contract)

    @sp.entry_point
    def set_provider_active(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_did, sp.TString)

        # Update is allowed only from owner
        owner_address = self.get_provider_owner_address(parameters.provider_did)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

        # Defining the data expected by the Storage contract
        contract_data = sp.TRecord(provider_did = sp.TString, status = sp.TNat)

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.data_contract, "change_status").open_some()

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_did = parameters.provider_did,
            status = 1
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.entry_point
    def set_provider_deprecated(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_did, sp.TString)

        # Update is allowed only from owner
        owner_address = self.get_provider_owner_address(parameters.provider_did)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

        # Defining the data expected by the Storage contract
        contract_data = sp.TRecord(provider_did = sp.TString, status = sp.TNat)

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.data_contract, "change_status").open_some()

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_did = parameters.provider_did,
            status = 2
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.entry_point
    def set_provider_status(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_did, sp.TString)
        sp.set_type(parameters.status, sp.TNat)

        # Update is allowed only from owner
        owner_address = self.get_provider_owner_address(parameters.provider_did)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

        # Defining the data expected by the Storage contract
        contract_data = sp.TRecord(provider_did = sp.TString, status = sp.TNat)

        # Defining the Storage contract itself and its entry point for the call
        storage_contract = sp.contract(contract_data, self.data.data_contract, "change_status").open_some()

        # Verify status ID exists
        sp.verify(self.data.provider_statuses.contains(parameters.status), message = "Incorrect status")

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_did = parameters.provider_did,
            status = parameters.status
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), storage_contract)

    @sp.onchain_view()
    def get_asset_provider(self, provider_did):
        # Defining the parameters' types
        sp.set_type(provider_did, sp.TString)
        
        # Defining the parameters' types
        provider = sp.view(
            "get_asset_provider",
            self.data.data_contract,
            provider_did,
            t = sp.TRecord(
                provider_did = sp.TString,
                provider_data = sp.TString,
                status = sp.TNat,
                creator_wallet_address = sp.TAddress,
            )
        ).open_some("Invalid view");

        # Format result
        result_provider = sp.record(
            provider_data = provider.provider_data,
            status = self.data.provider_statuses[provider.status]
        )

        # Calling the Storage contract with the parameters we defined
        sp.result(result_provider)

@sp.add_test(name = "AssetProviderRepository")
def test():
    sp.add_compilation_target("assetProviderRepository",
        AssetProviderRepository(sp.address("KT1_contract_address"))
    )
