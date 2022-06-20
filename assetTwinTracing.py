# Schema Registry Contract

import smartpy as sp

class AssetTwinTracing(sp.Contract):
    def __init__(self):
        self.init_type(
            sp.TRecord(
                assets = sp.TBigMap(
                    sp.TString,
                    sp.TString
                ),
            )
        )
        self.init(
            assets = sp.big_map(),
        )

    @sp.entry_point
    def register_state(self, traceable, repo_end_point):
        sp.set_type(traceable, sp.TString)
        sp.set_type(repo_end_point, sp.TString)

        sp.verify(self.data.assets.contains(traceable) == sp.bool(False), message = "Hash " + traceable + " already exists")

        self.data.assets[traceable] = repo_end_point

    @sp.onchain_view()
    def get_asset(self, traceable):
        sp.result(self.data.assets[traceable])

@sp.add_test(name = "AssetTwinTracing")
def test():
    scenario = sp.test_scenario()

    hash_1 = "efb583d376b19d92d81e75bea335768d2b5cc9d60460c182cb6e66e8031b1aea"
    hash_2 = "fc2c0c139d5b71c45a339f91a81961904ec564d62ca3727e0679bef4193c7c7a"
    record_1 = sp.record(traceable = hash_1, repo_end_point = "end_point_1")
    record_2 = sp.record(traceable = hash_2, repo_end_point = "end_point_2")

    c1 = AssetTwinTracing()

    scenario += c1

    c1.register_state(record_1).run(valid = True)
    scenario.verify(c1.get_asset(hash_1) == "end_point_1")
    c1.register_state(record_1).run(valid = False)
    c1.register_state(record_2).run(valid = True)
    scenario.verify(c1.get_asset(hash_2) == "end_point_1")

    sp.add_compilation_target("assetTwinTracing",
        AssetTwinTracing()
    )
