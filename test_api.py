"""
test_api.py

This script tests the trained model and the similar contract finder functionality
directly via the API.

Usage:
A) Random input contract selection
    $ python test_api.py
B) Apply the model on a speficic contract
    $ python test_api.py {path to contract}

Author: Nikola Valesova
Date: 23. 2. 2023
"""

# Import libraries
from os import listdir, path
import sys

import random
import requests

if __name__ == '__main__':
    # no parameter passed, selecting random input
    if len(sys.argv) == 1:
        subfolder = random.choice(listdir("contracts"))
        file = random.choice(listdir(path.join("contracts", subfolder)))
        contract_filepath = path.join("contracts", subfolder, file)
        print(f"Selected input contract: {contract_filepath}")
    # input contract specified, using it as the input
    else:
        # NOTE:        
        # no checks for validity are currently applied on the user input
        # as this solution is just an MVP for now, and it is intended only 
        # for the usage by IT experts, that understand the default error message
        contract_filepath = sys.argv[1]
 
    url = "http://localhost:4500/find_similar_contracts"

    with open(contract_filepath) as cf:
        event_data = {"contract_code": cf.read()}
        r = requests.post(url, json=event_data)
        print(r.json())
