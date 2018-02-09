import hashlib
import json
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import requests
from datetime import datetime

class BlockChain(object):

    # 블록체인 생성자
    def __init__(self):
        self.chain = [] # 체인을 빈 리스트로 선언
        self.current_transactions = [] # 거래 목록 리스트로 선언
        self.new_block(previous_hash=1, month=datetime.today().month, proof=100) # genesis block, 초기 블록을 만든다.
        self.nodes = set() # nodes들 설정 (사용자)

    # 새로운 블록구조(매달 장부)
    def new_block(self, proof, month, previous_hash=None):
        block = {
            'index':len(self.chain) + 1,
            'month':month, # 몇월달 장부인지
            'timestamp':time(), # 언제 블록이 생성되었는가
            'transactions':self.current_transactions, # 거래내역들
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1]) # 이전의 해쉬값
        }
        self.current_transactions = [] # 현재 거래내역은 없음
        self.chain.append(block) # 체인에 블록 추가하기
        return block

    # 새로운 거래(장부작성)
    def new_transaction(self, use_user, use_description, use_money, use_date, write_date, write_user, use_option):
        self.current_transactions.append({
            'use_user':use_user, # 돈 사용한 사람
            'use_description':use_description, # 돈을 사용한 이유
            'use_money':use_money, # 사용한 돈의 양
            'use_date':use_date, # 돈 사용한 날짜
            'write_date':write_date, # 장부 기록 날짜
            'write_user': write_user, # 장부를 기록한 사람
            'use_option':use_option # 지출/수입/회비 0,1,2
        })
        return self.last_block['index'] + 1 # 마지막 블록 + 1 을 반환

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
        parsed_url = urlparse(address) # address를 urlparse로 전환
        self.nodes.add(parsed_url.netloc) # 노드들에 추가

    # 체인의 유효성 검사, 올바른 블록(매달 장부)인가 체크
    def valid_chain(self, chain):

        # 초기화
        last_block = chain[0] # 최근 블록은 가장 첫번째 블록으로 설정
        current_index = 1 # 현재 index는 1

        while current_index < len(chain): # 현재 인덱스에서, 체인의 크기가 될때까지
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n~~~~`\n')

            # check that he hash of the block is correct
            # 블록이 올바른 블록인가 체크
            # 현재 블럭이 가르치는 이전블럭의 hash값과 이전블럭의 hash값이 일치하는지 여부 확인
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