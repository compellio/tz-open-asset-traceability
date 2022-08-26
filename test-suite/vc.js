
const $ = require("jquery");
const { MichelsonMap, TezosToolkit } = require('@taquito/taquito');
const { BeaconWallet } = require('@taquito/beacon-wallet');

function initUI() {
    updateUISetting({
        provider: "https://ghostnet.ecadinfra.com",
        lambdaContractAddress: "KT1LJFuXpPq1NuTYTwgbibM9mL66Kk7rN3Ke",
    });

    // setup UI actions

    // Register Asset Twin
    $("#btn_register_asset_twin").click(() => register_asset_twin(
        $("#asset_twin_hash"),
        $("#asset_twin_provider_id"),
        $("#asset_twin_repo_endpoint")
    ));

    // Get Asset Twin
    $("#btn_get_asset_twin").click(() => fetch_asset_twin(
        $("#asset_twin_hash_get"),
        $("#asset_twin_provider_id_get")
    ));

    // Add / Update provider
    $("#btn_provider_issue").click(() => add_provider(
        $("#provider_id"),
        $("#provider_data")
    ));

    $("#btn_provider_update_data").click(() => update_provider_data(
        $("#provider_id"),
        $("#provider_data")
    ));

    // Update provider owner
    $("#btn_provider_owner_update").click(() => set_provider_owner(
        $("#provider_id"),
        $("#provider_owner")
    ));

    // Get provider
    $("#btn_provider_get").click(() => get_provider(
        $("#provider_id")
    ));

    // Set provider status
    $("#btn_provider_activate").click(() => set_provider_status($("#provider_id"), "activate"));
    $("#btn_provider_deactivate").click(() => set_provider_status($("#provider_id"), "deactivate"));
    $("#btn_provider_set_status").click(() => set_provider_status(
        $("#provider_id"),
        "set",
        $("#provider_status_id")
    ));

    $("#btn_create_luw").click(() => create_luw(
        $("#create_luw_provider"),
        $("#create_luw_endpoint")
    ));

    $("#btn_state_luw_active").click(() => set_luw_state($("#change_luw_state_id"), 1));
    $("#btn_state_luw_prepare").click(() => set_luw_state($("#change_luw_state_id"), 2));
    $("#btn_state_luw_commit").click(() => set_luw_state($("#change_luw_state_id"), 3));
    $("#btn_state_luw_abort").click(() => set_luw_state($("#change_luw_state_id"), 4));

    $("#btn_add_repository").click(() => add_luw_repository(
        $("#add_luw_repository_id"),
        $("#add_luw_repository_repo_id")
    ));

    $("#btn_state_luw_repo_open").click(() => add_luw_repository_state($("#change_luw_repo_state_id"), $("#change_luw_repo_state_repo_id"), 1));
    $("#btn_state_luw_repo_ready").click(() => add_luw_repository_state($("#change_luw_repo_state_id"), $("#change_luw_repo_state_repo_id"), 2));
    $("#btn_state_luw_repo_commited").click(() => add_luw_repository_state($("#change_luw_repo_state_id"), $("#change_luw_repo_state_repo_id"), 3));
    $("#btn_state_luw_repo_rollbacked").click(() => add_luw_repository_state($("#change_luw_repo_state_id"), $("#change_luw_repo_state_repo_id"), 4));

    $("#btn_fetch_luw").click(() => fetch_luw(
        $("#fetch_luw_id").val(),
    ));

    // Settings / Wallet
    $("#btn_settings").click(() => $("#settings-box").toggleClass('d-none'));
    $("#btn_connect").click(() => connectWallet());
}

function updateUISetting(accountSettings) {
    $('#provider').val(accountSettings.provider);
    $('#lambdaContractAddress').val(accountSettings.lambdaContractAddress);
}

function readUISettings() {
    return {
        provider: $('#provider').val(),
        lambdaContractAddress: $('#lambdaContractAddress').val(),
    };
}

function showViewResult(result)
{
    $("#result-loader").addClass('d-none').removeClass('d-flex')
    $("#view-result-pre").html(result)
    $("#view-result").addClass('d-flex').removeClass('d-none')
}

function showResultAlert(text, link = null, type = "info")
{
    if (type === 'danger') {
        $("#result-loader").addClass('d-none').removeClass('d-flex')
    }

    let html = ""
    html += `<div class="w-100">${text}</div>`

    if (link !== null) {
        html += `<a class="btn btn-${type} mt-2" target="_blank" href="${link}">See Operation</a>`
    }

    $("#alert-result").attr('class', `alert alert-${type}`);
    $("#alert-result").html(html)
}

function clearAll()
{
    $("#view-result").addClass('d-none')
    $("#view-result-pre").html("")
    $("#alert-result").attr('class', 'd-none');
    $("#alert-result").html("")
    $(".is-invalid").removeClass("is-invalid")
}

