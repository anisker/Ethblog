# ETHBlog

ETHBlog is a developping social network that allows users to communicate and exchange contents ensuring the freedom of speech. It uses Ethereum blockain for stocking the contents.

# Installation 

ETHBlog requires [Python](https://www.python.org/downloads/) v3.4+ to run. To install the packages, you need to install the package management system [pip](https://pip.pypa.io/en/stable/installing/)

## Packages
ETHBlog is a project under development that its configuration is for a development environment. 
Execute the following commands to install the packages

```sh
$ pip install flask
$ pip install flask_sqlalchemy
$ pip install flask_bcrypt
$ pip install flask_login
$ pip install flask_mail
$ pip install flask_wtf
$ pip install wtforms
$ pip install itsdangerous
$ pip install datetime
$ pip install web3
```

# Smart contract compilation and deployment 
[Ganache](https://www.trufflesuite.com/ganache) is a tool that offers a personal Ethereum blockchain is used for testing smart contractsin a development environment.

The smart constract is in the file ETHBlog.sol. Compile and depoly it in the IDE [remix](https://remix.ethereum.org/). In the deployment section. choose "Web3 provider" as environment.
