
const $ = require("jquery");
const { TezosToolkit } = require('@taquito/taquito');
const { BeaconWallet } = require('@taquito/beacon-wallet');

function initUI() {
    updateUISetting({
        provider: "https://jakartanet.ecadinfra.com",
        assetTwinContractAddress: "KT1PCvaxTcGm4T7n1nmcYeZd5sQbizDUwa7f",
        assetProviderContractAddress: "KT1CMi1HmV6dyBobB5ys5rPzMtXkTTNMRu2N",
        LUWContractAddress: "KT1Qtbq2gUJ6GpCj5JXuu88bZ23GY5CRXWR9",
    });

    // setup UI actions

    // Register Asset Twin
    $("#btn_register_asset_twin").click(() => register_asset_twin(
        $("#asset_twin_hash"),
        $("#asset_twin_provider_did"),
        $("#asset_twin_repo_endpoint")
    ));

    // Get Asset Twin
    $("#btn_get_asset_twin").click(() => fetch_asset_twin(
        $("#asset_twin_hash_get"),
        $("#asset_twin_provider_did_get")
    ));

    // Add / Update provider
    $("#btn_provider_issue").click(() => add_provider(
        $("#provider_did"),
        $("#provider_data")
    ));

    // $("#btn_provider_update_data").click(() => update_provider_data(
    //     $("#provider_did"),
    //     $("#provider_data")
    // ));

    // // Update provider owner
    // $("#btn_provider_owner_update").click(() => set_provider_owner(
    //     $("#provider_did"),
    //     $("#provider_owner")
    // ));

    // Get provider
    $("#btn_provider_get").click(() => get_provider(
        $("#provider_did")
    ));

    // Set provider status
    $("#btn_provider_activate").click(() => set_provider_status($("#provider_did"), "activate"));
    $("#btn_provider_deactivate").click(() => set_provider_status($("#provider_did"), "deactivate"));
    $("#btn_provider_set_status").click(() => set_provider_status(
        $("#provider_did"),
        "set",
        $("#provider_status_id")
    ));

    // Settings / Wallet
    $("#btn_settings").click(() => $("#settings-box").toggleClass('d-none'));
    $("#btn_connect").click(() => connectWallet());
}

function updateUISetting(accountSettings) {
    $('#provider').val(accountSettings.provider);
    $('#assetTwinContractAddress').val(accountSettings.assetTwinContractAddress);
    $('#assetProviderContractAddress').val(accountSettings.assetProviderContractAddress);
    $('#LUWContractAddress').val(accountSettings.LUWContractAddress);
}

function readUISettings() {
    return {
        provider: $('#provider').val(),
        assetTwinContractAddress: $('#assetTwinContractAddress').val(),
        assetProviderContractAddress: $('#assetProviderContractAddress').val(),
        LUWContractAddress: $('#LUWContractAddress').val(),
    };
}

function showViewResult(result)
{
    $("#result-loader").addClass('d-none').removeClass('d-flex')
    $("#view-result-pre").html(result)
    $("#view-result").addClass('d-flex').removeClass('d-none')
}

