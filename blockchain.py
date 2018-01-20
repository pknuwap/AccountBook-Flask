import hashlib
import json
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import requests


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, month=1, proof=100) # genesis block
        self.nodes = set()

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

    # 새로운 사용자(노드) 등록
    def register_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # 체인의 유효성 검사, 올바른 블록(매달 장부)인가 체크
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n~~~~`\n')

            # check that he hash of the block is correct
            # 블록이 올바른 블록인가 체크
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    # 다른 노드(사용자)들을 검사해 길이가 가장 긴 체인으로 교체
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get('http://{%s}/chain'%(node))
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        return False



    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof * proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" # difficult y, 0000=nonce