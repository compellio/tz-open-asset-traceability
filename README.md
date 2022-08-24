# Tezos Open Asset Traceablility

Open Asset Traceablility smart contracts on tezos.

## Testing

There are several scenarios included for testing the functionality of the contracts. All Tests are included in a single file - `testScenarios.py`, in the root folder of this project.  To run the tests run the following command:

`~/smartpy-cli/SmartPy.sh test testScenarios.py testing`

The scenarios tested are be desribed seperately, per contract, as follows:

### assetProvider.py

#### Provider Creation

**Scenarios**
|  Scenario |  Outcome  | Failure Reason |
| ------------ | ------------ | ------------ |
| Create Asset Provider with ID A | Success | - |
| Verify Asset Provider creation with UID A | Success | - |
| Create Asset Provider with ID A | Failure | Asset Provider with Record A already exists |
| Create Asset Provider with ID B | Success | - |
| Verify Asset Provider creation with ID B | Success | - |

#### Provider Status Update

**Scenarios**
|  Scenario |  Outcome  | Failure Reason |
| ------------ | ------------ | ------------ |
| Set Asset Provider with ID A as Deprecated with proper Owner (Operator A) | Success | - |
| Verify Asset Provider status set to Deprecated | Success | - |
| Set Asset Provider with ID A as Active with improper Owner (Operator B) | Failure | Improper Owner |
| Set Asset Provider with ID A to Active Status with proper Owner (Operator A) | Success | - |
| Verify Asset Provider status set to Active | Success | - |
| Set Asset Provider with ID A to an improper Status with proper Owner (Operator A) | Failure | Improper Status ID |
| Set Asset Provider with improper ID to Active Status with proper Owner (Operator A) | Failure | Improper Provider ID |

### assetTwinTracing.py

#### Asset Twin Registration

**Scenarios**
|  Scenario |  Outcome  | Failure Reason |
| ------------ | ------------ | ------------ |
| Register Asset Twin with Hash A and Provider A | Success | - |
| Verify Asset Twin creation with Hash A | Success | - |
| Register Asset Twin with Hash A and Provider A | Failure | Asset Provider with Record A already exists |
| Register Asset Twin with Hash A and Provider B | Success | - |
| Register Asset Twin with Hash B and Provider A | Success | - |
| Verify Asset Twin creation with Hash B | Success | - |
| Verify Failure of fetching an Asset Twin with valid Hash A and invalid Provider | Success | - |

### LUW.py

#### LUW creation

**Scenarios**
|  Scenario |  Outcome  | Failure Reason |
| ------------ | ------------ | ------------ |
| Create LUW | Success | - |
| Verify LUW Owner | Success | - |
| Verify LUW State | Success | - |

#### LUW State Change

**Scenarios**
|  Scenario |  Outcome  | Failure Reason |
| ------------ | ------------ | ------------ |
| Alter LUW State with improper Owner (Operator B) | Failure | Improper Owner |
| Alter LUW State to "Prepare to Commit" with proper Owner (Operator A) | Success | - |
| Alter LUW with invalid ID | Failure | LUW ID does not exist |
| Alter LUW with invalid State ID | Failure | State ID does not exist |
| Verify LUW State is set to "Prepare to Commit" | Success | - |