from flask import Flask, render_template, jsonify, request
import json
from textwrap import dedent
from uuid import uuid4
from blockchain import BlockChain
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def home_intro():
    return render_template('intro.html', name="home_intro")

@app.route('/current')
def current():
    return render_template('current.html', name="current")

@app.route('/home')
def home_main():
    return render_template('home.html', name="home_main")

@app.route('/stat')
def stat():
    return render_template('stat.html', name="stat")

@app.route('/join')
def join():
    return render_template('join.html', name="join")

node_identifier = str(uuid4()).replace('-', '')

blockchain = BlockChain() # object create

# 새로운 블록 생성, 매달 생성해줘야함!
@app.route('/mine', methods=['GET'])
def mine():
    month = datetime.today().month
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender = '0',
        recipient = node_identifier,
        des= str(datetime.today().month) + " block",
        use_money_time=datetime.today().month,
        amount = 1
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, month, previous_hash)

    response = {
        'message':str(block['month']) + "장부가 만들어졌습니다",
        'index':block['index'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash'],
        'month': block['month'],  # 몇월달 장부인지
    }
    return jsonify(response), 200


# make new transaction
@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    values = request.get_json()

    required = ['sender','recipient','des','amount', 'use_money_time']

    if not all(k in values for k in required):
        return "Missing values", 400

    index = blockchain.new_transaction(values['sender'], values['recipient'],values['des'],values['amount'],values['use_money_time'])

    response = {'message': 'Transaction will be added to Block {0}'.format(index)}

    return jsonify(response), 201


@app.route("/chain", methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
