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

    @sp.entry_point
    def create_asset_provider(self, asset_provider_uid, data):
        sp.set_type(asset_provider_uid, sp.TString)

        # Defining the data that we expect as a return from the Logic contract
        data_schema = self.get_asset_provider_schema()

        # Defining the Logic contract itself and its entry point for the call
        data_contract = sp.contract(data_schema, self.data.data_contract, "create_asset_provider").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            asset_provider_uid = asset_provider_uid,
            data = data
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), data_contract)

    @sp.private_lambda()
    def get_asset_provider_schema(self):
        record = sp.TRecord(
            originator = sp.TAddress,
            orgName = sp.TString,
            orgRegistrationNumber = sp.TString,
            domain = sp.TString,
            website = sp.TString,
            alternativeProviderIds = sp.TList(sp.TString),
            assetRepositoryEndpoints = sp.TList(sp.TString),
            luwCoordinatorEndpoints = sp.TList(sp.TString),
            metadata = sp.TMap(
                sp.TString,
                sp.TString
            )
        )

        sp.result(record)

    @sp.onchain_view()
    def get_asset_provider(self, asset_provider_uid):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)

@sp.add_test(name = "AssetProviderRepository")
def test():
    sp.add_compilation_target("assetProviderRepository",
        AssetProviderRepository(sp.address("KT1MWPUKoU4FUVr1nBA4cwjMSoSsxqE3x9kc"))
    )
