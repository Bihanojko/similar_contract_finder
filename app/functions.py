"""
functions.py

This script contains the definitions of the functions that are shared across
multiple modules.

Author: Nikola Valesova
Date: 23. 2. 2023
"""

# Import libraries
from re import sub

def remove_comments(contract_code: str) -> str:
    """remove all single-line and multi-line comments"""
    return sub(r"\/\/.*|\/\*[\s\S]+?(?=\*\/)\*\/", "", contract_code)
