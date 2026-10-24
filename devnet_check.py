#!/usr/bin/env python3
"""Minimal read-only Solana Devnet diagnostic using Python's standard library."""
import argparse
import json
import sys
from urllib import request, error

DEVNET_GENESIS = "EtWTRABZaYq6iMfeYKouRu166VU2xqa1wcaWoxPkrZBG"
DEVNET_RPC = "https://api.devnet.solana.com"


def parse_rpc_result(data, method):
    if not isinstance(data, dict):
        raise ValueError(f"{method} returned a non-object response")
    if "error" in data:
        raise ValueError(f"{method} returned an RPC error: {data['error']}")
    if "result" not in data:
        raise ValueError(f"{method} returned no result")
    return data["result"]


def rpc(method, params=None, rpc_url=DEVNET_RPC):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode("utf-8")
    req = request.Request(rpc_url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req, timeout=12) as response:
        payload = json.loads(response.read(64_000).decode("utf-8"))
    return parse_rpc_result(payload, method)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only Solana Devnet RPC checks. Never submits transactions.")
    parser.add_argument("--address", help="Optional PUBLIC Solana address whose balance to query")
    args = parser.parse_args(argv)
    if args.address:
        chars = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
        if not 32 <= len(args.address) <= 44 or set(args.address) - chars:
            parser.error("--address should be a public Solana base58 address (32–44 characters)")
    try:
        genesis = rpc("getGenesisHash")
        if genesis != DEVNET_GENESIS:
            print(f"FAIL: expected Devnet genesis {DEVNET_GENESIS}, got {genesis!r}", file=sys.stderr)
            return 2
        print("PASS: Solana Devnet genesis confirmed")
        print(f"Current slot: {rpc('getSlot', [{'commitment': 'confirmed'}])}")
        if args.address:
            bal = rpc("getBalance", [args.address, {"commitment": "confirmed"}])
            print(f"Balance for {args.address}: {bal['value'] / 1_000_000_000:.9f} Devnet SOL")
        print("Read-only checks complete; no keypairs or signatures used")
        return 0
    except (error.URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"RPC check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
