
const $ = require("jquery");
const { InMemorySigner } = require('@taquito/signer');
const { TezosToolkit } = require('@taquito/taquito');
const { BeaconWallet } = require('@taquito/beacon-wallet');
const delay = t => new Promise(resolve => setTimeout(resolve, t));

function initUI() {
    updateUISetting({
        provider: "https://ghostnet.ecadinfra.com",
        lambdaContractAddress: "KT1UaB5DY2MUkCEXY3TqjN7K8PDHpbHUASGQ",
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
    $("#btn_state_luw_repo_committed").click(() => add_luw_repository_state($("#change_luw_repo_state_id"), $("#change_luw_repo_state_repo_id"), 3));
    $("#btn_state_luw_repo_rollbacked").click(() => add_luw_repository_state($("#change_luw_repo_state_id"), $("#change_luw_repo_state_repo_id"), 4));

    $("#btn_fetch_luw").click(() => fetch_luw(
        $("#fetch_luw_id").val(),
    ));


    $("#btn_init_sim").click(() => init_sim());

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

function showViewResult(result) {
    $("#result-loader").addClass('d-none').removeClass('d-flex')
    $("#view-result-pre").html(result)
    $("#view-result").addClass('d-flex').removeClass('d-none')
}

function showResultAlert(text, link = null, type = "info") {
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

function showSimResultAlert(text, type = "info", $title = false) {
    let html = ""
    html += `<div class="w-100 ${$title === true ? 'h3' : 'h6' }">${text}</div>`

    $("#alert-sim").attr('class', `alert alert-${type}`);
    $("#alert-sim").html(html)
}

function appendSimResultAlert(text, $title = false) {
    var $alert = $('#alert-sim'); 
    let html = `<div class="w-100 ${$title === true ? 'h3' : 'h6' }">${text}</div>`

    $alert.append(html)
    $alert.animate({scrollTop: $alert.height()}, 1000);
}

function clearAll() {
    $("#view-result").addClass('d-none')
    $("#view-result-pre").html("")
    $("#alert-result").attr('class', 'd-none');
    $("#alert-result").html("")
    $(".is-invalid").removeClass("is-invalid")
}

function isElementASCII(element) {
    let value = element.val()

    if (/^[\x00-\x7F]*$/.test(value)) {
        return true
    }

    element.addClass('is-invalid')
    return false;
}

function activateTabs() {
    var pillElements = document.querySelectorAll('button[data-bs-toggle="pill"]')
    pillElements.forEach(function (pillElement) {
        pillElement.addEventListener('shown.bs.tab', function () {
            clearAll()
        })
    });
}

let tezos, wallet, tezosSim;
let browser_operations_url = "https://ghostnet.tzkt.io/"
let non_ascii_char_message = 'Input string contains characters not allowed in Michelson. For more info see the <a target="_blank" href="https://tezos.gitlab.io/michelson-reference/#type-string">Michelson reference for type string</a>'
let scenario_array = [
    "loan_request",
    "luw_initiation",
    "request_proof_residence_address",
    "persist_proof_residence_address",
    "register_proof_residence_address",
    "fetch_proof_residence_address",
    "bank_register_proof_residence_address",
    "KYC_check",
    "request_additional_info",
    "update_proof_address",
    "fetch_updated_proof_address",
    "prepare_to_commit",
    "update_repositories",
    "commit",
    "wrapup",
]

var current_scenario

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
        .then((address) => walletAddress = address)
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
            showResultAlert(`Registered new Asset ${asset_twin_hash.val()}`, browser_operations_url + data.opHash, "success");
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
            showResultAlert(`Created new Provider with DID ${provider_id.val()}`, browser_operations_url + data.opHash, "success");
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
            showResultAlert(`Updated Data for Provider with DID ${provider_id.val()}`, browser_operations_url + data.opHash, "success");
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
            showResultAlert(`Updated Owner Address to ${provider_address.val()} for Provider with DID ${provider_id.val()}`, browser_operations_url + data.opHash, "success");
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

            switch (status_operation) {
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
            showResultAlert(`Updated Status for Provider with DID ${provider_id.val()} Status`, browser_operations_url + data.opHash, "success");
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
            );
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
            showResultAlert(`Updated LUW with ID ${luw_id.val()} State`, browser_operations_url + data.opHash, "success");
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

function init_sim() {
    $("connection").remove()
    $(".actions-container").html("")
    $("#btn_next_step").hide();
    $("#sim-megacontainer").show();
    $("#btn_init_sim").addClass("disabled");

    current_scenario = []
    current_scenario = current_scenario.concat(scenario_array)

    jQuery('#sim-coordinator').connections({
        'to': '#sim-att',
        'class': 'con-coordinator-att con-inactive animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-bank').connections({
        'to': '#sim-coordinator',
        'class': 'con-bank-coordinator con-inactive invisible animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-ivc').connections({
        'to': '#sim-ivc-repo',
        'class': 'con-ivc-repo con-inactive animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-bank').connections({
        'to': '#sim-bank-repo',
        'class': 'con-bank-repo con-inactive animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-utility').connections({
        'to': '#sim-utility-repo',
        'class': 'con-utility-repo con-inactive animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-coor-left').connections({
        'to': '#sim-ivc',
        'class': 'con-coordinator-ivc con-inactive invisible animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-coor-right').connections({
        'to': '#sim-utility',
        'class': 'con-coordinator-utility con-inactive invisible animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-att-left').connections({
        'to': '#sim-luw',
        'class': 'con-att-luw con-inactive animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-att').connections({
        'to': '#sim-provider',
        'class': 'con-att-provider con-inactive animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });
    jQuery('#sim-att-right').connections({
        'to': '#sim-asset',
        'class': 'con-att-asset con-inactive animate__flash animate__slow animate__infinite',
        'css': {
            border: '4px solid'
        },
        'within': "#sim-connections-layer",
    });

    showSimResultAlert("Preparing simulation", "info");
    prepare_simulation_data()
}

function prepare_simulation_data() {
    var simLuwId;
    let setContract, provider, flaggedError = false;
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.lambdaContractAddress;

    tezosSim = new TezosToolkit(accountSettings.provider);

    InMemorySigner.fromSecretKey('edskRh1YUTUMfZuHHj3aftufevwSukuHuYRo4pyBfG9k8nvLhE2VNzEimmegDAMRGTM5Qqim4P9E2Ff5CaL66Y4bVW2wxkJTqR')
        .then((theSigner) => {
            tezosSim.setProvider({ signer: theSigner });
            //We can access the public key hash
            return tezosSim.signer.publicKeyHash();
        })
        .then((publicKeyHash) => {
            pk = publicKeyHash
        })
        .catch((error) => console.log(`Error: ${error} ${JSON.stringify(error, null, 2)}`));

    return tezosSim.contract.at(accountSettings.lambdaContractAddress)
        .then((contract) => {
            setContract = contract
            return contract.contractViews.get_asset_provider('test_suite_sim_provider').executeView({ viewCaller: contractCallFib });
        })
        .then(
            (viewResult) => {
                provider = viewResult;
            },
            (error) => {
                flaggedError = true
                console.log(error)
                return tezosSim.contract.at(accountSettings.lambdaContractAddress)
                    .then(() => {
                        return setContract.methods.create_asset_provider(
                            JSON.stringify(
                                {
                                    "repositories": [
                                        "utility_company_repo",
                                        "identity_company_repo"
                                    ]
                                }
                            ),
                            'test_suite_sim_provider'
                        ).send();
                    })
                    .then((op) => {
                        return op.confirmation(1).then(() => op);
                    })
                    .then(() => {
                        return setContract.contractViews.get_asset_provider('test_suite_sim_provider').executeView({ viewCaller: contractCallFib });
                    })
                    .then((viewResult) => {
                        provider = viewResult;
                    })
            },
        )
        .then(() => {
            let providerData = JSON.parse(provider.provider_data)

            $('#sim-provider .actions-container').append(
                `<div class="card">
                    <b>Provider (ID: test_suite_sim_provider)</b>
                    <div class="card-body">
                        Provider Repositories
                        <div class="card-list d-flex flex-row justify-content-between">

                        </div>
                    </div>
                </div>`
            )

            providerData.repositories.forEach(element => $("#sim-provider .actions-container .card-list").append(`<div>${element}</div>`));

            showSimResultAlert('Simulation ready, click on "Next step" button to continue', "success");
            $('#btn_init_sim').text("Restart Simulation")
            $("#btn_init_sim").removeClass("disabled");

            $('#btn_next_step').show()
        })
}

function loan_request() {
    showSimResultAlert('1. Loan Request', "info", true);
    appendSimResultAlert('Customer requesting a loan from a Bank', "info");
    $('#sim-bank').addClass("sim-con-active animate__animated")
}

function luw_initiation() {
    disableNextStep()
    showSimResultAlert('2. LUW Initiation', "info", true);
    appendSimResultAlert('The Bank application sends a request for a new LUW to the Coordinator', "info");
    $('.con-bank-coordinator').removeClass("invisible")
    $('.con-bank-coordinator').addClass("con-active animate__animated")

    delay(2000)
        .then(() => {
            appendSimResultAlert("The Coordinator calls the Asset Twin Tracing contract")
            $('.con-coordinator-att').addClass("con-active animate__animated")
            disableNextStep()

            const accountSettings = readUISettings();

            return tezosSim.contract.at(accountSettings.lambdaContractAddress)
                .then((contract) => {
                    appendSimResultAlert("The Asset Twin Tracing contract calls the LUW contract and generates a new LUW. Please wait while the LUW is created...")
                    $('.con-att-luw').addClass("con-active animate__animated")

                    return contract.methods.create_luw('tz1Kjd9kg5aHn9zGsN1tnNb9HwdwbuxLbpHu', 'test_suite_sim_provider').send();
                })
                .then((op) => {
                    return op.confirmation(1).then(() => op);
                })
                .then((data) => {
                    simLuwId = data.results[0].metadata.internal_operation_results[1].result.storage.args[1].args[0]["int"] - 1
                    appendSimResultAlert(`The LUW with ID ${simLuwId} has been created <a target="_blank" href="${browser_operations_url + data.hash}">See Operation</a>`)
                    $('#sim-luw .actions-container').append(
                        `<div class="card">
                            <b>LUW (ID: ${simLuwId}, Status: active)</b>
                            <div class="card-body">
                                LUW Repositories
                                <div class="card-list d-flex flex-row justify-content-between">

                                </div>
                            </div>
                        </div>`
                    )

                    

                    return delay(500);
                })
                .then(() => {
                    appendSimResultAlert(`3. The ID of the new LUW (${simLuwId}) is returned to the Bank for future transactions`)

                    $('#sim-bank .actions-container').append(
                        `<div class="card">
                            LUW (ID: ${simLuwId})
                        </div>`
                    )

                    return delay(500);
                })
                .catch((error) => {
                    showSimResultAlert(error.message, null, "danger");
                });
        }).then(() => {
            enableNextStep()
        });
}

function request_proof_residence_address() {
    disableNextStep()
    $('#sim-bank').addClass("sim-con-active animate__animated")
    showSimResultAlert('The Bank application will now initiate KYC processes', "info");

    delay(4000)
        .then(() => {
            appendSimResultAlert("4. Request Proof of Residence", true);
            appendSimResultAlert("The Bank application sends an outside request to an Identity Verification Company, for the Customer's Proof of Residence. The Coordinator endpoint and LUW ID are contained in the request");
            $('#sim-utility .actions-container').append(
                `<div class="card">
                    LUW (ID: ${simLuwId})
                </div>`
            )
            $('.con-coordinator-utility').removeClass("invisible")
            $('#sim-utility').addClass("sim-con-active animate__animated")
            return delay(4000)
        }).then(() => {
            appendSimResultAlert("5. Request Proof of Address", true);
            appendSimResultAlert("It also sends an outside request to an Utility Company, for the Customer's Proof of Address. The Coordinator endpoint and the LUW ID are also contained in the request");
            $('#sim-ivc .actions-container').append(
                `<div class="card">
                    LUW (ID: ${simLuwId})
                </div>`
            )
            $('.con-coordinator-ivc').removeClass("invisible")
            $('#sim-ivc').addClass("sim-con-active animate__animated")
            return delay(500)
        }).then(() => {
            enableNextStep()
        });
}

function persist_proof_residence_address() {
    disableNextStep()
    showSimResultAlert("6-7, 10-11. Persist and Bind Proofs", "info", true);

    $('.con-ivc-repo').addClass("con-active animate__animated")
    $('.con-utility-repo').addClass("con-active animate__animated")

    appendSimResultAlert('The Utility and Identity Verification companies, persist the requested data in their respective repositories');

    $('#sim-ivc-repo .actions-container').append(
        `<div class="card">
            Proof of Residence
        </div>`
    )

    $('#sim-utility-repo .actions-container').append(
        `<div class="card">
            Proof of Address
        </div>`
    )

    delay(4000)
        .then(() => {
            appendSimResultAlert("After persisting the data, both companies contact the Coordinator to update the LUW and include their repositories");
            $('.con-coordinator-ivc').addClass("con-active animate__animated")
            $('.con-coordinator-utility').addClass("con-active animate__animated")

            return delay(4000)
        }).then(() => {
            appendSimResultAlert("The Coordinator contacts the Asset Twin Tracing contract to confirm the repositories corresponding to the Provider");
            $('.con-coordinator-att').addClass("con-active animate__animated")
            $('.con-att-provider').addClass("con-active animate__animated")

            return delay(4000)
        }).then(() => {
            const accountSettings = readUISettings();

            $('.con-att-provider').removeClass("con-active animate__animated")
            
            appendSimResultAlert("The Coordinator contacts the Asset Twin Tracing contract to pass the information and update the LUW");
            $('.con-att-luw').addClass("con-active animate__animated")

            return tezosSim.contract.at(accountSettings.lambdaContractAddress)
                .then((contract) => {
                    return contract.methods.add_luw_repository(simLuwId, 'identity_company_repo').send();
                })
                .then((op) => {
                    return op.confirmation(1).then(() => op);
                })
                .then((op) => {
                    appendSimResultAlert(`Identity company repo added <a target="_blank" href="${browser_operations_url + op.hash}">See Operation</a>`);
                    
                    $("#sim-luw .actions-container .card-list").append(
                        `<div id="luw_identity_company_repo" class="d-flex flex-column">
                            <div>identity_company_repo</div>
                            <div class="status">open</div>
                        </div>`
                    )
                    
                    return tezosSim.contract.at(accountSettings.lambdaContractAddress)
                        .then((contract) => {
                            return contract.methods.add_luw_repository(simLuwId, 'utility_company_repo').send();
                        })
                        .then((op) => {
                            return op.confirmation(1).then(() => op);
                        })
                        .then(() => {
                            appendSimResultAlert(`Utility company repo added <a target="_blank" href="${browser_operations_url + op.hash}">See Operation</a>`);
                            $("#sim-luw .actions-container .card-list").append(
                                `<div id="luw_utility_company_repo" class="d-flex flex-column">
                                    <div>utility_company_repo</div>
                                    <div class="status">open</div>
                                </div>`
                            )
                            return delay(500)
                        })
                        .catch((error) => {
                            showSimResultAlert(error.message, null, "danger");
                        });
                })
                .catch((error) => {
                    showSimResultAlert(error.message, null, "danger");
                });
        }).then(() => {
            enableNextStep()
        });
}

function register_proof_residence_address() {
    showSimResultAlert('The Proof of Residence and Address hashes are registered to the Asset Twin Tracing contract, either directly or part of a Merkle Tree', "info");
    $('.con-ivc-repo').addClass("con-active animate__animated")
    $('.con-utility-repo').addClass("con-active animate__animated")
    $('#sim-ivc').addClass("sim-con-active animate__animated")
    $('#sim-utility').addClass("sim-con-active animate__animated")
    $('#sim-asset').addClass("sim-con-active animate__animated")

    $('#sim-asset .actions-container').append(
        `<div class="card">
            <div class="card-body">
                Asset Twins
                <div class="card-list">
                    <div class="card">Proof of Residence Hash</div>
                    <div class="card">Proof of Address Hash</div>
                </div>
            </div>
        </div>`
    )
}

function fetch_proof_residence_address() {
    showSimResultAlert("8, 12. Fetch Proofs", "info", true);
    appendSimResultAlert('The Bank application fetches the requested info');
    $('.con-coordinator-ivc').addClass("con-active animate__animated")
    $('.con-coordinator-utility').addClass("con-active animate__animated")
    $('.con-ivc-repo').addClass("con-active animate__animated")
    $('.con-utility-repo').addClass("con-active animate__animated")
    $('.con-bank-coordinator').addClass("con-active animate__animated")
}

function bank_register_proof_residence_address() {
    showSimResultAlert("9, 13. Register KYC Documents", "info", true);
    appendSimResultAlert('The Bank application registers the fetched documents in its own repository');
    $('.con-bank-repo').addClass("con-active animate__animated")
    $('#sim-bank-repo .actions-container').append(
        `<div class="card">
            <div class="card-body">
                Asset Twins
                <div class="card-list">
                    <div class="card">Proof of Residence Hash</div>
                    <div class="card">Proof of Address Hash</div>
                </div>
            </div>
        </div>`
    )
}

function KYC_check() {
    disableNextStep()
    $('#sim-bank').addClass("sim-con-active animate__animated")
    showSimResultAlert('14 KYC Check', "info", true);
    appendSimResultAlert('Having the required info, the Bank performs its KYC functions');

    delay(4000)
        .then(() => {
            appendSimResultAlert("Let's suppose that during the KYC process, the Bank found incomplete info about the Customer's address");
            return delay(500)
        }).then(() => {
            enableNextStep()
        });
}

function request_additional_info() {
    showSimResultAlert('15. Request additional info', "info", true);
    appendSimResultAlert("The Bank will request some additional info from the Utility company about the Customer's address");
    
    $('#sim-bank').addClass("sim-con-active animate__animated")
    $('#sim-utility').addClass("sim-con-active animate__animated")
}

function update_proof_address() {
    disableNextStep()
    showSimResultAlert('15. Request additional info', "info", true);
    appendSimResultAlert('The Utility company will update the Proof of Address');
    $('#sim-utility').addClass("sim-con-active animate__animated")
    $('#sim-utility-repo').addClass("sim-con-active animate__animated")
    $('#sim-utility-repo .actions-container').append('<div class="card">Updated Proof of Address</div>')
    jQuery('.sim-container').connections('update');
    
    delay(4000)
        .then(() => {
            appendSimResultAlert('16. Update Proof of Address', true);
            appendSimResultAlert("Asynchronously, the updated Proof of Address will be registered on the Asset Twin Tracing contract");
            $('.con-utility-repo').addClass("con-active animate__animated")
            $('.con-coordinator-utility').addClass("con-active animate__animated")
            $('.con-coordinator-aat').addClass("con-active animate__animated")
            $('.con-aat-asset').addClass("con-active animate__animated")
            $('#sim-asset .actions-container .card-list').append('<div class="card">Updated Proof of Address Hash </div>')

            return delay(500)
        }).then(() => {
            enableNextStep()
        });
}

function fetch_updated_proof_address() {
    showSimResultAlert('17-18. Fetch and Update Proof of Address', "info", true);

    appendSimResultAlert('The Bank application requests the updated Proof of Address and registers it');
    $('.con-coordinator-utility').addClass("con-active animate__animated")
    $('.con-utility-repo').addClass("con-active animate__animated")
    $('.con-bank-coordinator').addClass("con-active animate__animated")
    $('#sim-bank .actions-container .card-list').append('<div class="card">Updated Proof of Address Hash </div>')
}

function prepare_to_commit() {
    disableNextStep()

    showSimResultAlert('19. Prepare to commit', "info", true);
    appendSimResultAlert('Having performed the KYC checks, the Bank application contacts the Coordinator to commit the LUW');
    $('.con-bank-coordinator').addClass("con-active animate__animated")

    delay(4000)
        .then(() => {
            appendSimResultAlert("The Coordinator will contact the Asset Twin Tracing contract to prepare the LUW for commit");
            $('.con-coordinator-att').addClass("con-active animate__animated")
            $('.con-att-luw').addClass("con-active animate__animated")

            return delay(4000)
        }).then(() => {
            const accountSettings = readUISettings();

            return tezosSim.contract.at(accountSettings.lambdaContractAddress)
                .then((contract) => {
                    return contract.methods.change_luw_state(simLuwId, 2).send();
                })
                .then((op) => {
                    return op.confirmation(1).then(() => op);
                })
                .then((op) => {
                    appendSimResultAlert(`The LUW's state is now set to "prepare_to_commit". No repositories can be added to the LUW from now on <a target="_blank" href="${browser_operations_url + op.hash}">See Operation</a>`);
                    $('#sim-luw .actions-container b').html(`<b>LUW (ID: ${simLuwId}, Status: prepare_to_commit)</b>`)
                    return delay(500)
                })
                .catch((error) => {
                    showSimResultAlert(error.message, null, "danger");
                });
        }).then(() => {
            enableNextStep()
        });
}

function update_repositories() {
    disableNextStep()
    showSimResultAlert('The Coordinator will now contact the repositories to check their status', "info");
    $('.con-coordinator-ivc').addClass("con-active animate__animated")
    $('.con-coordinator-utility').addClass("con-active animate__animated")
    $('.con-ivc-repo').addClass("con-active animate__animated")
    $('.con-utility-repo').addClass("con-active animate__animated")

    delay(4000)
        .then(() => {
            const accountSettings = readUISettings();

            appendSimResultAlert("If the status of the Repositories is in the correct state, their status on the LUW will be updated");
            $('.con-coordinator-att').addClass("con-active animate__animated")
            $('.con-att-luw').addClass("con-active animate__animated")

            return tezosSim.contract.at(accountSettings.lambdaContractAddress)
                .then((contract) => {
                    return contract.methods.change_luw_repository_state(simLuwId, 'identity_company_repo', 2).send();
                })
                .then((op) => {
                    return op.confirmation(1).then(() => op);
                })
                .then((op) => {
                    appendSimResultAlert(`Identity company repository status changed to "ready" <a target="_blank" href="${browser_operations_url + op.hash}">See Operation</a>`);
                    $("#luw_identity_company_repo .status").html("ready")
                    
                    return tezosSim.contract.at(accountSettings.lambdaContractAddress)
                        .then((contract) => {
                            return contract.methods.change_luw_repository_state(simLuwId, 'utility_company_repo', 2).send();
                        })
                        .then((op) => {
                            return op.confirmation(1).then(() => op);
                        })
                        .then(() => {
                            appendSimResultAlert(`Utility company repository status changed to "ready" <a target="_blank" href="${browser_operations_url + op.hash}">See Operation</a>`);
                            $("#luw_utility_company_repo .status").html("ready")
                            return delay(500)
                        })
                        .catch((error) => {
                            showSimResultAlert(error.message, null, "danger");
                        });
                })
                .catch((error) => {
                    showSimResultAlert(error.message, null, "danger");
                });
        }).then(() => {
            enableNextStep()
        });
}

function commit() {
    disableNextStep()

    showSimResultAlert('20. Commit', "info", true);
    appendSimResultAlert('The LUW will now be committed');
    $('#sim-luw').addClass("sim-con-active animate__animated")

    delay(500)
        .then(() => {
            const accountSettings = readUISettings();

            return tezosSim.contract.at(accountSettings.lambdaContractAddress)
                .then((contract) => {
                    return contract.methods.change_luw_state(simLuwId, 3).send();
                })
                .then((op) => {
                    return op.confirmation(1).then(() => op);
                })
                .then((op) => {
                    appendSimResultAlert(`The LUW's state is now set to "committed". <a target="_blank" href="${browser_operations_url + op.hash}">See Operation</a>`);
                    $('#sim-luw .actions-container b').html(`<b>LUW (ID: ${simLuwId}, Status: committed)</b>`)
                    $("#luw_identity_company_repo .status").html("committed")
                    $("#luw_utility_company_repo .status").html("committed")
                    return delay(500)
                })
                .catch((error) => {
                    showSimResultAlert(error.message, null, "danger");
                });
        }).then(() => {
            enableNextStep()
        });
}

function wrapup() {
    disableNextStep()

    showSimResultAlert('21, 22-23. KYC Completion and Fee Payment', "info", true);
    appendSimResultAlert('With KYC completed, the banks sends the result back to the customer, at the same time paying the required fees to the Verification and Utility companies');
    $('#sim-bank').addClass("sim-con-active animate__animated")
    $('#sim-utility').addClass("sim-con-active animate__animated")
    $('#sim-ivc').addClass("sim-con-active animate__animated")

    delay(500)
        .then(() => {
            appendSimResultAlert('The simulation is now complete. If you want to rerun the simulation, click on the "Initiate Simulation" button');
            $('#btn_next_step').hide()
            enableNextStep()
        });
}

$("#btn_next_step").click(function () {
    clearSim()

    let current_step = current_scenario.shift()
    eval(current_step)()
});

function clearSim() {
    $("connection").removeClass("con-active con-blocked animate__animated")
    $(".sim-container").removeClass("sim-con-active sim-con-blocked animate__animated")
}

function enableNextStep() {
    $("#btn_next_step").removeClass("disabled");
    $("#btn_init_sim").removeClass("disabled");
    $("#btn_next_step").text("Next Step");
}

function disableNextStep() {
    $("#btn_next_step").addClass("disabled");
    $("#btn_init_sim").addClass("disabled");
    $("#btn_next_step").text("Please Wait...");
}

$(document).ready(initUI);
