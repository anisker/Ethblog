import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import json
from web3 import Web3


app = Flask(__name__)

app.config['SECRET_KEY'] = '0cff3580a0a8851257c37c7f2f439237'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'anisker96@gmail.com'
app.config['MAIL_PASSWORD'] = 'amelkakanissou20'
mail=Mail(app)

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
web3.eth.defaultAccount = web3.eth.accounts[0]
abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"postId","type":"uint256"},{"indexed":false,"internalType":"string","name":"title","type":"string"}],"name":"NewPost","type":"event"},{"constant":false,"inputs":[{"internalType":"string","name":"_username","type":"string"},{"internalType":"string","name":"_date","type":"string"},{"internalType":"string","name":"_title","type":"string"},{"internalType":"string","name":"_content","type":"string"}],"name":"createPost","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getNumberOfPosts","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"_postId","type":"uint256"}],"name":"getPost","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"ownerPostCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"postToOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"posts","outputs":[{"internalType":"string","name":"username","type":"string"},{"internalType":"string","name":"date","type":"string"},{"internalType":"string","name":"title","type":"string"},{"internalType":"string","name":"content","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"_postId","type":"uint256"},{"internalType":"string","name":"_title","type":"string"},{"internalType":"string","name":"_content","type":"string"}],"name":"setPost","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"usernamesPosts","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
address = web3.toChecksumAddress("0x2c89D41B78D29e32a53e2429D83C2dBFA5Fd95a9")
contract = web3.eth.contract(address= address, abi = abi)

from ethblog import routes