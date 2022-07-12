# Test Scenarios

import smartpy as sp

@sp.add_test(name = "TestScripts")
def test():
    ASSET_PROVIDER = sp.io.import_stored_contract("assetProvider.py")
    ASSET_PROVIDER_REPOSITORY = sp.io.import_stored_contract("assetProviderRepository.py")
    ASSET_TWIN_TRACING = sp.io.import_stored_contract("assetTwinTracing.py")
    certifier = sp.test_account("Certifier")
    operator_A = sp.test_account("Operator_A")
    operator_B = sp.test_account("Operator_B")

    certifier_address = certifier.address
    operator_A_address = operator_A.address
    operator_B_address = operator_B.address

    scenario = sp.test_scenario()
    scenario.h1("Preparation")
    scenario.table_of_contents()

    scenario.h2("Accounts")
    scenario.show([certifier, operator_A, operator_B])

    scenario.h2("Contracts List")

    # Asset Provider Contract Instantiation

    scenario.h3("Asset Provider")

    asset_provider = ASSET_PROVIDER.AssetProvider()

    scenario += asset_provider

    # Asset Provider Repository Contract Instantiation

    scenario.h3("Asset Provider Repository")

    asset_provider_repo = ASSET_PROVIDER_REPOSITORY.AssetProviderRepository(
        asset_provider.address
    )

    scenario += asset_provider_repo

    # Asset Provider Repository Contract Instantiation

    scenario.h3("Asset Twin Tracing")

    asset_twin_tracing = ASSET_TWIN_TRACING.AssetTwinTracing(asset_provider.address)

    scenario += asset_twin_tracing

    # Testing 

    scenario.h1("Testing")

    # Asset Provider Testing

    scenario.h2("Asset Provider Testing")
    scenario.h3("Asset Provider Creation")

    asset_provider_data_A = "asset_provider_data_A"
    asset_provider_data_B = "asset_provider_data_B"

    provider_did_1 = "86a6c8f7-dc31-46ba-98fc-58bea40fc28d"
    provider_did_2 = "7f6fd42a-1927-4dd1-b32a-e87f4890d77a"

    asset_provider_1 = sp.record(
        provider_did = provider_did_1,
        provider_data = asset_provider_data_A
    )

    asset_provider_2 = sp.record(
        provider_did = provider_did_2,
        provider_data = asset_provider_data_B
    )

    asset_provider_repo.create_asset_provider(asset_provider_1).run(valid = True, sender = operator_A_address)
    scenario.verify(asset_provider_repo.get_asset_provider(provider_did_1).provider_data == asset_provider_data_A)
    asset_provider_repo.create_asset_provider(asset_provider_1).run(valid = False, sender = operator_B_address)
    asset_provider_repo.create_asset_provider(asset_provider_2).run(valid = True, sender = operator_B_address)
    scenario.verify(asset_provider_repo.get_asset_provider(provider_did_2).provider_data == asset_provider_data_B)

    scenario.h3("Asset Provider Status Change")

    asset_provider_status_valid = sp.record(
        provider_did = provider_did_1,
        status = 1
    )

    asset_status_invalid_status = sp.record(
        provider_did = provider_did_2,
        status = 9999
    )

    asset_status_invalid_provider = sp.record(
        provider_did = "non_existing_did",
        status = 1
    )

    asset_provider_repo.set_provider_deprecated(asset_provider_status_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(asset_provider_repo.get_asset_provider(provider_did_1).status == "deprecated")
    asset_provider_repo.set_provider_active(asset_provider_status_valid).run(valid = False, sender = operator_B_address)
    asset_provider_repo.set_provider_status(asset_provider_status_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(asset_provider_repo.get_asset_provider(provider_did_1).status == "active")
    asset_provider_repo.set_provider_status(asset_status_invalid_status).run(valid = False, sender = operator_A_address)
    asset_provider_repo.set_provider_status(asset_status_invalid_provider).run(valid = False, sender = operator_A_address)

    # Asset Twin Testing

    scenario.h2("Asset Twin Testing")

    hash_1 = "efb583d376b19d92d81e75bea335768d2b5cc9d60460c182cb6e66e8031b1aea"
    hash_2 = "fc2c0c139d5b71c45a339f91a81961904ec564d62ca3727e0679bef4193c7c7a"
    
    hash_1_provider_1 = sp.record(
        anchor_hash = hash_1,
        provider_did = provider_did_1,
        repo_end_point = "end_point_1"
    )

    hash_1_provider_2 = sp.record(
        anchor_hash = hash_1,
        provider_did = provider_did_2,
        repo_end_point = "end_point_1"
    )
    
    hash_1_provider_invalid = sp.record(
        anchor_hash = hash_1,
        provider_did = "provider_did_invalid",
        repo_end_point = "end_point_1"
    )

    hash_2_provider_1 = sp.record(
        anchor_hash = hash_2,
        provider_did = provider_did_1,
        repo_end_point = "end_point_2"
    )

    asset_twin_tracing.register(hash_1_provider_1).run(valid = True, sender = operator_A_address)
    scenario.verify(asset_twin_tracing.fetch_asset_twin(hash_1_provider_1).creator_wallet_address == operator_A_address)
    asset_twin_tracing.register(hash_1_provider_1).run(valid = False, sender = operator_B_address)
    asset_twin_tracing.register(hash_1_provider_2).run(valid = True, sender = operator_A_address)
    asset_twin_tracing.register(hash_2_provider_1).run(valid = True, sender = operator_B_address)
    scenario.verify(asset_twin_tracing.fetch_asset_twin(hash_2_provider_1).creator_wallet_address == operator_B_address)
    scenario.verify(sp.is_failing(asset_twin_tracing.fetch_asset_twin(hash_1_provider_invalid)))