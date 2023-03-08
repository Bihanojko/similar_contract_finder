"""
test_model.py

This script tests the trained model and the similar contract finder functionality
outside of the API.

Usage:
A) Random input contract selection
    $ python test_model.py
B) Apply the model on a speficic contract
    $ python test_model.py {path to contract}

Author: Nikola Valesova
Date: 23. 2. 2023
"""

# Import libraries
from os import listdir, path
import sys

import json
import numpy.typing as npt
import random

# Import functionality shared across modules
from app.functions import *
from app.contract_similarity_model.contract_similarity_model_class import *
from app.contract_similarity_model.custom_unpickler_class import *

def get_similar_contract_codes(contract_similarity_model: ContractSimilarityModel, model_input_emb: npt.ArrayLike) -> str:
    # Use the k-NN model to find the 5 most similar documents to a given query document
    indices = contract_similarity_model.similarity_model.kneighbors(model_input_emb.reshape(1, -1), return_distance=False)

    # Extract the similar contract codes based on their indices
    most_similar_contracts = [contract_similarity_model.contract_codes[i] for i in indices[0]]

    # Transform the response to a formatted json object
    most_similar_contracts_response = json.dumps(most_similar_contracts, indent=4)
    return most_similar_contracts_response

def find_similar_contracts(contract_code: str) -> str:
    contract_code_wo_comments = remove_comments(contract_code)

    # Load the stored pickle model
    contract_similarity_model = CustomUnpickler(open(path.join("app", "contract_similarity_model", "model.pkl"), 'rb')).load()

    # Transform the input contract into an embedded vector
    model_input_emb = contract_similarity_model.sentence_transformer.encode(contract_code_wo_comments)

    return get_similar_contract_codes(contract_similarity_model, model_input_emb)

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
 
    with open(contract_filepath) as cf:
        contract_code = cf.read()

    print(find_similar_contracts(contract_code))
