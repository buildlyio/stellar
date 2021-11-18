from stellar_sdk.xdr import TransactionResult
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
from stellar_sdk import (
    Network,
    Server,
    TransactionBuilder,
    Asset,
    Claimant,
    CreateClaimableBalance,
    ClaimPredicate,
)
import argparse
import requests
import time

"""
python doget-user-script.py --public_key=
                    --secret_key=
                    --amount=100
                    --dogetcode=DOGET
                    --assetissuerpublickey=GDOEVDDBU6OBWKL7VHDAOKD77UP4DKHQYKOKJJT5PR3WRDBTX35HUEUX-2
                    --url=https://horizon-testnet.stellar.org

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

# set counter to 0
i = 0

if args.dogetcode == "DOGET":
    file="accounts-doget.txt"
else:
    file="accounts.txt"

# 100 loops x 10 users = 1000 deposits
for i in range(0, 100):
    print("start of loop:")
    print(i)

    # get last account as cursor
    with open(file) as myfile:
        cursor = list(myfile)[-1]
        print(cursor)

    # filter the do-get users using API call
    # cursor needs to be set to last account in accounts.txt and pull 10 at a time

    response = requests.get(f"{args.url}/accounts/?asset={args.dogetcode}:{args.assetissuerpublickey}&cursor={cursor}&limit=10&order=asc")

    do_get_user_list = response.json()

    print(response.url)

    # get list of use account id
    do_get_user_accounts = []
    string1 = 'coding'

    # opening file
    file1 = open(file, "r")
    # read file content
    readfile = file1.read()
    # closing text file
    file1.close()
    # add counter to limit the number of claimants
    x=0
    for user in do_get_user_list['_embedded']['records']:
        account_check = str(user['account_id'])

        # LIMIT ACCOUNTS
        if x == 1:
            break
        # checking condition for string found or not
        if account_check in readfile:
            print('Account Already Used: ', user['account_id'] , 'Account Found')
        else:
            # write account to file
            file2 = open(file, "a")
            file2.write(account_check + "\n")
            file2.close()
            print("NEW user['account_id']: ", user['account_id'])
            do_get_user_accounts.append(user['account_id'])
            x=x+1


    print("verified accounts: ", len(do_get_user_accounts))

    # get a account to create claimable balance entry
    try:
        account = server.load_account(str(args.public_key))
    except NotFoundError:
        raise Exception(f"Failed to load {str(args.public_key)}")

    # can add multiple claimer to the newly created claimable balance
    claimants = []

    # Create a claimable balance with one conditions.
    soon = int(time.time() + 2592000)
    bCanClaim = ClaimPredicate.predicate_before_relative_time(2592000)
    aCanClaim = ClaimPredicate.predicate_not(
        ClaimPredicate.predicate_before_absolute_time(soon)
    )

    # add do-get user to claimants who going to claime the claimable balance
    for user_account in do_get_user_accounts:
        claimants.append(Claimant(destination=user_account, predicate = bCanClaim))

    # add parent account to reclaim balance after predicate time expires
    # claimants.append(Claimant(destination=args.public_key, predicate = aCanClaim))

    # create claimable balance entry with the list of claimants
    claimable_balance_entry = CreateClaimableBalance(
        asset=Asset('MEOW','GCZZK6B4MRHK2R4RRSS3ZYJZPFNQPO5Q47NHBESAOF2OCU3OJIZAMEOW'),
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
        # readFile = open("file")
        # lines = readFile.readlines()
        # readFile.close()
        # w = open(file,'w')
        # w.writelines([item for item in lines[:-9]])
        # w.close()
        # failed so break
        break


    # increment counter for while loop
    i = i + 1
