# Similar contracts finder

A smart contract similarity tool that returns the top 5 similar contracts for a given smart contract solidity file.

## Usage

1. cd ..
2. make install

Execute

```
import requests

contract_filepath = {PATH_TO_CONTRACT}
 
url = "http://localhost:4500/find_similar_contracts"

with open(contract_filepath) as cf:
    event_data = {"contract_code": cf.read()}
    r = requests.post(url, json=event_data)
    print(r.json())

```
