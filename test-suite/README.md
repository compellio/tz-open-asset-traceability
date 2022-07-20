# Tezos Open Asset Traceability

You will need to have a **Wallet** on an existing Tezos Testnet. We have used **Jakartanet** for our tests.

For implementing the test process, we created a test suite that relies on the [Taquito](https://tezostaquito.io/) library in order to design and perform test calls to smart contracts. Interfacing with the **Wallet** is done through the [Beacon SDK](https://github.com/airgap-it/beacon-sdk).

## Installation

For installation of the Test Suite, you will have to use the latest versions of Node.js and npm

1. Navigate to the test-suite folder
2. Open your Command Console
3. Run `npm install`
4. Run `npm start`

If the installation was successful, a localhost URL will appear on the console, for example, http://localhost:1234. Open your browser and enter this URL. If there are no errors you can start testing.

## Test scenarios