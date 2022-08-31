# Tezos Open Asset Traceablility

Open Asset Traceablility smart contracts on tezos.

## Testing

There are several scenarios included for testing the functionality of the contracts. All Tests were implemented in a single file - `testScenarios.py`, in the root folder of this project.  

The test require the following contract files in order to run successfully:
- assetProvider.py
- assetProviderRepository.py
- assetTwinTracing.py
- LUW.py
- LUWRepository.py

The logic is divided across these several files. Therefore, testing needs to be done using the smartPy IDE (https://smartpy.io/ide), so that the necessary files can be loaded.
The command line client cannot be used due to this limitation.

In order to run the tests, the first step is to store the necessary contracts to the smartPy IDE. 

This can be done by using the **Create Contract** functionality.
The names of the contracts **need to be the same as the file name** (eg. assetProvider.py) in order for the tests to load the contracts successfully.
The create contract process starts with defining the name:

![Create contract process](screenshots/01.png)

Following the definition, the contract code needs to be stored in the contract:

**assetProvider.py**
![assetProvider](screenshots/02.png)

Repeat the process for all necessary contracts:

**assetProvidertRepository.py**
![assetProvidertRepository](screenshots/03.png)


**assetTwinTracing.py**
![assetTwinTracing](screenshots/04.png)

**LUW.py**
![LUW](screenshots/05.png)

**LUWRepository.py**
![LUWRepository](screenshots/06.png)

Finally, the test contract is created, which is the one that will be run:

**testSchenarios.py**
![testSchenarios](screenshots/07.png)

After all contracts are created, the following list can be seen in the List of Stored Contracts:
![loaded_list](screenshots/08.png)

After the contracts are created and the test scenario is also created and loaded, if we hit run then all tests will be executed and the result of the several verification executions will be presented in the output window as follows:
![tests_run](screenshots/09.png)

The list of the test results is presented in the output window:
![test_results](screenshots/10.png)

The difference in coloring between results is due to the verification type.
The blue-colored result verified the successful execution of a test, whereas the brown-colored verified a test case that leads to failure of execution.

For example, this is the test result for the successful flow of Set Provider Status operation , which was verified:
![tests_true](screenshots/12.png)

And this is the test result for the failed flow due to existing issuer of the Set Issuer Active operation, which also was verified that it is handled as expected:
![tests_false](screenshots/11.png)

A test was implemented for the following cases:

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