# Schema Registry Contract

import smartpy as sp

class AssetProvider(sp.Contract):
    def __init__(self):
        self.init_type(
            sp.TRecord(
                asset_providers = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        provider_did = sp.TString,
                        provider_data = sp.TString,
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
        self.data.asset_providers[parameters.provider_did] = parameters

    @sp.onchain_view()
    def get_asset_provider(self, provider_did):
        sp.result(self.data.asset_providers[provider_did])

    @sp.onchain_view()
    def verify_provider_exists(self, provider_did):
        sp.result(self.data.asset_providers.contains(provider_did))

    @sp.onchain_view()
    def get_provider_owner_address(self, provider_did):
        sp.result(self.data.asset_providers[provider_did].creator_wallet_address)

@sp.add_test(name = "AssetProvider")
def test():
    sp.add_compilation_target("assetProvider",
        AssetProvider()
    )
