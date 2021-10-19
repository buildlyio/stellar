from os import system
from time import sleep
import argparse

# add parser to add argument to the script
my_parser = argparse.ArgumentParser()
my_parser.add_argument('--public_key', action='store', type=str, required=True, help='account public_key who will create claimable balance')
my_parser.add_argument('--secret_key', action='store', type=str, required=True, help='account secret_key who will create claimable balance')
my_parser.add_argument('--amount', action='store', type=int, required=True, help='claimable balance amount')
my_parser.add_argument('--dogetcode', action='store', type=str, required=True,  help='do get user asset code ex. DOGET')
my_parser.add_argument('--assetissuerpublickey', action='store', type=str, required=True, help='who has issued asset to the user')
my_parser.add_argument('--url', action='store', type=str, required=True, help='server URL')
args = my_parser.parse_args()

while True: #manually terminate when you want to stop streaming
    system('python doget-user-script.py --public_key=' + args.public_key + ' --secret_key=' + args.secret_key + ' --amount=22 --dogetcode=' + args.dogetcode + ' --assetissuerpublickey=' + args.assetissuerpublickey + ' --url=' + args.url)
    sleep(5) #sleep for 5 seconds
