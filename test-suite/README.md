# Tezos Open Asset Traceability

You will need to have a **Wallet** on an existing Tezos Testnet. We have used **Jakartanet** for our tests.

For implementing the test process, we created a test suite that relies on the [Taquito](https://tezostaquito.io/) library in order to design and perform test calls to smart contracts. Interfacing with the **Wallet** is done through the [Beacon SDK](https://github.com/airgap-it/beacon-sdk).

## Installation

For installation of the Test Suite, you will have to use the latest versions of Node.js and npm

1. Navigate to the test-suite folder
2. Open your Command Console
3. Run `npm install`
4. Run `npm start`

> **Warning**
> Running a new version of the test-suite, requires you to clean the cache. You can do so by running `rm -rf .parcel-cache`

If the installation was successful, a localhost URL will appear on the console, for example, http://localhost:1234. Open your browser and enter this URL. If there are no errors you can start testing.

## Test scenarios

### Create Provider

The use case for which the client submits their ID document to the blockchain.

**Parameters:**

**Provider ID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

**Provider Data (string)** - An provider ID document in JSON format. The entry will be considered as a string parameter. For example:

```
{ "@context": "https://w3id.org/did/v1", "id": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "verificationMethod": [ { "id": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "type": "EcdsaSecp256k1VerificationKey2019", "controller": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "publicKeyJwk": { "kty": "EC", "crv": "secp256k1", "x": "n03trG-1sWidluyYQ2gcKrgYE94rMkLIArZCHjv2GpI", "y": "6__x_vqe0nBGYf7azbQ1_VvvuCafG5MhhUPNvYp-Mak" } } ], "authentication": [ "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1" ], "assertionMethod": [ "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1" ] }
```

In case of using direct input, you should manually escape characters, so the above JSON should have the following form:

```
'{\"@context\":\"https:\/\/w3id.org\/did\/v1\",\"id\":\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\",\"verificationMethod\":[{\"id\":\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\",\"type\":\"EcdsaSecp256k1VerificationKey2019\",\"controller\":\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\",\"publicKeyJwk\":{\"kty\":\"EC\",\"crv\":\"secp256k1\",\"x\":\"n03trG-1sWidluyYQ2gcKrgYE94rMkLIArZCHjv2GpI\",\"y\":\"6__x_vqe0nBGYf7azbQ1_VvvuCafG5MhhUPNvYp-Mak\"}}],\"authentication\":[\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\"],\"assertionMethod\":[\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\"]}'
```

### Get Provider

The use case for which the client retrieves the Asset Twin data registered in the blockchain.

**Parameters:**

**Asset Twin Hash (string)** - A string representing a hash of an Asset Twin. For example:

```
71fc1177f6a2b6c145bde55431690d948511ba36e2e4a1d50130549f65b4b5cb
```

**Provider ID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

### Provider Data Update

The use case for which the client updates the provider's data on the blockchain.

**Parameters:**

**Provider ID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

### Provider Status Update

The use case for which the client sets their provider status on the blockchain.

**Parameters:**

**Provider ID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

**Status ID (nat) - Optional** - This is the ID of the status as listed in `provider_statuses` in the `Registry Logic` contract.

### Provider Owner Update

The use case for which the client updates the provider's owner on the blockchain.

**Parameters:**

**Provider ID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

**Owner (address)** - The wallet address of the new owner. A valid wallet address is required. Example:

```
tz1hvMUvkmWx27auF3mX7dZrHBpbNoGUNWSc
```

> **Warning**
> After running this script, you will only be able to update the Provider using the wallet that corresponds to the public address inputed in `Owner (address)`

**Provider Data (string)** - An provider ID document in JSON format. The entry will be considered as a string parameter. See provider creation above for example.

### Register Asset Twin

The use case for which the client Regisrers an Asset Twin to the blockchain.

**Parameters:**

**Asset Twin Hash (string)** - A string representing a hash of an Asset Twin. For example:

```
71fc1177f6a2b6c145bde55431690d948511ba36e2e4a1d50130549f65b4b5cb
```
> **Warning**
> This is just an example. The asset twin hash should be unique. Trying to add the same hash twice will cause an error.

**Provider ID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```
> **Warning**
> This is just an example. The ID identifies the provider and should be unique. Trying to add the same ID twice will cause an error.
> 

**Endpoint (string)** - A string defining the endpoint where the Asset Twin registration can be verified. For example:

```
https://example.com/registration/
```

### Fetch Asset Twin
The use case for which the client requests the data of an Asset Twin that is stored in the blockchain.

**Parameters:**

**Asset Twin Hash (string)** - A string representing a hash of an Asset Twin. For example:

```
71fc1177f6a2b6c145bde55431690d948511ba36e2e4a1d50130549f65b4b5cb
```

**Provider ID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

### LUW Creation

The use case for which the client creates a LUW on the blockchain.

**Parameters:**

**Provider ID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

**Service Endpoint (string)** - A valid Address defining the endpoint service of the LUW. This can be either a wallet or a contract address. Example:

```
tz1hvMUvkmWx27auF3mX7dZrHBpbNoGUNWSc
```

### LUW State Change

The use case for which the client changes the state of a LUW on the blockchain.

**Parameters:**

**LUW ID (nat)** - A nat defining the id of a LUW.

States are pre-defined and can be chosen by clicking the respective button.

### LUW Repository Addition

The use case for which the client adds a repository to a LUW on the blockchain.

> **Warning**
> LUW state should be set to "Active" for adding new repositories.
> 

**Parameters:**

**LUW ID (nat)** - A nat defining the id of a LUW.

**Repository ID (string)** - A string defining the ID of the Repository.

### LUW Repository State Change

The use case for which the client changes the state of a LUW repository on the blockchain.

**Parameters:**

**LUW ID (nat)** - A nat defining the id of a LUW.

**Repository ID (string)** - A string defining the ID of the Repository.

States are pre-defined and can be chosen by clicking the respective button.

### Fetch LUW

The use case for which the client retrieves the LUW data registered in the blockchain.

**Parameters:**

**LUW ID (nat)** - A nat defining the id of a LUW.

## Simulation

The simulation tab is used for showing a real-life use case of the project's smart contracts. The simulation is separated in multiple steps, each explaining what happens in the background. Some calls are real-time calls to the smart contracts, so unless there is an error, please wait for the calls to finish.

> **Warning**
> The first time a simulation is initiated for a fresh set of contracts, there may be a delay while everything is set up
> 