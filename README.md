# ETHBlog

ETHBlog is a social network under development that allows users to communicate and exchange contents ensuring the freedom of speech. It uses Ethereum blockain for stocking the contents.

# Installation 

ETHBlog requires [Python](https://www.python.org/downloads/) v3.6+ to run. To install the packages, you need to install the package management system [pip](https://pip.pypa.io/en/stable/installing/)

## Packages
ETHBlog is a project under development that its configuration is for a development environment. 
Execute the following commands to install the packages

### flask

Lightweight WSGI web application framework
```sh
$ pip install flask
```
### flask SQLAlchemy

An Object-relational mapping (ORM) extension of Flask.
```sh
$ pip install flask_sqlalchemy
```
### flask bcrypt

Provides bcrypt hashing utilities for the application
```sh
$ pip install flask_bcrypt
```
### flask login

Provides user session management for Flask
```sh
$ pip install flask_login
```
### flask mail

Provides functions to send emails to users
```sh
$ pip install flask_mail
```
### flask wtf

Provides an interactive user interface for users
```sh
$ pip install flask_wtf
```
### wtforms

A tool to help with form validation.
```sh
$ pip install wtforms
```
### itsdangerous

Various helpers to pass data to untrusted environments and to get it back safe and sound. Data is cryptographically signed to ensure that a token has not been tampered with.
```sh
$ pip install itsdangerous
```
### datetime

Supplies classes for manipulating dates and times.
```sh
$ pip install datetime
```
### web3

A Python library for interacting with Ethereum.
```sh
$ pip install web3
```

# Smart contract compilation and deployment 
[Ganache](https://www.trufflesuite.com/ganache) is a tool that offers a personal Ethereum blockchain used for testing smart contractsin a development environment.

The smart constract is in the file ETHBlog.sol. Compile and depoly it in the IDE [remix](https://remix.ethereum.org/). Under the deployment section. choose "Web3 provider" as environment. After the deployement, put the smart contract's address in the file '__init__.py' in this line :
```sh
address = web3.toChecksumAddress("address here")
```
