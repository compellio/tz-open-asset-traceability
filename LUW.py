# Schema Registry Contract

import smartpy as sp

class LUW(sp.Contract):
    def __init__(self):
        self.init_type(
            sp.TRecord(
                luw_map = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        originator = sp.TAddress,
                        last_state_key = sp.TNat,
                        state_history = sp.TMap(
                            sp.TNat,
                            sp.TNat
                        ),
                    )
                ),
                states = sp.TBigMap(
                    sp.TNat,
                    sp.TString
                ),
            )
        )
        self.init(
            luw_map = sp.big_map(),
            states = sp.big_map({
                1: "active",
                2: "prepare_to_commit",
                3: "commited",
                4: "aborted"
            }),
        )

    @sp.entry_point
    def create_luw_contract(self, luw_uid):
        sp.set_type(luw_uid, sp.TString)

        sp.verify(self.data.luw_map.contains(luw_uid) == sp.bool(False), message = "LUW with UID " + luw_uid + " already exists")

        new_luw_record = sp.record(
            originator = sp.source,
            last_state_key = 0,
            state_history = {0: 1}
        )

        self.data.luw_map[luw_uid] = new_luw_record

    @sp.entry_point
    def change_luw_state(self, luw_uid, state_id):
        sp.set_type(luw_uid, sp.TString)
        sp.set_type(state_id, sp.TNat)

        sp.verify(self.data.states.contains(state_id), message = "Incorrect state ID")
        sp.verify(self.data.luw_map.contains(luw_uid), message = "LUW with UID " + luw_uid + " does not exist")

        luw = self.data.luw_map[luw_uid]

        sp.verify(luw.originator == sp.source, message = "Owner address of LUW could not be verified")

        luw_new_state_key = luw.last_state_key + 1
        luw_state_history = luw.state_history

        luw_state_history[luw_new_state_key] = state_id

        new_luw_record = sp.record(
            originator = luw.originator,
            last_state_key = luw_new_state_key,
            state_history = luw_state_history
        )

        self.data.luw_map[luw_uid] = new_luw_record

    @sp.onchain_view()
    def get_luw(self, luw_uid):
        sp.result(self.data.luw_map[luw_uid])

@sp.add_test(name = "LUW")
def test():
    scenario = sp.test_scenario()

    luw_uid_1 = "86a6c8f7-dc31-46ba-98fc-58bea40fc28d"
    luw_uid_2 = "7f6fd42a-1927-4dd1-b32a-e87f4890d77a"

    address_1 = sp.test_account("address_1").address
    address_2 = sp.test_account("address_2").address
    
    c1 = LUW()

    scenario += c1

    c1.create_luw_contract(luw_uid_1).run(valid = True, sender = address_1)
    c1.create_luw_contract(luw_uid_1).run(valid = False, sender = address_1)
    c1.create_luw_contract(luw_uid_2).run(valid = True, sender = address_1)
    c1.change_luw_state(sp.record(luw_uid = luw_uid_1, state_id = 2)).run(valid = True, sender = address_1)
    c1.change_luw_state(sp.record(luw_uid = luw_uid_1, state_id = 999)).run(valid = False, sender = address_1)
    c1.change_luw_state(sp.record(luw_uid = luw_uid_1, state_id = 3)).run(valid = False, sender = address_2)

    sp.add_compilation_target("luw",
        LUW()
    )
