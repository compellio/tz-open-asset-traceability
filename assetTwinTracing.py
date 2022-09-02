# Schema Registry Contract

import smartpy as sp

class AssetTwinTracing(sp.Contract):
    def __init__(self, certifier):
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
                calling_contract_address = sp.TOption(sp.TAddress),
                certifier = sp.TAddress
                # asset_provider_contract = sp.TAddress,
            )
        )
        self.init(
            assets = sp.big_map(),
            calling_contract_address=sp.none,
            certifier=certifier
            # asset_provider_contract = asset_provider_contract,
        )

    ###########
    # Helpers #
    ###########

    # Verify Provider existence
    # def verify_provider_exists(self, provider_id):
    #     provider_existance = sp.view(
    #         "verify_provider_exists",
    #         self.data.asset_provider_contract,
    #         provider_id,
    #         t = sp.TBool
    #     ).open_some("Invalid view");

    #     return provider_existance

    @sp.entry_point
    def register(self, anchor_hash, provider_id, repo_end_point):
        sp.set_type(anchor_hash, sp.TString)
        sp.set_type(provider_id, sp.TString)
        sp.set_type(repo_end_point, sp.TString)

        # Verifying whether the caller address is the calling contract
        sp.verify(self.data.calling_contract_address.open_some(message="Empty calling_contract_address") == sp.sender,
                  message="Incorrect caller")

        # sp.verify(self.verify_provider_exists(provider_id) == sp.bool(True), message = "Provider " + provider_id + " does not exist")

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
        
        sp.verify(self.data.assets[anchor_hash].contains(provider_id), message = "Hash " + anchor_hash + " does not exist for provider " + provider_id)
        
        sp.result(self.data.assets[anchor_hash][provider_id])


    @sp.entry_point
    def change_calling_contract_address(self, new_calling_contract_address):
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")

        # Update logic contract address
        self.data.calling_contract_address = sp.some(new_calling_contract_address)

@sp.add_test(name = "AssetTwinTracing")
def test():
    sp.add_compilation_target("assetTwinTracing",
        AssetTwinTracing(sp.address('tz1_certifier_address'))
    )
