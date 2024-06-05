<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">BLOCKCHAIN</h1>
</p>
<p align="center">
    <em><code>► A basic blockchain based on bitcoin</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/neoff69/blockchain?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/neoff69/blockchain?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/neoff69/blockchain?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/neoff69/blockchain?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary><br>

-   [ Overview](#-overview)
-   [ Repository Structure](#-repository-structure)
-   [ Modules](#-modules)
</details>
<hr>

## Overview

<code>► </code>

---

## Repository Structure

```sh
└── blockchain/
    ├── Blockchain
    │   ├── Blockchain.py
    │   ├── __pycache__
    │   └── utxo_utils.py
    ├── Node
    │   ├── BlockchainNode.py
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── dataManager
    │   └── utils.py
    ├── __pycache__
    │   └── blockchain.cpython-311.pyc
    ├── block
    │   ├── Block.py
    │   └── __pycache__
    ├── mining
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── mining.py
    │   └── mining_test
    ├── tests
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── integration
    │   └── unit
    ├── transaction
    │   ├── CoinbaseTransaction.py
    │   ├── Transaction.py
    │   ├── TransactionData.py
    │   └── __pycache__
    ├── user
    │   ├── Wallet.py
    │   └── __pycache__

```

---

## Modules

<details closed><summary>transaction</summary>

| File                                                                                                           | Summary                                                                            |
| -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [Transaction.py](https://github.com/neoff69/blockchain/blob/master/transaction/Transaction.py)                 | <code>► The usual transaction that is made in the blockchain </code>               |
| [CoinbaseTransaction.py](https://github.com/neoff69/blockchain/blob/master/transaction/CoinbaseTransaction.py) | <code>►The first transaction of the block, that give a reward to the miner </code> |
| [TransactionData.py](https://github.com/neoff69/blockchain/blob/master/transaction/TransactionData.py)         | <code>► The data that the transaction need</code>                                  |

</details>

<details closed><summary>user</summary>

| File                                                                          | Summary                                                            |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [Wallet.py](https://github.com/neoff69/blockchain/blob/master/user/Wallet.py) | <code>► A basic wallet creation with public and private key</code> |

</details>

<details closed><summary>mining</summary>

| File                                                                            | Summary                                             |
| ------------------------------------------------------------------------------- | --------------------------------------------------- |
| [mining.py](https://github.com/neoff69/blockchain/blob/master/mining/mining.py) | <code>► The code to start the mining process</code> |

</details>

<details closed><summary>mining.mining_test</summary>

| File                                                                                                                          | Summary                                                                   |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [test_connection_network.py](https://github.com/neoff69/blockchain/blob/master/mining/mining_test/test_connection_network.py) | <code>► A basic test to check if the P2P network work in localhost</code> |

</details>

<details closed><summary>Blockchain</summary>

| File                                                                                        | Summary                         |
| ------------------------------------------------------------------------------------------- | ------------------------------- |
| [utxo_utils.py](https://github.com/neoff69/blockchain/blob/master/Blockchain/utxo_utils.py) | <code>► INSERT-TEXT-HERE</code> |
| [Blockchain.py](https://github.com/neoff69/blockchain/blob/master/Blockchain/Blockchain.py) | <code>► INSERT-TEXT-HERE</code> |

</details>
