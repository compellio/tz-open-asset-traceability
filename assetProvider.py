# Schema Registry Contract

import smartpy as sp

class AssetProvider(sp.Contract):
    def __init__(self, certifier):
        self.init_type(
            sp.TRecord(
                asset_providers = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        provider_id = sp.TString,
                        provider_data = sp.TString,
                        status = sp.TNat,
                        creator_wallet_address = sp.TAddress,
                    )
                ),
                logic_contract_address = sp.TOption(sp.TAddress),
                certifier = sp.TAddress
            )
        )
        self.init(
            asset_providers = sp.big_map(),
            logic_contract_address = sp.none,
            certifier = certifier
        )

    @sp.entry_point
    def create_asset_provider(self, parameters):
        # Verifying whether the calling contract address is the logic contract
        sp.verify(self.data.logic_contract_address.open_some(message="Empty logic_contract_address") == sp.sender, message = "Incorrect caller")

        self.data.asset_providers[parameters.provider_id] = parameters

    @sp.entry_point
    def change_status(self, parameters):
        # Verifying whether the calling contract address is the logic contract
        sp.verify(self.data.logic_contract_address.open_some(message="Empty logic_contract_address") == sp.sender, message = "Incorrect caller")

        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.status, sp.TNat)

        provider_data = self.data.asset_providers[parameters.provider_id]
        
        with sp.modify_record(provider_data, "data") as data:
            data.status = parameters.status

        self.data.asset_providers[parameters.provider_id] = provider_data

    @sp.entry_point
    def change_data(self, parameters):
        # Verifying whether the calling contract address is the logic contract
        sp.verify(self.data.logic_contract_address.open_some(message="Empty logic_contract_address") == sp.sender, message = "Incorrect caller")

        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.provider_data, sp.TString)

        provider_data = self.data.asset_providers[parameters.provider_id]
        
        with sp.modify_record(provider_data, "data") as data:
            data.provider_data = parameters.provider_data

        self.data.asset_providers[parameters.provider_id] = provider_data

    @sp.entry_point
    def change_owner(self, parameters):
        # Verifying whether the calling contract address is the logic contract
        sp.verify(self.data.logic_contract_address.open_some(message="Empty logic_contract_address") == sp.sender, message = "Incorrect caller")

        # Defining the parameters' types
        sp.set_type(parameters.provider_id, sp.TString)
        sp.set_type(parameters.new_owner_address, sp.TAddress)

        provider_data = self.data.asset_providers[parameters.provider_id]
        
        with sp.modify_record(provider_data, "data") as data:
            data.creator_wallet_address = parameters.new_owner_address

        self.data.asset_providers[parameters.provider_id] = provider_data

    @sp.entry_point
    def change_logic_contract_address(self, new_logic_contract_address):
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")

        # Update logic contract address
        self.data.logic_contract_address = sp.some(new_logic_contract_address)

    @sp.onchain_view()
    def get_asset_provider(self, provider_id):
        sp.verify(self.data.asset_providers.contains(provider_id), message = "Provider ID does not exist")
        sp.result(self.data.asset_providers[provider_id])

    @sp.onchain_view()
    def verify_provider_exists(self, provider_id):
        sp.result(self.data.asset_providers.contains(provider_id))

    @sp.onchain_view()
    def get_provider_owner_address(self, provider_id):
        sp.verify(self.data.asset_providers.contains(provider_id), message = "Provider ID does not exist")
        sp.result(self.data.asset_providers[provider_id].creator_wallet_address)

@sp.add_test(name = "AssetProvider")
def test():
    sp.add_compilation_target("assetProvider",
        AssetProvider(sp.address('tz1_certifier_address'))
    )