function isElementASCII(element)
{
    let value = element.val()

    if (/^[\x00-\x7F]*$/.test(value)) {
        return true
    }

    element.addClass('is-invalid')
    return false;
}

function activateTabs()
{
    var pillElements = document.querySelectorAll('button[data-bs-toggle="pill"]')
    pillElements.forEach(function(pillElement) {
        pillElement.addEventListener('shown.bs.tab', function () {
            clearAll()
        })
    });
}

let tezos, wallet;
let browser_operations_url = "https://ghostnet.tzkt.io/" 
let non_ascii_char_message = 'Input string contains characters not allowed in Michelson. For more info see the <a target="_blank" href="https://tezos.gitlab.io/michelson-reference/#type-string">Michelson reference for type string</a>' 

// This function will connect your application with the wallet
function connectWallet() {
    const accountSettings = readUISettings();
    tezos = new TezosToolkit(accountSettings.provider);

    const options = {
        name: 'Open Asset Traceability',
        preferredNetwork: "ghostnet"
    };
    
    wallet = new BeaconWallet(options);

    wallet
        .requestPermissions({
            network: {
                type: "ghostnet"
            }
        })
        .then((_) => wallet.getPKH())
        .then((address) => console.log(address))
        .then(() => tezos.setWalletProvider(wallet))
        .then(() => $('#app-overlay').remove())
        .then(() => $('#settings-pills').removeClass("d-none"))
        .then(() => activateTabs());
}

