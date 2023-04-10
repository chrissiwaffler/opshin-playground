# Gift smart contract with Opshin on Cardano
- this example heavily builds on the [tutorial for smart contract by PyCardano](https://pycardano.readthedocs.io/en/latest/guides/plutus.html)
- I am adding some minor variations here and there e.g., some print statements, some comments, etc.

## Setup
### Create your own project id [at Blockfrost.io](https://blockfrost.io/#introduction)
- create a project id for the **Preview Testnet**
- create a new file named `config.py` that looks like:
    ``` python
    blockfrost_project_id = "your_project_id"
    ```

### Creating your own keys (needed)
- create your own keys pairs
- 2 are needed in order to correctly execute `deploy_gift.py` and `retrieve_gift.py`
- follow this procedure, so the keys are in the correct folder structure
```shell
$ mkdir keys && cd keys
$ mkdir key1 && mkdir key2

# first keypair
$ cd key1
$ cardano-cli address key-gen \
    --verification-key-file payment.vkey \
    --signing-key-file payment.skey
$ cd ..

# second keypair
$ cd key2
$ cardano-cli address key-gen \
    --verification-key-file payment.vkey \
    --signing-key-file payment.skey
$ cd ../..
```
## Procedure
1. Build the smart contract
2. Deploy the smart contract (the gift)
3. retrieve the gift with another address

### Build the smart contract

``` shell
$ python3.8 -m venv venv
$ source venv/bin/activate
$ pip install opshin
$ opshin build gift.py
```

### Deploy the smart contract
- simply execute the python file `deploy_gift.py` by executing it
- example command: `python3 deploy_gift.py`

### Retrieve the gift with another address
- After running `deploy_gift.py`, copy the script address and replace it with the existing one (`script_address`)
- run the script with for example: `python3 retrieve_gift.py`
- check Output of the transaction with the transaction hash of the console:
    - the taker address should have gotten ~ 25 ADA
    - around ~ 24 ADA should be return to the script address
    - the rest < 1 ADA are tx-fees
