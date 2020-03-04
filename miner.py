import hashlib
import requests
from time import perf_counter
import time
import sys
import json
import random


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    # block_string = json.dumps(block, sort_keys=True)
    proof = random.random()
    while valid_proof(block, proof) is False:
        proof -= 1

    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # return True or False
    return guess_hash[:6] == "000000"


# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         node = sys.argv[1]
#     else:
node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

headers = {'Content-Type': 'application/json',
           'Authorization': 'Token 50f83144a74d87d4dbe9230f7714c1ceb54d55b0'}
coins_mined = 0
# Run forever until interrupted
while True:
    start_time = perf_counter()
    r = requests.get(url=node + "/last_proof", headers=headers)
    # Handle non-json response
    try:
        data2 = r.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
        break

    # TODO: Get the block from `data` and use it to look for a new proof
    print(data2)
    last_proof = data2.get('proof')
    # data2["proof"]
    # diff = data["difficulty"]
    new_proof = proof_of_work(last_proof)

    post_data = {"proof": new_proof}

    r = requests.post(url=node + "/mine", json=post_data, headers=headers)
    data3 = r.json()

    if data3.get('messages') == ['New Block Forged']:
        break

    print(data3)
    time.sleep(data3.get('cooldown'))
