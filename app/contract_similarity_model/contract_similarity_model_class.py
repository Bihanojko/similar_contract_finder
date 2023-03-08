"""
contract_similarity_model_class.py

This script contains a class definition of the ContractSimilarityModel object. 

Author: Nikola Valesova
Date: 23. 2. 2023
"""

class ContractSimilarityModel():
    def __init__(self, sentence_transformer, knn, contract_names, contract_codes, encoded_contracts):
        # an instance of the SentenceTransformer class which is used to encode contract text into vector representations
        self.sentence_transformer = sentence_transformer
        # an instance of the KNN model used to perform nearest neighbor search on the encoded contract vectors
        self.similarity_model = knn
        # strings representing the names of the contracts that are indexed by this model
        self.contract_names = contract_names
        # strings representing the codes of the contracts that are indexed by this model
        self.contract_codes = contract_codes
        # numpy array of shape (n, d) where n is the number of contracts indexed and d is the dimensionality of the encoded vectors
        self.encoded_contracts = encoded_contracts
