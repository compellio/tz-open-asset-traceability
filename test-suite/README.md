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

### Register Asset Twin

The use case for which the client Regisrers an Asset Twin to the blockchain.

**Parameters:**

**Asset Twin Hash (string)** - A string representing a hash of an Asset Twin. For example:

```
71fc1177f6a2b6c145bde55431690d948511ba36e2e4a1d50130549f65b4b5cb
```
> **Warning**
> This is just an example. The asset twin hash should be unique. Trying to add the same hash twice will cause an error.

**Provider DID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```
> **Warning**
> This is just an example. The DID identifies the provider and should be unique. Trying to add the same DID twice will cause an error.
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

**Provider DID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

### Get Provider

The use case for which the client retrieves the Asset Twin data registered in the blockchain.

**Parameters:**

**Asset Twin Hash (string)** - A string representing a hash of an Asset Twin. For example:

```
71fc1177f6a2b6c145bde55431690d948511ba36e2e4a1d50130549f65b4b5cb
```

**Provider DID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

### Create Provider

The use case for which the client submits their DID document to the blockchain.

**Parameters:**

**Provider DID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

**Provider Data (string)** - An provider DID document in JSON format. The entry will be considered as a string parameter. For example:

```
{ "@context": "https://w3id.org/did/v1", "id": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "verificationMethod": [ { "id": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "type": "EcdsaSecp256k1VerificationKey2019", "controller": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "publicKeyJwk": { "kty": "EC", "crv": "secp256k1", "x": "n03trG-1sWidluyYQ2gcKrgYE94rMkLIArZCHjv2GpI", "y": "6__x_vqe0nBGYf7azbQ1_VvvuCafG5MhhUPNvYp-Mak" } } ], "authentication": [ "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1" ], "assertionMethod": [ "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1" ] }
```

In case of using direct input, you should manually escape characters, so the above JSON should have the following form:

```
'{\"@context\":\"https:\/\/w3id.org\/did\/v1\",\"id\":\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\",\"verificationMethod\":[{\"id\":\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\",\"type\":\"EcdsaSecp256k1VerificationKey2019\",\"controller\":\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\",\"publicKeyJwk\":{\"kty\":\"EC\",\"crv\":\"secp256k1\",\"x\":\"n03trG-1sWidluyYQ2gcKrgYE94rMkLIArZCHjv2GpI\",\"y\":\"6__x_vqe0nBGYf7azbQ1_VvvuCafG5MhhUPNvYp-Mak\"}}],\"authentication\":[\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\"],\"assertionMethod\":[\"did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1\"]}'
```

### Provider Status Update

The use case for which the client sets their provider status on the blockchain.

**Parameters:**

**Provider DID (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

**Status ID (nat) - Optional** - This is the ID of the status as listed in `provider_statuses` in the `Registry Logic` contract.

