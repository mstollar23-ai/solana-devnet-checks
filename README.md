# Solana Devnet Checks

A small, independent **read-only** Python utility to verify that an RPC connection points to Solana Devnet, read its current confirmed slot and optionally inspect the balance of a **public wallet address**.

Useful for Solana developers preparing controlled token-mint tests. This project does not mint tokens, submit transactions, handle wallets, request airdrops, or store credentials.

## Requirements

Python 3.10+; only the Python standard library is used.

## Usage

```bash
python3 devnet_check.py
python3 devnet_check.py --address 11111111111111111111111111111111
```

The script checks Devnet's expected genesis hash **before** requesting an address balance. It only sends JSON-RPC `getGenesisHash`, `getSlot`, and `getBalance` calls to `https://api.devnet.solana.com`.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Security and privacy

- No secret keys, mnemonic phrases, or private RPC URLs are required.
- Never paste private keys into GitHub or public issues.
- This repository is independent of any private application code.
- This repo does **not** guarantee access to third-party Devnet faucets. Faucet services independently assess account eligibility and rate limits.
- Read-only code; no financial transactions.

## Devnet test SOL

See the [official Solana developer guide](https://solana.com/developers/cookbook/development/airdrops-and-faucets) for supported Devnet faucet options. Devnet SOL has no monetary value.
