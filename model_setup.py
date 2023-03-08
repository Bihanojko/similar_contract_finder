"""
model_setup.py

This script loads a collection of contracts, pre-processes and encodes them using
SentenceTransformer and fits a k-NN model on the encoded embeddings to predict
the most similar contracts for a given input. The trained model is then saved
using pickle for later use.

Author: Nikola Valesova
Date: 23. 2. 2023
"""

# Import libraries
from os import listdir, path

import numpy.typing as npt
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from typing import Dict, List, Union

from app.contract_similarity_model.contract_similarity_model_class import ContractSimilarityModel
# Import functionality shared across modules
from app.functions import *

def process_contracts(sentence_transformer: SentenceTransformer) -> Dict[str, List[Union[str, npt.ArrayLike]]]:
    """Load all contract files, create embeddings from their content
    and return all contract names, their contents and embeddings"""
    contract_names = []
    contract_codes = []
    contract_vectors = []

    subfolders = listdir("contracts")

    for subfolder in sorted(subfolders):
        print(subfolder)

        contract_files = listdir(path.join("contracts", subfolder))

        for contract_file in sorted(contract_files):
            with open(path.join("contracts", subfolder, contract_file)) as cf:
                contract_names.append(path.join(subfolder, contract_file))
                contract_code = cf.read()
                contract_codes.append(contract_code)
                contract_code_wo_comments = remove_comments(contract_code)
                contract_vectors.append(sentence_transformer.encode(contract_code_wo_comments))
    
    return {
        "contract_names": contract_names,
        "contract_codes": contract_codes,
        "contract_vectors": contract_vectors,
    }

def fit_similarity_model(contract_vectors: List[npt.ArrayLike]) -> NearestNeighbors:
    """Initialize and fit the k-NN model on the document embeddings"""
    knn = NearestNeighbors(n_neighbors=5, algorithm='brute')
    knn.fit(contract_vectors)
    return knn

def setup_similarity_model() -> None:
    """Load, train and persist the contract similarity model"""
    sentence_transformer = SentenceTransformer(path.join("sentence-transformers", "all-MiniLM-L6-v2"))
    contract_data = process_contracts(sentence_transformer)
    knn = fit_similarity_model(contract_data["contract_vectors"])
    wrapped_model = ContractSimilarityModel(sentence_transformer, knn, contract_data["contract_names"], contract_data["contract_codes"], contract_data["contract_vectors"])

    # Persist the model
    pickle.dump(wrapped_model, open(path.join("app", "contract_similarity_model", "model.pkl"), 'wb'))

if __name__ == '__main__':
    setup_similarity_model()
