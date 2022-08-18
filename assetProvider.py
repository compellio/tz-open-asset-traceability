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

        issuer_data = self.data.asset_providers[parameters.provider_id]
        
        with sp.modify_record(issuer_data, "data") as data:
            data.status = parameters.status

        self.data.asset_providers[parameters.provider_id] = issuer_data

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
