# Schema Registry Contract

import smartpy as sp

class AssetProviderRepository(sp.Contract):
    def __init__(self):
        self.init_type(
            sp.TRecord(
                asset_providers = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
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
                ),
            )
        )
        self.init(
            asset_providers = sp.big_map(),
        )

    @sp.entry_point
    def create_asset_provider(self, asset_provider_uid, data):
        sp.set_type(asset_provider_uid, sp.TString)

        sp.verify(self.data.asset_providers.contains(asset_provider_uid) == sp.bool(False), message = "Asset provider with UID " + asset_provider_uid + " already exists")

        self.data.asset_providers[asset_provider_uid] = data

    @sp.onchain_view()
    def get_asset_provider(self, asset_provider_uid):
        sp.result(self.data.asset_providers[asset_provider_uid])

@sp.add_test(name = "AssetProviderRepository")
def test():
    scenario = sp.test_scenario()

    asset_provider_uid_1 = "86a6c8f7-dc31-46ba-98fc-58bea40fc28d"
    asset_provider_uid_2 = "7f6fd42a-1927-4dd1-b32a-e87f4890d77a"
    
    data = sp.record(
        originator = sp.address("tz1WM1wDM4mdtD3qMiELJSgbB14ZryyHNu7P"),
        orgName = "Organisation Example",
        orgRegistrationNumber = "11111",
        domain = "example.org",
        website = "https://example.org",
        alternativeProviderIds = [],
        assetRepositoryEndpoints = [],
        luwCoordinatorEndpoints = [],
        metadata = {}
    )

    record_1 = sp.record(asset_provider_uid = asset_provider_uid_1, data = data)
    record_2 = sp.record(asset_provider_uid = asset_provider_uid_2, data = data)

    c1 = AssetProviderRepository()

    scenario += c1

    c1.create_asset_provider(record_1).run(valid = True)
    scenario.verify(c1.get_asset_provider(asset_provider_uid_1).domain == "example.org")
    c1.create_asset_provider(record_1).run(valid = False)
    c1.create_asset_provider(record_2).run(valid = True)


    sp.add_compilation_target("assetProviderRepository",
        AssetProviderRepository()
    )
