import hashlib
import json
from time import time
from uuid import uuid4


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, month=1, proof=100) # genesis block

    # 새로운 블록구조(매달 장부)
    def new_block(self, proof, month, previous_hash=None):
        block = {
            'index':len(self.chain) + 1,
            'month':month, # 몇월달 장부인지
            'timestamp':time(),
            'transactions':self.current_transactions, # 거래내역들
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    # 새로운 거래(장부작성)
    def new_transaction(self, sender, recipient, des, amount, use_money_time):
        self.current_transactions.append({
            'sender':sender, # 보내는 사람
            'recipient':recipient, # 받는사람
            'des':des, # 거래 설명
            'amount':amount, # 돈의 양
            'use_money_time':use_money_time, # 장부기록시간
            'timestamp': time() # 장부 작성시간
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof * proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" # difficult y, 0000=nonce