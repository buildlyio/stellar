from stellar_sdk.xdr import TransactionResult
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
from stellar_sdk import (
    Network,
    Server,
    TransactionBuilder,
    Asset,
    Claimant,
    CreateClaimableBalance,
)
import argparse
import requests

"""
python doget-user-script.py --public_key=GB7YHRL25LI66F6VYVRHGXZ3HPYEEKDMKY5JKLCOYZSXFZIB5Y6BXBAQ
                    --secret_key=SBLZMMOSJUJQ4RAMA3Y46EZPKAD5D44I65E7FDSQENYVFYIZEWDI3VHH
                    --amount=100
                    --dogetcode=DoGet
                    --assetissuerpublickey=GB7YHRL25LI66F6VYVRHGXZ3HPYEEKDMKY5JKLCOYZSXFZIB5Y6BXBAQ
                    --url=https://horizon-testnet.stellar.org

"""

"""
--public_key=GC5PRFNWGGWTKVH5DLIO3QL5DV4FPBFAE26Q77BPSXCPQQWGJQVHSW7U
--secret_key=SCK3HVVRT5UWEO3LSTGGR4GNZ22CRGLNEH62OM3FBGZHTAVWSSK2CK2W
"""


# add parser to add argument to the script
my_parser = argparse.ArgumentParser()
my_parser.add_argument('--public_key', action='store', type=str, required=True, help='account public_key who will create claimable balance')
my_parser.add_argument('--secret_key', action='store', type=str, required=True, help='account secret_key who will create claimable balance')
my_parser.add_argument('--amount', action='store', type=int, required=True, help='claimable balance amount')
my_parser.add_argument('--dogetcode', action='store', type=str, required=True,  help='do get user asset code ex. DOGET')
my_parser.add_argument('--assetissuerpublickey', action='store', type=str, required=True, help='who has issued asset to the user')
my_parser.add_argument('--url', action='store', type=str, required=True, help='server URL')
args = my_parser.parse_args()


# server url
# https://horizon-testnet.stellar.org
server = Server(f"{args.url}")

# filter the do-get users using API call
response = requests.get(f"{args.url}/accounts/?asset={args.dogetcode}:{args.assetissuerpublickey}")
do_get_user_list = response.json()

print("do_get_user_list", do_get_user_list)

# get list of use account id
do_get_user_accounts = []
for user in do_get_user_list['_embedded']['records']:
    print("user['account_id']: ", user['account_id'])
    do_get_user_accounts.append(user['account_id'])


# get a account to create claimable balance entry
try:
    account = server.load_account(str(args.public_key))
except NotFoundError:
    raise Exception(f"Failed to load {str(args.public_key)}")

# can add multiple claimer to the newly created claimable balance
claimants = []

# add do-get user to claimants who going to claime the claimable balance
for user_account in do_get_user_accounts:
    claimants.append(Claimant(destination=user_account))

# create claimable balance entry with the list of claimants
claimable_balance_entry = CreateClaimableBalance(
    asset=Asset('MEOW','GCZZK6B4MRHK2R4RRSS3ZYJZPFNQPO5Q47NHBESAOF2OCU3OJIZAMEOW')
    amount=str(args.amount),
    claimants=claimants
)
print("Claimants: ", claimants)
tx = (
    TransactionBuilder(
        source_account=account,
        network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
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

    # Get claimable balances
    response = requests.get(f"{args.url}/claimable_balances/{balance_id}")
    claimable_balance = response.json()
    print('claimants', claimable_balance['claimants'])

except (BadRequestError, BadResponseError) as err:
    print(f"Tx submission failed: {err}")
