# Schema Registry Contract

import smartpy as sp

class AssetTwinTracing(sp.Contract):
    def __init__(self):
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
            )
        )
        self.init(
            assets = sp.big_map(),
        )

    @sp.entry_point
    def register(self, anchor_hash, provider_id, repo_end_point):
        sp.set_type(anchor_hash, sp.TString)
        sp.set_type(provider_id, sp.TString)
        sp.set_type(repo_end_point, sp.TString)

        tracable_record = sp.record(
            asset_repository_endpoint = repo_end_point,
            creator_wallet_address = sp.source,
        )

        sp.if (self.data.assets.contains(anchor_hash) == False):
            self.data.assets[anchor_hash] = {provider_id : tracable_record}
        sp.else:
            sp.if (~self.data.assets[anchor_hash].contains(provider_id)):
                self.data.assets[anchor_hash][provider_id] = tracable_record
            sp.else:
                sp.failwith("Hash " + anchor_hash + " already exists for provider " + provider_id)

    @sp.onchain_view()
    def fetch_asset_twin(self, parameters):
        sp.set_type(parameters.anchor_hash, sp.TString)
        sp.set_type(parameters.provider_id, sp.TString)

        anchor_hash = parameters.anchor_hash
        provider_id = parameters.provider_id
        
        sp.verify(~self.data.assets[anchor_hash].contains(provider_id) == sp.bool(False), message = "Hash " + anchor_hash + " does not exist for provider " + provider_id)
        
        sp.result(self.data.assets[anchor_hash][provider_id])

@sp.add_test(name = "AssetTwinTracing")
def test():
    sp.add_compilation_target("assetTwinTracing",
        AssetTwinTracing()
    )
