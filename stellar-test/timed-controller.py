from os import system
from time import sleep

while True: #manually terminate when you want to stop streaming
    system('python doget-user-script.py --public_key=GBCOBOTX7SWYWMEE5AZAOAEJ3O5CDE3P2EX7YXLR4AW64VXQUZQIUD3W --secret_key=SAG2ATQAU4ZPHM3QZISX5BFJPIEMWJ3HLTU2GJ3JR4XDOMXH7RMVZCAP --amount=22 --dogetcode=DOGET --assetissuerpublickey=GDOEVDDBU6OBWKL7VHDAOKD77UP4DKHQYKOKJJT5PR3WRDBTX35HUEUX --url=https://horizon.stellar.org')
    sleep(5) #sleep for 5 minutes
