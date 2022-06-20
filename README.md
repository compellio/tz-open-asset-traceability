# Tezos Open Asset Traceablility

Open Asset Traceablility smart contracts on tezos.

## Testing

There are several scenarios included for testing the functionality of the contracts. Tests should be ran seperately for each contract file in the root folder of this project. These scenarios will be desribed below.

### assetProvider.py

**Command**

`~/smartpy-cli/SmartPy.sh test assetProvider.py testing`

**Scenarios**
|  Scenario |  Outcome  | Failure Reason |
| ------------ | ------------ | ------------ |
| Create Asset Provider with UID A | Success | - |
| Verify Asset Provider creation with UID A | Success | - |
| Create Asset Provider with UID A | Failure | Asset Provider with Record A already exists |
| Create Asset Provider with UID B | Success | - |
| Verify Asset Provider creation with UID B | Success | - |

### assetTwinTracing.py

**Command**

`~/smartpy-cli/SmartPy.sh test assetTwinTracing.py testing`

**Scenarios**
|  Scenario |  Outcome  | Failure Reason |
| ------------ | ------------ | ------------ |
| Create Asset Twin with Hash A | Success | - |
| Verify Asset Twin creation with Hash A | Success | - |
| Create Asset Twin with Hash A | Failure | Asset Provider with Record A already exists |
| Create Asset Twin with Hash B | Success | - |
| Verify Asset Twin creation with Hash B | Success | - |