from flask import Flask, render_template, jsonify, request, redirect

from uuid import uuid4
from blockchain import BlockChain
from datetime import datetime
import setObject
from flask_recaptcha import ReCaptcha
import os

app = Flask(__name__)
# ReCaptcha 설정
app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = setObject.recaptcha_site_key,
    RECAPTCHA_SECRET_KEY = setObject.recaptcha_secret_key
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)


node_identifier = str(uuid4()).replace('-', '')

blockchain = BlockChain() # object create

# 새로운 블록 생성, 매달 생성해줘야함!
@app.route('/mine', methods=['GET'])
def mine():

    month = datetime.today().month # 현재 달
    last_block = blockchain.last_block # 맨 마지막 블럭
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # blockchain.new_transaction(
    #     sender = '0',
    #     recipient = node_identifier,
    #     des= str(datetime.today().month) + " block",
    #     use_money_time=datetime.today().month,
    #     amount = 1,use_option=1
    # )

    previous_hash = blockchain.hash(last_block)

    # 새로운 블럭 생성
    block = blockchain.new_block(proof, month, previous_hash)

    response = {
        'message':str(block['month']) + "장부가 만들어졌습니다",
        'index':block['index'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash'],
        'month': block['month'],  # 몇월달 장부인지
    }
    return jsonify(response), 200


# 새로운 거래내역 추가 창
@app.route('/transactions/make', methods=['GET'])
def make_transactions():
    return render_template('block_make_transaction.html')


# make new transaction
@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    # values = request.get_json()
    values = request.form

    required = ['use_name','use_option','use_money','use_date', 'use_d']
    write_date = int(datetime.today().strftime("%Y%m%d")) # 장부작성일
    write_user = os.uname()[1] # 장부를 작성한자의 컴퓨터 이름

    # POST 값이 제대로 다 주어졌는가 확인
    if not all(k in values for k in required):
        return "Missing values", 400

    index = blockchain.new_transaction(values['use_name'], values['use_d'], values['use_money'],
                                       values['use_date'],write_date, write_user, values['use_option'])

    response = {'message': 'Transaction will be added to Block {0}'.format(index)}

    return jsonify(response), 201


# 체인정보 보기

@app.route("/chain", methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200


# 새로운 노드(사용자) 추가
@app.route('/node/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message':'New nodes have been added',
        'total_nodes':list(blockchain.nodes)
    }
    return jsonify(response), 201

# 네트워크에 존재하는 모든 노드들의 체인을 똑같이 유지시킴
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message':'Our chain was replaced',
            'new_chain':blockchain.chain
        }
    else:
        response = {
            'message':'Our chain is authoritative',
            'chain':blockchain.chain
        }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run()
