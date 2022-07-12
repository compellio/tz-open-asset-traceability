# Schema Registry Contract

import smartpy as sp

class AssetProviderRepository(sp.Contract):
    def __init__(self, data_contract):
        self.init_type(
            sp.TRecord(
                data_contract = sp.TAddress
            )
        )
        self.init(
            data_contract = data_contract
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

    @sp.entry_point
    def create_asset_provider(self, provider_did, provider_data):
        sp.set_type(provider_did, sp.TString)
        sp.set_type(provider_data, sp.TString)

        # Check if provider does not exist, does not allow add call otherwise
        sp.verify(~self.check_provider_exists(provider_did), message = "Provider did already exists")

        data_schema = sp.TRecord(
            provider_did = sp.TString,
            provider_data = sp.TString,
            creator_wallet_address = sp.TAddress,
        )

        # Defining the Logic contract itself and its entry point for the call
        data_contract = sp.contract(data_schema, self.data.data_contract, "create_asset_provider").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            provider_did = provider_did,
            provider_data = provider_data,
            creator_wallet_address = sp.source,
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), data_contract)

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
                creator_wallet_address = sp.TAddress,
            )
        ).open_some("Invalid view");

        # Format result
        result_provider = sp.record(
            provider_data = provider.provider_data,
        )

        # Calling the Storage contract with the parameters we defined
        sp.result(result_provider)

@sp.add_test(name = "AssetProviderRepository")
def test():
    sp.add_compilation_target("assetProviderRepository",
        AssetProviderRepository(sp.address("KT1_contract_address"))
    )
