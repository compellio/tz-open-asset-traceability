# Schema Registry Contract

import smartpy as sp

class AssetTwinTracing(sp.Contract):
    def __init__(self, asset_provider_contract):
        self.init_type(
            sp.TRecord(
                assets = sp.TBigMap(
                    sp.TString,
                    sp.TMap(
                        sp.TString,
                        sp.TRecord(
                            asset_repository_endpoint = sp.TString,
                            creator_wallet_address = sp.TAddress,
                        )
                    )
                ),
                asset_provider_contract = sp.TAddress,
            )
        )
        self.init(
            assets = sp.big_map(),
            asset_provider_contract = asset_provider_contract,
        )

    ###########
    # Helpers #
    ###########

    # Verify Provider existence
    def verify_provider_exists(self, provider_did):
        provider_existance = sp.view(
            "verify_provider_exists",
            self.data.asset_provider_contract,
            provider_did,
            t = sp.TBool
        ).open_some("Invalid view");

        return provider_existance

    @sp.entry_point
    def register(self, anchor_hash, provider_did, repo_end_point):
        sp.set_type(anchor_hash, sp.TString)
        sp.set_type(provider_did, sp.TString)
        sp.set_type(repo_end_point, sp.TString)

        sp.verify(self.verify_provider_exists(provider_did) == sp.bool(True), message = "Provider " + provider_did + " does not exist")

        tracable_record = sp.record(
            asset_repository_endpoint = repo_end_point,
            creator_wallet_address = sp.source,
        )

        sp.if (self.data.assets.contains(anchor_hash) == False):
            self.data.assets[anchor_hash] = {provider_did : tracable_record}
        sp.else:
            sp.if (~self.data.assets[anchor_hash].contains(provider_did)):
                self.data.assets[anchor_hash][provider_did] = tracable_record
            sp.else:
                sp.failwith("Hash " + anchor_hash + " already exists for provider " + provider_did)

    @sp.onchain_view()
    def fetch_asset_twin(self, parameters):
        sp.set_type(parameters.anchor_hash, sp.TString)
        sp.set_type(parameters.provider_did, sp.TString)

        anchor_hash = parameters.anchor_hash
        provider_did = parameters.provider_did
        
        sp.verify(self.data.assets[anchor_hash].contains(provider_did), message = "Hash " + anchor_hash + " does not exist for provider " + provider_did)
        
        sp.result(self.data.assets[anchor_hash][provider_did])

@sp.add_test(name = "AssetTwinTracing")
def test():
    sp.add_compilation_target("assetTwinTracing",
        AssetTwinTracing(
            sp.address("KT1_contract_address")
        )
    )
