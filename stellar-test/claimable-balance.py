import time
import argparse
from stellar_sdk.xdr import TransactionResult, OperationType
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
from stellar_sdk import (Keypair, Network, Server, TransactionBuilder, Transaction, Asset,
                         Operation, Claimant, ClaimPredicate, CreateClaimableBalance, ClaimClaimableBalance
                         )

# command to test the script
# python3 script.py --public_key=GB7YHRL25LI66F6VYVRHGXZ3HPYEEKDMKY5JKLCOYZSXFZIB5Y6BXBAQ
# 		     --secret_key=SBLZMMOSJUJQ4RAMA3Y46EZPKAD5D44I65E7FDSQENYVFYIZEWDI3VHH
# 		     --amount=100
# 		     --destination=GB7YHRL25LI66F6VYVRHGXZ3HPYEEKDMKY5JKLCOYZSXFZIB5Y6BXBAQ


# add parser to add argument to the script
my_parser = argparse.ArgumentParser()
my_parser.add_argument('--public_key', action='store', type=str, required=True, help='account public_key who will create claimable balance')
my_parser.add_argument('--secret_key', action='store', type=str, required=True, help='account secret_key who will create claimable balance')
my_parser.add_argument('--amount', action='store', type=int, required=True, help='claimable balance amount')
my_parser.add_argument('--destination', action='store', type=str, required=True, help='public_key of the account who will claim that claimable balance')
args = my_parser.parse_args()

# script to create claimable balance
# server url
server = Server("https://horizon-testnet.stellar.org")

# get a account to create claimable balance entry
try:
    account = server.load_account(str(args.public_key))
except NotFoundError:
    raise Exception(f"Failed to load {str(args.public_key)}")

# Create the operation and submit it in a transaction.
# here pass amount and Claimant destination i.e who will claim that claimable balance
claimable_balance_entry = CreateClaimableBalance(
    asset=Asset.native(),
    amount=str(args.amount),
    claimants=[
        Claimant(destination=str(args.public_key)),
    ]
)

tx = (
    TransactionBuilder(
        source_account=account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=server.fetch_base_fee()
    )
        .append_operation(claimable_balance_entry)
        .set_timeout(180)
        .build()
)

tx.sign(str(args.secret_key))

try:
    tx_response = server.submit_transaction(tx)
    print("Claimable balance created!")

    """Get balance id"""
    # get created claimable balance id to claim the claimable balance
    tx_result = TransactionResult.from_xdr(tx_response["result_xdr"])
    results = tx_result.result.results

    # We look at the first result since our first (and only) operation
    operation_result = results[0].tr.create_claimable_balance_result
    balance_id = operation_result.balance_id.to_xdr_bytes().hex()
    print(f"Balance ID (2): {balance_id}")

except (BadRequestError, BadResponseError) as err:
    print(f"Tx submission failed: {err}")