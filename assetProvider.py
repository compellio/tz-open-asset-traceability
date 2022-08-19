# Schema Registry Contract

import smartpy as sp

class AssetProvider(sp.Contract):
    def __init__(self):
        self.init_type(
            sp.TRecord(
                asset_providers = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        provider_id = sp.TString,
                        provider_data = sp.TString,
                        status = sp.TNat,
                        creator_wallet_address = sp.TAddress,
                    )
                ),
            )
        )
        self.init(
            asset_providers = sp.big_map(),
        )

    @sp.entry_point
    def create_asset_provider(self, parameters):
        self.data.asset_providers[parameters.provider_id] = parameters

    @sp.entry_point
    def change_status(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.status, sp.TNat)

        provider_data = self.data.asset_providers[parameters.provider_id]
        
        with sp.modify_record(provider_data, "data") as data:
            data.status = parameters.status

        self.data.asset_providers[parameters.provider_id] = provider_data

    @sp.entry_point
    def change_data(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.provider_data, sp.TString)

        # Verifying whether the caller address is our Registry contract
        # sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        provider_data = self.data.asset_providers[parameters.provider_id]
        
        with sp.modify_record(provider_data, "data") as data:
            data.provider_data = parameters.provider_data

        self.data.asset_providers[parameters.provider_id] = provider_data

    @sp.entry_point
    def change_owner(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.new_owner_address, sp.TAddress)

        # Verifying whether the caller address is our Registry contract
        # sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        provider_data = self.data.asset_providers[parameters.provider_id]
        
        with sp.modify_record(provider_data, "data") as data:
            data.creator_wallet_address = parameters.new_owner_address

        self.data.asset_providers[parameters.provider_id] = provider_data

    @sp.onchain_view()
    def get_asset_providers(self):
        sp.result(self.data.asset_providers)

    @sp.onchain_view()
    def get_asset_provider(self, provider_id):
        sp.result(self.data.asset_providers[provider_id])

    @sp.onchain_view()
    def verify_provider_exists(self, provider_id):
        sp.result(self.data.asset_providers.contains(provider_id))

    @sp.onchain_view()
    def get_provider_owner_address(self, provider_id):
        sp.result(self.data.asset_providers[provider_id].creator_wallet_address)

@sp.add_test(name = "AssetProvider")
def test():
    sp.add_compilation_target("assetProvider",
        AssetProvider()
    )
