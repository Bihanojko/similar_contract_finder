# Similar contracts finder

A smart contract similarity tool that returns the top 5 similar contracts for a given smart contract solidity file.

## Installation

1. Install Git LFS (Large File System) if not already installed
 - Check if already installed
    ```$ git lfs install```
 - In case of the following response, Git LFS has already been installed, move to step 2
    ```
    $ git lfs install
    > Git LFS initialized.
    ```
- Otherwise install Git LFS as described in this guide: https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage
2. Navigate to a folder where you want to clone the solution to
    ```$ mkdir {NEW_FOLDER_PATH} && cd {NEW_FOLDER_PATH}```
3. Clone the git repository
    ```$ git clone https://github.com/Bihanojko/similar_contract_finder.git```
4. Navigate to the cloned repository
    ```$ cd similar_contract_finder/```
5. Pull the prepared docker image
    ```$ docker pull bihanojko/similar-contract-finder```
6. Run the docker image
    ```$ docker run -p 4500:5000 -d bihanojko/similar-contract-finder```

## Usage

A. To test the model via the API and apply the model on a randomly selected contract, execute the following command:
    ```$ python test_api.py```
To test the model via the API on a specific contract, use this command:
    ```$ python test_api.py {PATH_TO_CONTRACT}```

B. To test the model outside of the API, the sentence transformers module needs to be installed
    ```$ pip install sentence-transformers```
Then execute the following command for a random input contract selection:
    ```$ python test_model.py```
or the following command to apply the model on a selected contract
    ```$ python test_model.py {PATH_TO_CONTRACT}```

C. Alternatively, copy-paste the following code to your Python script, fill in the wanted path to contract and execute the script.

```
import requests

contract_filepath = {PATH_TO_CONTRACT}
 
url = "http://localhost:4500/find_similar_contracts"

with open(contract_filepath) as cf:
    event_data = {"contract_code": cf.read()}
    r = requests.post(url, json=event_data)
    print(r.json())
```
