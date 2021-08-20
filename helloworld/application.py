#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun
import requests
import boto3
from flask_cors import CORS
from datetime import datetime
import simplejson as json

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    

@application.route('/get_books', methods=['GET'])
def get_id():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('books')
    # replace table scan ###
    resp = table.scan()
    print(str(resp))
    return Response(json.dumps(resp['Items']), mimetype='application/json', status=200)
    
    
@application.route('/set_book', methods=['GET'])
def set_doc():
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('books')
    cid = request.args.get('id')
    title = request.args.get('title')
    author = request.args.get('author')
    item={
    'id': cid,
    'title': title,
    'author': author,
     }
    table.put_item(Item=item)
    
    return Response(json.dumps(item), mimetype='application/json', status=200)
    
@application.route('/del_book' , methods=['GET'])

def del_doc():
    id=request.args.get('id')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('books')
    
    resp = table.delete_item(
        Key={
            'id':id
        }
        )
    print (str(resp))
    return Response(json.dumps(resp), mimetype='application/json', status=200)

if __name__ == '__main__':
    flaskrun(application)
