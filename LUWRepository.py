# Schema Registry Contract

import smartpy as sp

class LUWRepository(sp.Contract):
    def __init__(self, luw_contract):
        self.init_type(
            sp.TRecord(
                luw_contract = sp.TAddress
            )
        )
        self.init(
            luw_contract = luw_contract
        )

    @sp.entry_point
    def create_luw_contract(self, luw_uid):
        sp.set_type(luw_uid, sp.TString)

        # Defining the data that we expect as a return from the Logic contract
        data_schema = self.get_luw_schema()

        # Defining the Logic contract itself and its entry point for the call
        luw_contract = sp.contract(data_schema, self.data.luw_contract, "create_luw_contract").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            luw_uid = luw_uid,
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), luw_contract)

    @sp.private_lambda()
    def get_luw_schema(self):
        record = sp.TRecord(
            luw_uid = sp.TString,
        )

        sp.result(record)

    @sp.onchain_view()
    def get_luw(self, luw_uid):
        # Defining the parameters' types
        sp.set_type(luw_uid, sp.TString)

@sp.add_test(name = "LUWRepository")
def test():
    sp.add_compilation_target("luwRepository",
        LUWRepository(sp.address("KT1MWPUKoU4FUVr1nBA4cwjMSoSsxqE3x9kc"))
    )
