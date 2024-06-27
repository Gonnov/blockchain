<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">BLOCKCHAIN</h1>
</p>
<p align="center">
    <em>Securing the future, one block at a time.</em>
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
-   [ Getting Started](#-getting-started)
    -   [ Installation](#-installation)
    -   [ Usage](#-usage)
    -   [ Tests](#-tests)
-   [ Project Roadmap](#-project-roadmap)
-   [ Contributing](#-contributing)

</details>
<hr>

## Overview

The BlockchainX project implements a decentralized blockchain network with core functionalities encompassing secure transaction handling, mining operations, and blockchain integrity maintenance. Transaction classes ensure data integrity using hashing and signatures, while UTXO ledger management ensures accurate balance updates. Nodes manage peer connections, mempool transactions, and blockchain synchronization, enhancing network efficiency. Wallet generation and mining processes further strengthen blockchain security. This project's value lies in its robust architecture that facilitates secure, efficient, and decentralized transactions within a trustless network.

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
    ├── README.md
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
    └── user
        ├── Wallet.py
        └── __pycache__
```

---

## Modules

<details closed><summary>transaction</summary>

| File                                                                                                           | Summary                                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Transaction.py](https://github.com/neoff69/blockchain/blob/master/transaction/Transaction.py)                 | Implements transaction classes ensuring secure data transfer with hashes and signatures. Validates transaction integrity based on size, key matches, and signature verification. Maintains transaction timestamp and ID.                   |
| [CoinbaseTransaction.py](https://github.com/neoff69/blockchain/blob/master/transaction/CoinbaseTransaction.py) | Defines and validates a coinbase transactions output, ensuring transaction integrity within the blockchain network by serializing and checking transaction validity against predefined rules and size limits.                              |
| [TransactionData.py](https://github.com/neoff69/blockchain/blob/master/transaction/TransactionData.py)         | Defines and serializes transaction data including sender and receiver public keys, amount, timestamp, and a unique identifier. An essential component within the blockchain architecture for handling transaction information efficiently. |

</details>

<details closed><summary>user</summary>

| File                                                                          | Summary                                                                                                                                                                           |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Wallet.py](https://github.com/neoff69/blockchain/blob/master/user/Wallet.py) | Generates wallet address through ECC-Signs transaction data with private key-Handles key pair generation-Essential for secure transaction signing in the blockchain architecture. |

</details>

<details closed><summary>mining</summary>

| File                                                                            | Summary                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [mining.py](https://github.com/neoff69/blockchain/blob/master/mining/mining.py) | Initiate blockchain server, connect to gateway node, prompt for miners public key generation or input, then commence mining process with validated blocks sent to all network nodes before stopping server. |

</details>

<details closed><summary>mining.mining_test</summary>

| File                                                                                                                          | Summary                                                                                                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [test_connection_network.py](https://github.com/neoff69/blockchain/blob/master/mining/mining_test/test_connection_network.py) | Simulates network connections and interactions between blockchain nodes. Establishes communication with a gateway node, shares blocks, and prints chain details. Emulates start and stop operations to test network functionality. |

</details>

<details closed><summary>Blockchain</summary>

| File                                                                                        | Summary                                                                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [utxo_utils.py](https://github.com/neoff69/blockchain/blob/master/Blockchain/utxo_utils.py) | Handles ledger management by updating receiver and sender balances based on transactions in a blockchain system. Ensures transaction validity before ledger updates.                                                                                                   |
| [Blockchain.py](https://github.com/neoff69/blockchain/blob/master/Blockchain/Blockchain.py) | Manages blockchain integrity through mining, validation, and UTXO set construction. Verifies blocks, transactions, tree consistency, and inclusion, upholding blockchain integrity and security. Key methods include mining, validation checks, and UTXO set creation. |

</details>

<details closed><summary>Node</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                                                                 |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [BlockchainNode.py](https://github.com/neoff69/blockchain/blob/master/Node/BlockchainNode.py) | Defines a BlockchainNode in the network, managing peers, mempool, and blockchain. It handles node connections, messages, transactions, and data exchanges. Incorporates key functionalities like connecting to nodes, adding transactions to mempool, and managing node disconnections. |
| [utils.py](https://github.com/neoff69/blockchain/blob/master/Node/utils.py)                   | Implements peer removal logic for the Node component, enabling the removal of a specific peer from the list by matching its address and port.                                                                                                                                           |

</details>

<details closed><summary>Node.dataManager</summary>

| File                                                                                                          | Summary                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [manageMempool.py](https://github.com/neoff69/blockchain/blob/master/Node/dataManager/manageMempool.py)       | Manages mempool transactions for validation and storage, enhancing node functionality within the blockchain architecture.                                                       |
| [manageNewBlock.py](https://github.com/neoff69/blockchain/blob/master/Node/dataManager/manageNewBlock.py)     | Manages addition of new blocks to the blockchain chain, ensuring integrity and syncing with peers. Automatically adds valid blocks from peers and updates the local blockchain. |
| [managePeers.py](https://github.com/neoff69/blockchain/blob/master/Node/dataManager/managePeers.py)           | Manages peer connections by connecting and adding new peers to the network.                                                                                                     |
| [manageBlockchain.py](https://github.com/neoff69/blockchain/blob/master/Node/dataManager/manageBlockchain.py) | Manages blockchain synchronization by updating with a valid chain, removing confirmed transactions from the mempool.                                                            |

</details>

<details closed><summary>block</summary>

| File                                                                         | Summary                                                                                                                                                                    |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Block.py](https://github.com/neoff69/blockchain/blob/master/block/Block.py) | Defines and manages the properties and methods of a blockchain block, facilitating hashing, mining, and verification. Required for the blockchains integrity and security. |

</details>

---

## Getting Started

**System Requirements:**

-   **Python**: `version x.y.z`

### Installation

<h4>From <code>source</code></h4>

> 1. Clone the blockchain repository:
>
> ```console
> $ git clone https://github.com/neoff69/blockchain
> ```
>
> 2. Change to the project directory:
>
> ```console
> $ cd blockchain
> ```

### Usage

<h4>From <code>source</code></h4>

> 1. Use the virtual environment:
>
> ```console
> $ source venv/bin/activate
> ```
>
> 2. Start mining::
>
> ```console
> $ python -m mining.mining
> ```

### Tests

> Run the test suite using the command below:
>
> ```console
> $ python -m unittest discover -s tests -p 'test_*.py'
> ```

---

## Project Roadmap

-   [ ] `► Add multi threading for new block detection`
-   [ ] `► Fix the merkle tree for verification`
-   [ ] `► Add a graphic interface`

---

## Contributing

Contributions are welcome! Here are several ways you can contribute:

-   **[Report Issues](https://github.com/neoff69/blockchain/issues)**: Submit bugs found or log feature requests for the `blockchain` project.
-   **[Submit Pull Requests](https://github.com/neoff69/blockchain/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
-   **[Join the Discussions](https://github.com/neoff69/blockchain/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
    ```sh
    git clone https://github.com/neoff69/blockchain
    ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
    ```sh
    git checkout -b new-feature-x
    ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
    ```sh
    git commit -m 'Implemented new feature x.'
    ```
6. **Push to github**: Push the changes to your forked repository.
    ```sh
    git push origin new-feature-x
    ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
 </details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/neoff69/blockchain/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=neoff69/blockchain">
   </a>
</p>
</details>

---