function showResultAlert(result, type)
{
    if (type === 'alert-danger') {
        $("#result-loader").addClass('d-none').removeClass('d-flex')
    }

    $("#alert-result").attr('class', `alert ${type}`);
    $("#alert-result").html(result)
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
let browser_operations_url = "https://jakartanet.tzkt.io/" 
let non_ascii_char_message = 'Input string contains characters not allowed in Michelson. For more info see the <a target="_blank" href="https://tezos.gitlab.io/michelson-reference/#type-string">Michelson reference for type string</a>' 

// This function will connect your application with the wallet
function connectWallet() {
    const accountSettings = readUISettings();
    tezos = new TezosToolkit(accountSettings.provider);

    const options = {
        name: 'Open Asset Traceability',
        preferredNetwork: "jakartanet"
    };
    
    wallet = new BeaconWallet(options);

    wallet
        .requestPermissions({
            network: {
                type: "jakartanet"
            }
        })
        .then((_) => wallet.getPKH())
        .then((address) => console.log(address))
        .then(() => tezos.setWalletProvider(wallet))
        .then(() => $('#app-overlay').remove())
        .then(() => $('#settings-pills').removeClass("d-none"))
        .then(() => activateTabs());
}

function register_asset_twin(asset_twin_hash, provider_did, repo_endpoint) {
    const accountSettings = readUISettings();

    if (
        isElementASCII(asset_twin_hash) === false
        || isElementASCII(provider_did) === false
        || isElementASCII(repo_endpoint) === false
    ) {
        showResultAlert(non_ascii_char_message, "alert-danger")
        return;
    }

    return tezos.wallet.at(accountSettings.assetTwinContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            return contract.methods.default(
                String(asset_twin_hash.val()),
                String(provider_did.val()),
                String(repo_endpoint.val()),
            ).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Registered new Asset ${asset_twin_hash.val()} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            fetch_asset_twin(asset_twin_hash, provider_did, false);
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function fetch_asset_twin(asset_twin_hash, provider_did, show_alert = true) {
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.assetTwinContractAddress;

    if (
        isElementASCII(asset_twin_hash) === false
        || isElementASCII(provider_did) === false
    ) {
        showResultAlert(non_ascii_char_message, "alert-danger")
        return;
    }

    data = {
        anchor_hash: asset_twin_hash.val(),
        provider_did: provider_did.val(),
    }

    $("#result-loader").addClass('d-flex').removeClass('d-none')

    return tezos.wallet.at(accountSettings.assetTwinContractAddress)
        .then((contract) => {
            if (show_alert) clearAll()
            if (show_alert) showResultAlert("Getting...", "alert-info");

            return contract.contractViews.fetch_asset_twin(data).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            if (show_alert) showResultAlert("Finished", "alert-success");
            showViewResult(JSON.stringify(viewResult))
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function add_provider(provider_did, provider_data) {
    const accountSettings = readUISettings();

    if (
        isElementASCII(provider_did) === false
        ||
        isElementASCII(provider_data) === false
    ) {
        showResultAlert(non_ascii_char_message, "alert-danger")
        return;
    }

    return tezos.wallet.at(accountSettings.assetProviderContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            return contract.methods.create_asset_provider(String(provider_data.val()), String(provider_did.val())).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Created new Provider with DID ${provider_did.val()} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            get_provider(provider_did, false)
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

// function update_provider_data(provider_did, provider_data) {
//     const accountSettings = readUISettings();

//     if (
//         isElementASCII(String(provider_did)) === false
//         ||
//         isElementASCII(String(provider_data)) === false
//     ) {
//         showResultAlert(non_ascii_char_message, "alert-danger")
//         return;
//     }

//     return tezos.wallet.at(accountSettings.assetProviderContractAddress)
//         .then((contract) => {
//             clearAll()
//             showResultAlert("Sending...", "alert-info");

//             return contract.methods.set_provider_data(String(provider_data), String(provider_did)).send();
//         })
//         .then((op) => {
//             showResultAlert("Waiting for confirmation...", "alert-info");
//             return op.confirmation(1).then(() => op);
//         })
//         .then((data) => {
//             showResultAlert(`Updated Data for Provider with DID ${provider_did} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
//             get_provider(provider_did, false)
//         })
//         .catch((error) => {
//             showResultAlert(error.message, "alert-danger");
//         });
// }

// function set_provider_owner(provider_did, provider_address) {
//     const accountSettings = readUISettings();

//     if (isElementASCII(String(provider_did)) === false) {
//         showResultAlert(non_ascii_char_message, "alert-danger")
//     }

//     return tezos.wallet.at(accountSettings.assetProviderContractAddress)
//         .then((contract) => {
//             clearAll()
//             showResultAlert("Sending...", "alert-info");

//             return contract.methods.set_provider_owner(String(provider_did), provider_address).send();
//         })
//         .then((op) => {
//             showResultAlert("Waiting for confirmation...", "alert-info");
//             return op.confirmation(1).then(() => op);
//         })
//         .then((data) => {
//             showResultAlert(`Updated Owner Address to ${provider_address} for Provider with DID ${provider_did} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
//             get_provider(provider_did, false)
//         })
//         .catch((error) => {
//             showResultAlert(error.message, "alert-danger");
//         });
// }

function set_provider_status(provider_did, status_operation, status_id = 0) {
    const accountSettings = readUISettings();

    if (isElementASCII(provider_did) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
    }

    let method;

    return tezos.wallet.at(accountSettings.assetProviderContractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            switch(status_operation) {
                case "activate":
                    method = contract.methods.set_provider_active(String(provider_did.val()))
                    break;
                case "deactivate":
                    method = contract.methods.set_provider_deprecated(String(provider_did.val()))
                    break;
                case "set":
                    method = contract.methods.set_provider_status(String(provider_did.val()), parseInt(status_id.val()))
                    break;
              }

            return method.send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Status for Provider with DID ${provider_did.val()} Status <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            get_provider(provider_did, false)
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function get_provider(provider_did, show_alert = true) {
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.assetProviderContractAddress;

    if (isElementASCII(provider_did) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
    }

    $("#result-loader").addClass('d-flex').removeClass('d-none')

    return tezos.wallet.at(accountSettings.assetProviderContractAddress)
        .then((contract) => {
            if (show_alert) clearAll()
            if (show_alert) showResultAlert("Getting...", "alert-info");

            return contract.contractViews.get_asset_provider(String(provider_did.val())).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            if (show_alert) showResultAlert("Finished", "alert-success");
            showViewResult(JSON.stringify(viewResult))
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

$(document).ready(initUI);
