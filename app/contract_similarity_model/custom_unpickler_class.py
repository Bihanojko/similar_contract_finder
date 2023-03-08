"""
custom_unpickler_class.py

This script contains the definition of the custom unpikler class
which is necessary for correnct unpiklicking of the saved model.

Author: Nikola Valesova
Date: 23. 2. 2023
"""

# Import libraries
import pickle

class CustomUnpickler(pickle.Unpickler):
    # Import a custom class called "ContractSimilarityModel" from a specific file path
    # since without its definition being known, the unpickling fails
    def find_class(self, module, name):
        if name == 'ContractSimilarityModel':
            from .contract_similarity_model_class import ContractSimilarityModel
            return ContractSimilarityModel
        return super().find_class(module, name)
