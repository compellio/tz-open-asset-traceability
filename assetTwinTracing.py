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
                            registration_timestamps = sp.TList(sp.TTimestamp)
                        )
                    )
                ),
                calling_contract_address = sp.TOption(sp.TAddress),
                certifier = sp.TAddress
            )
        )
        self.init(
            assets = sp.big_map(),
            calling_contract_address = sp.none,
            certifier = certifier
        )

    ###########
    # Helpers #
    ###########

    @sp.entry_point
    def register(self, anchor_hash, provider_id, repo_end_point):
        sp.set_type(anchor_hash, sp.TString)
        sp.set_type(provider_id, sp.TString)
        sp.set_type(repo_end_point, sp.TString)

        # Verifying whether the caller address is the calling contract
        sp.verify(self.data.calling_contract_address.open_some(message = "Empty calling contract address") == sp.sender,
            message = "Incorrect caller")

        tracable_record = sp.record(
            asset_repository_endpoint = repo_end_point,
            creator_wallet_address = sp.source,
            registration_timestamps = sp.list([sp.timestamp_from_utc_now()], t = sp.TTimestamp),
        )

        sp.if (self.data.assets.contains(anchor_hash) == True):
            sp.if (self.data.assets[anchor_hash].contains(provider_id) == True):
                new_timestamps = sp.cons(sp.timestamp_from_utc_now(), self.data.assets[anchor_hash][provider_id].registration_timestamps)
                with sp.modify_record(self.data.assets[anchor_hash][provider_id], "data") as data:
                    data.registration_timestamps = new_timestamps
            sp.else:
                self.data.assets[anchor_hash][provider_id] = tracable_record
        sp.else:
            self.data.assets[anchor_hash] = {provider_id : tracable_record}

    @sp.onchain_view()
    def fetch_asset_twin(self, parameters):
        sp.set_type(parameters.anchor_hash, sp.TString)
        sp.set_type(parameters.provider_id, sp.TString)
        
        sp.verify(self.data.assets.contains(parameters.anchor_hash), message = "Hash not found")
        sp.verify(self.data.assets[parameters.anchor_hash].contains(parameters.provider_id), message = "Hash not found")
        
        sp.result(self.data.assets[parameters.anchor_hash][parameters.provider_id])

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
