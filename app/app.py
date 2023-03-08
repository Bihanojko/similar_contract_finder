"""
app.py

This script provides a RESTful API for finding similar smart contracts. It uses
a pre-trained model to generate vector embedding from the given contract and 
the k-nearest neighbors algorithm to find the top 5 most similar contracts 
to a given input contract code.

Author: Nikola Valesova
Date: 23. 2. 2023
"""

# Import libraries
from flask import Flask, request, abort, jsonify
import json
import numpy.typing as npt

# k-NN model is used but import of the module is not needed
# from sklearn.neighbors import NearestNeighbors

# Import functionality shared across modules
from functions import *
from contract_similarity_model.contract_similarity_model_class import *
from contract_similarity_model.custom_unpickler_class import *

app = Flask(__name__)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

def get_similar_contract_codes(contract_similarity_model: ContractSimilarityModel, model_input_emb: npt.ArrayLike) -> str:
    # use the k-NN model to find the 5 most similar documents to a given query document
    indices = contract_similarity_model.similarity_model.kneighbors(model_input_emb.reshape(1, -1), return_distance=False)
    
    # extract the similar contract codes based on their indices
    most_similar_contracts = [contract_similarity_model.contract_codes[i] for i in indices[0]]

    # transform the response to a formatted json object
    most_similar_contracts_response = json.dumps(most_similar_contracts, indent=4)
    return most_similar_contracts_response

@app.route("/find_similar_contracts", methods=["POST"])
def find_similar_contracts() -> str:
    contract_code = request.json.get("contract_code")
    if contract_code is None:
        abort(404, description="No contract code provided")
        return jsonify("Check the README for usage example: https://github.com/Bihanojko/similar_contract_finder/blob/main/README.md")

    contract_code_wo_comments = remove_comments(contract_code)

    # load the stored pickle model
    contract_similarity_model = CustomUnpickler(open("contract_similarity_model/model.pkl", 'rb')).load()

    # transform the input contract into an embedded vector
    model_input_emb = contract_similarity_model.sentence_transformer.encode(contract_code_wo_comments)

    return get_similar_contract_codes(contract_similarity_model, model_input_emb)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
