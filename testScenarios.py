# Test Scenarios

import smartpy as sp

@sp.add_test(name = "TestScripts")
def test():
    ASSET_PROVIDER = sp.io.import_stored_contract("assetProvider.py")
    ASSET_PROVIDER_REPOSITORY = sp.io.import_stored_contract("assetProviderRepository.py")
    ASSET_TWIN_TRACING = sp.io.import_stored_contract("assetTwinTracing.py")
    LUW = sp.io.import_stored_contract("LUW.py")
    LUW_REPOSITORY = sp.io.import_stored_contract("LUWRepository.py")
    LAMBDA = sp.io.import_stored_contract("registry.py")

    certifier = sp.test_account("Certifier")
    operator_A = sp.test_account("Operator_A")
    operator_B = sp.test_account("Operator_B")
    offchain_coordinator = sp.test_account("Offchain_Coordinator")

    certifier_address = certifier.address
    operator_A_address = operator_A.address
    operator_B_address = operator_B.address
    offchain_coordinator_address = offchain_coordinator.address

    scenario = sp.test_scenario()
    scenario.h1("Preparation")
    scenario.table_of_contents()

    scenario.h2("Accounts")
    scenario.show([certifier, operator_A, operator_B])

    scenario.h2("Contracts List")

    # Asset Provider Contract Instantiation

    scenario.h3("Asset Provider")

    asset_provider = ASSET_PROVIDER.AssetProvider(certifier_address)

    scenario += asset_provider

    # Asset Provider Repository Contract Instantiation

    scenario.h3("Asset Provider Repository")

    asset_provider_repo = ASSET_PROVIDER_REPOSITORY.AssetProviderRepository(
        asset_provider.address, certifier_address
    )

    scenario += asset_provider_repo

    # Update logic contract address of the storage contract
    scenario.h2("Updating storage contract with logic contract address for Asset Provider Repository")
    asset_provider_repo.update_storage_contract_with_address().run(valid = True, sender = certifier_address)

    # Asset Twin  Contract Instantiation

    scenario.h3("Asset Twin Tracing")

    asset_twin_tracing = ASSET_TWIN_TRACING.AssetTwinTracing(
        certifier_address
    )

    scenario += asset_twin_tracing


    # LUW Contract Instantiation

    scenario.h3("LUW")

    luw_contract = LUW.LUW(certifier_address)

    scenario += luw_contract

    # LUW Repository Contract Instantiation

    scenario.h3("LUW Repository")

    luw_repo_contract = LUW_REPOSITORY.LUWRepository(
        luw_contract.address, certifier_address
    )

    scenario += luw_repo_contract

    # Update logic contract address of the storage contract
    scenario.h2("Updating storage contract with logic contract address for LUW Repository")
    luw_repo_contract.update_storage_contract_with_address().run(valid = True, sender = certifier_address)

    # Lambda Contract Instantiation

    scenario.h3("Lambda Contract")

    lambda_contract = LAMBDA.Registry(
        sp.record(
            asset_provider_contract = asset_provider_repo.address,
            asset_twin_contract = asset_twin_tracing.address,
            luw_contract = luw_repo_contract.address,
        ),
        certifier_address
    )

    scenario += lambda_contract

    # Update calling contract address of the asset twin contract to allow calls from the lambda contract

    scenario.h2("Updating asset twin contract with calling contract address")
    asset_twin_tracing.change_calling_contract_address(lambda_contract.address).run(valid = True, sender = certifier_address)

    # Testing 

    scenario.h1("Testing")
    scenario.h2("Expected Successful Cases")

    # Asset Provider Testing

    scenario.h2("Asset Provider Testing")
    scenario.h3("Asset Provider Creation")

    asset_provider_data_A = "asset_provider_data_A"
    asset_provider_data_B = "asset_provider_data_B"

    provider_id_1 = "86a6c8f7-dc31-46ba-98fc-58bea40fc28d"
    provider_id_2 = "7f6fd42a-1927-4dd1-b32a-e87f4890d77a"

    asset_provider_1 = sp.record(
        provider_id = provider_id_1,
        provider_data = asset_provider_data_A
    )

    asset_provider_2 = sp.record(
        provider_id = provider_id_2,
        provider_data = asset_provider_data_B
    )

    lambda_contract.create_asset_provider(asset_provider_1).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.get_asset_provider(provider_id_1).provider_data == asset_provider_data_A)
    lambda_contract.create_asset_provider(asset_provider_2).run(valid = True, sender = operator_B_address)
    scenario.verify(lambda_contract.get_asset_provider(provider_id_2).provider_data == asset_provider_data_B)

    scenario.h3("Asset Provider Management")

    change_asset_provider_1_data = sp.record(
        provider_id = provider_id_1,
        provider_data = asset_provider_data_B
    )
    
    lambda_contract.set_provider_data(change_asset_provider_1_data).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.get_asset_provider(provider_id_1).provider_data == asset_provider_data_B)

    change_asset_provider_1_owner_A = sp.record(
        provider_id = provider_id_1,
        new_owner_address = operator_A_address
    )

    change_asset_provider_1_owner_B = sp.record(
        provider_id = provider_id_1,
        new_owner_address = operator_B_address
    )

    lambda_contract.set_provider_owner(change_asset_provider_1_owner_B).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.get_asset_provider(provider_id_1).creator_wallet_address == operator_B_address)
    lambda_contract.set_provider_owner(change_asset_provider_1_owner_A).run(valid = True, sender = operator_B_address)
    scenario.verify(lambda_contract.get_asset_provider(provider_id_1).creator_wallet_address == operator_A_address)

    scenario.h3("Asset Provider Status Change")

    asset_provider_status_valid = sp.record(
        provider_id = provider_id_1,
        status = 1
    )

    asset_status_invalid_status = sp.record(
        provider_id = provider_id_2,
        status = 9999
    )

    asset_status_invalid_provider = sp.record(
        provider_id = "non_existing_did",
        status = 1
    )

    lambda_contract.set_provider_deprecated(provider_id_1).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.get_asset_provider(provider_id_1).status == "deprecated")
    lambda_contract.set_provider_status(asset_provider_status_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.get_asset_provider(provider_id_1).status == "active")

    # Asset Twin Testing

    scenario.h2("Asset Twin Testing")

    hash_1 = "efb583d376b19d92d81e75bea335768d2b5cc9d60460c182cb6e66e8031b1aea"
    hash_2 = "fc2c0c139d5b71c45a339f91a81961904ec564d62ca3727e0679bef4193c7c7a"
    
    hash_1_provider_1 = sp.record(
        anchor_hash = hash_1,
        provider_id = provider_id_1,
        repo_end_point = "end_point_1"
    )

    hash_1_provider_2 = sp.record(
        anchor_hash = hash_1,
        provider_id = provider_id_2,
        repo_end_point = "end_point_1"
    )
    
    hash_1_provider_invalid = sp.record(
        anchor_hash = hash_1,
        provider_id = "provider_id_invalid",
        repo_end_point = "end_point_1"
    )

    hash_2_provider_1 = sp.record(
        anchor_hash = hash_2,
        provider_id = provider_id_1,
        repo_end_point = "end_point_2"
    )

    lambda_contract.register_asset_twin(hash_1_provider_1).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.fetch_asset_twin(hash_1_provider_1).creator_wallet_address == operator_A_address)
    lambda_contract.register_asset_twin(hash_1_provider_2).run(valid = True, sender = operator_A_address)
    lambda_contract.register_asset_twin(hash_2_provider_1).run(valid = True, sender = operator_B_address)
    lambda_contract.register_asset_twin(hash_1_provider_1).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.fetch_asset_twin(hash_2_provider_1).creator_wallet_address == operator_B_address)

    # LUW Testing 

    scenario.h2("LUW Testing")
    scenario.h3("LUW Creation")

    luw_record = sp.record(
        provider_id = "provider_id",
        luw_service_endpoint = offchain_coordinator_address,
    )

    lambda_contract.create_luw(luw_record).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.fetch_luw(0).creator_wallet_address == operator_A_address)
    scenario.verify(lambda_contract.get_active_luw_state(0) == "active")

    repository_id_1 = "01add8a4-7302-490b-be57-cec2cd02f8da"
    repository_id_2 = "db161792-d5a9-434b-b0fc-5359f6d6460b"

    repository_add_valid_1 = sp.record(
        luw_id = 0,
        repository_id = repository_id_1,
    )

    repository_add_valid_2 = sp.record(
        luw_id = 0,
        repository_id = repository_id_2,
    )

    repository_add_invalid_luw = sp.record(
        luw_id = 999,
        repository_id = repository_id_1,
    )

    scenario.h3("LUW Repository Management")
    lambda_contract.add_luw_repository(repository_add_valid_1).run(valid = True, sender = operator_A_address)
    lambda_contract.add_luw_repository(repository_add_valid_2).run(valid = True, sender = operator_A_address)

    repository_change_state_valid = sp.record(
        luw_id = 0,
        repository_id = repository_id_1,
        state_id = 2
    )

    repository_change_state_invalid_luw = sp.record(
        luw_id = 999,
        repository_id = repository_id_1,
        state_id = 2
    )

    repository_change_state_invalid_state = sp.record(
        luw_id = 0,
        repository_id = repository_id_1,
        state_id = 999
    )

    repository_change_state_invalid_repo = sp.record(
        luw_id = 0,
        repository_id = "invalid_repo",
        state_id = 2
    )

    update_luw_all_repo_states = sp.record(
        luw_id = 0,
        state_id = 3
    )

    lambda_contract.change_luw_repository_state(repository_change_state_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.get_luw_repository_state(repository_add_valid_1) == "ready")

    luw_valid_new_state_record = sp.record(
        luw_id = 0,
        state_id = 2,
    )

    luw_new_state_invalid_luw_id_record = sp.record(
        luw_id = 999,
        state_id = 2,
    )

    luw_new_state_invalid_state_id_record = sp.record(
        luw_id = 0,
        state_id = 999,
    )

    lambda_contract.change_luw_state(luw_valid_new_state_record).run(valid = True, sender = operator_A_address)
    scenario.verify(lambda_contract.get_active_luw_state(0) == "prepare_to_commit")

    scenario.h2("Expected Failed Cases")

    # Asset Provider Testing

    scenario.h2("Asset Provider Testing")
    scenario.h3("Asset Provider Creation")

    scenario.h4("Adding an existing Provider ID. Expected exception - Provider ID already exists")
    lambda_contract.create_asset_provider(asset_provider_1).run(valid = False, sender = operator_B_address, exception = "Provider ID already exists")

    scenario.h4("Changing provider data from incorrect wallet address. Expected exception - Non-matching owner address")
    lambda_contract.set_provider_data(change_asset_provider_1_data).run(valid = False, sender = operator_B_address, exception = "Non-matching owner address")

    scenario.h4("Changing provider owner from incorrect wallet address. Expected exception - Non-matching owner address")
    lambda_contract.set_provider_owner(change_asset_provider_1_owner_B).run(valid = False, sender = operator_B_address, exception = "Non-matching owner address")

    scenario.h3("Asset Provider Status Change")

    scenario.h4("Changing provider to Active status from incorrect wallet address. Expected exception - Non-matching owner address")
    lambda_contract.set_provider_active(provider_id_1).run(valid = False, sender = operator_B_address, exception = "Non-matching owner address")
    
    scenario.h4("Changing provider status from incorrect wallet address. Expected exception - Non-matching owner address")
    lambda_contract.set_provider_status(asset_status_invalid_status).run(valid = False, sender = operator_A_address, exception = "Non-matching owner address")
    
    scenario.h4("Changing provider status of a non-existing provider ID. Expected exception - Provider ID does not exist")
    lambda_contract.set_provider_status(asset_status_invalid_provider).run(valid = False, sender = operator_A_address, exception = "Provider ID does not exist")

    # Asset Twin Testing
    
    scenario.verify(sp.is_failing(lambda_contract.fetch_asset_twin(hash_1_provider_invalid)))
    e = sp.catch_exception(lambda_contract.fetch_asset_twin(hash_1_provider_invalid), t = sp.TString)
    scenario.verify(e == sp.some("Hash not found"))
    
    # LUW Testing 

    scenario.h2("LUW Testing")

    scenario.h3("LUW Repository Management")

    scenario.h4("Adding a Repository to a non-active LUW. Expected exception - LUW is not Active")
    lambda_contract.add_luw_repository(repository_add_valid_1).run(valid = False, sender = operator_A_address, exception = "LUW is not Active")

    scenario.h4("Adding a Repository to a LUW from an incorrect wallet address. Expected exception - Non-matching owner address")
    lambda_contract.add_luw_repository(repository_add_valid_2).run(valid = False, sender = operator_B_address, exception = "Non-matching owner address")

    scenario.h4("Changing a LUW Repository state from an incorrect wallet address. Expected exception - Non-matching owner address")
    lambda_contract.change_luw_repository_state(repository_change_state_valid).run(valid = False, sender = operator_B_address, exception = "Non-matching owner address")
    
    scenario.h4("Changing a LUW Repository state for a non-existing LUW ID. Expected exception - LUW ID does not exist")
    lambda_contract.change_luw_repository_state(repository_change_state_invalid_luw).run(valid = False, sender = operator_A_address, exception = "LUW ID does not exist")
    
    scenario.h4("Changing a LUW Repository state to an invalid state ID. Expected exception - Incorrect state ID")
    lambda_contract.change_luw_repository_state(repository_change_state_invalid_state).run(valid = False, sender = operator_A_address, exception = "Incorrect state ID")

    scenario.h4("Changing a LUW Repository state for a non-existing Repository. Expected exception - Repository ID does not exist")
    lambda_contract.change_luw_repository_state(repository_change_state_invalid_repo).run(valid = False, sender = operator_A_address, exception = "Repository ID does not exist")

    scenario.h3("LUW State Change")
    
    scenario.h4("Changing LUW state from incorrect wallet address. Expected exception - Non-matching owner address")
    lambda_contract.change_luw_state(luw_valid_new_state_record).run(valid = False, sender = operator_B_address, exception = "Non-matching owner address")
    
    scenario.h4("Changing LUW state for a non-existing LUW ID. Expected exception - LUW ID does not exist")
    lambda_contract.change_luw_state(luw_new_state_invalid_luw_id_record).run(valid = False, sender = operator_A_address, exception = "LUW ID does not exist")
    
    scenario.h4("Changing LUW state to an invalid state ID. Expected exception - Incorrect state ID")
    lambda_contract.change_luw_state(luw_new_state_invalid_state_id_record).run(valid = False, sender = operator_A_address, exception = "Incorrect state ID")