function register_asset_twin(asset_twin_hash, provider_id, repo_endpoint) {
    const accountSettings = readUISettings();

    if (
        isElementASCII(asset_twin_hash) === false
        || isElementASCII(provider_id) === false
        || isElementASCII(repo_endpoint) === false
    ) {
        showResultAlert(non_ascii_char_message, null, "danger")
        return;
    }

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");
            
            return contract.methods.register_asset_twin(
                String(asset_twin_hash.val()),
                String(provider_id.val()),
                String(repo_endpoint.val()),
            ).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Registered new Asset ${asset_twin_hash.val()}`, browser_operations_url + data.opHash,  "success");
            fetch_asset_twin(asset_twin_hash, provider_id, false);
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function fetch_asset_twin(asset_twin_hash, provider_id, show_alert = true) {
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.lambdaContractAddress;

    if (
        isElementASCII(asset_twin_hash) === false
        || isElementASCII(provider_id) === false
    ) {
        showResultAlert(non_ascii_char_message, null, "danger")
        return;
    }

    data = {
        anchor_hash: asset_twin_hash.val(),
        provider_id: provider_id.val(),
    }

    $("#result-loader").addClass('d-flex').removeClass('d-none')

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            if (show_alert) clearAll()
            if (show_alert) showResultAlert("Getting...", null, "info");

            return contract.contractViews.fetch_asset_twin(data).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            if (show_alert) showResultAlert("Finished", null, "success");
            showViewResult(JSON.stringify(viewResult))
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function add_provider(provider_id, provider_data) {
    const accountSettings = readUISettings();

    if (
        isElementASCII(provider_id) === false
        ||
        isElementASCII(provider_data) === false
    ) {
        showResultAlert(non_ascii_char_message, null, "danger")
        return;
    }

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");

            return contract.methods.create_asset_provider(String(provider_data.val()), String(provider_id.val())).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Created new Provider with DID ${provider_id.val()}`, browser_operations_url + data.opHash,  "success");
            get_provider(provider_id, false)
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function update_provider_data(provider_id, provider_data) {
    const accountSettings = readUISettings();

    if (
        isElementASCII(provider_id) === false
        ||
        isElementASCII(provider_data) === false
    ) {
        showResultAlert(non_ascii_char_message, null, "danger")
        return;
    }

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");

            return contract.methods.set_provider_data(String(provider_data.val()), String(provider_id.val())).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Data for Provider with DID ${provider_id.val()}`, browser_operations_url + data.opHash,  "success");
            get_provider(provider_id, false)
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function set_provider_owner(provider_id, provider_address) {
    const accountSettings = readUISettings();

    if (isElementASCII(provider_id) === false) {
        showResultAlert(non_ascii_char_message, null, "danger")
    }

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");

            return contract.methods.set_provider_owner(provider_address.val(), String(provider_id.val())).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Owner Address to ${provider_address.val()} for Provider with DID ${provider_id.val()}`, browser_operations_url + data.opHash,  "success");
            get_provider(provider_id, false)
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function set_provider_status(provider_id, status_operation, status_id = 1) {
    const accountSettings = readUISettings();

    if (isElementASCII(provider_id) === false) {
        showResultAlert(non_ascii_char_message, null, "danger")
    }

    let method;

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");

            switch(status_operation) {
                case "activate":
                    method = contract.methods.set_provider_active(String(provider_id.val()))
                    break;
                case "deactivate":
                    method = contract.methods.set_provider_deprecated(String(provider_id.val()))
                    break;
                case "set":
                    method = contract.methods.set_provider_status(String(provider_id.val()), parseInt(status_id.val()))
                    break;
              }

            return method.send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Status for Provider with DID ${provider_id.val()} Status`, browser_operations_url + data.opHash,  "success");
            get_provider(provider_id, false)
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function get_provider(provider_id, show_alert = true) {
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.lambdaContractAddress;

    if (isElementASCII(provider_id) === false) {
        showResultAlert(non_ascii_char_message, null, "danger")
    }

    $("#result-loader").addClass('d-flex').removeClass('d-none')

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            if (show_alert) clearAll()
            if (show_alert) showResultAlert("Getting...", null, "info");

            return contract.contractViews.get_asset_provider(String(provider_id.val())).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            if (show_alert) showResultAlert("Finished", null, "success");
            showViewResult(JSON.stringify(viewResult))
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function create_luw(provider_id, service_endpoint) {
    const accountSettings = readUISettings();

    if (
        isElementASCII(provider_id) === false
        ||
        isElementASCII(service_endpoint) === false
    ) {
        showResultAlert(non_ascii_char_message, null, "danger")
        return;
    }

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");

            return contract.methods.create_luw(String(service_endpoint.val()), String(provider_id.val())).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((op) => {
            (
                async () => {
                    let data = await op.transactionOperation();
                    let luw_id = data.metadata.internal_operation_results[1].result.storage.args[0]["int"] - 1
                    showResultAlert(`Created new LUW with ID ${luw_id}`, browser_operations_url + op.opHash, "success");
                    fetch_luw(luw_id, false);
                }
            )();
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function set_luw_state(luw_id, state_id = 1) {
    const accountSettings = readUISettings();

    if (isElementASCII(luw_id) === false) {
        showResultAlert(non_ascii_char_message, null, "danger")
    }

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");
            
            return contract.methods.change_luw_state(luw_id.val(), state_id).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated LUW with ID ${luw_id.val()} State`, browser_operations_url + data.opHash,  "success");
            fetch_luw(luw_id.val(), false)
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function add_luw_repository(luw_id, repository_id) {
    const accountSettings = readUISettings();

    if (
        isElementASCII(luw_id) === false
        ||
        isElementASCII(repository_id) === false
    ) {
        showResultAlert(non_ascii_char_message, null, "danger")
        return;
    }

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");

            return contract.methods.add_luw_repository(luw_id.val(), String(repository_id.val())).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((op) => {
            showResultAlert(`Added Repository ${repository_id.val()} to LUW with ID ${luw_id.val()}`, browser_operations_url + op.opHash, "success");
            fetch_luw(luw_id.val(), false);
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function add_luw_repository_state(luw_id, repository_id, state_id = 1) {
    const accountSettings = readUISettings();

    if (
        isElementASCII(luw_id) === false
        ||
        isElementASCII(repository_id) === false
    ) {
        showResultAlert(non_ascii_char_message, null, "danger")
        return;
    }

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", null, "info");

            return contract.methods.change_luw_repository_state(luw_id.val(), String(repository_id.val()), state_id).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", null, "info");
            return op.confirmation(1).then(() => op);
        })
        .then((op) => {
            showResultAlert(`Altered Repository ${repository_id.val()} of LUW with ID ${luw_id.val()} to State ${state_id}`, browser_operations_url + op.opHash, "success");
            fetch_luw(luw_id.val(), false);
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

function fetch_luw(luw_id, show_alert = true) {
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.lambdaContractAddress;

    $("#result-loader").addClass('d-flex').removeClass('d-none')

    return tezos.wallet.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            if (show_alert) clearAll()
            if (show_alert) showResultAlert("Getting...", null, "info");

            return contract.contractViews.fetch_luw(luw_id).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            if (show_alert) showResultAlert("Finished", null, "success");
            
            let repositories = {};
            let states = {};
            
            viewResult.repository_endpoints.forEach((val, key) => {
                repositories[key] = val
            });
            viewResult.state_history.forEach((val, key) => {
                states[key] = val
            });
            
            showViewResult(
                "Creator wallet address: " + JSON.stringify(viewResult.creator_wallet_address, null, 4)
                + "</br>"
                + "LUW service endpoint: " + JSON.stringify(viewResult.luw_service_endpoint, null, 4)
                + "</br>"
                + "Provider ID: " + JSON.stringify(viewResult.provider_id, null, 4)
                + "</br>"
                + JSON.stringify(repositories, null, 4)
                + "</br>"
                + JSON.stringify(states, null, 4)
            )
        })
        .catch((error) => {
            showResultAlert(error.message, null, "danger");
        });
}

$(document).ready(initUI);
