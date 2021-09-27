from fastapi import APIRouter
from fastapi import FastAPI

router = APIRouter()

@router.get("/accounts/", tags=["accounts"])
async def get_secrets():
    from stellar_sdk.keypair import Keypair

    pair = Keypair.random()
    print(f"Secret: {pair.secret}")
    secret = pair.secret
    # Secret: SCMDRX7A7OVRPAGXLUVRNIYTWBLCS54OV7UH2TF5URSG4B4JQMUADCYU
    print(f"Public Key: {pair.public_key}")
    public_key = pair.public_key
    # Public Key: GAG7SXULMNWCW6LX42JKZOZRA2JJXQT23LYY32OXA6XECUQG7RZTQJHO

    import requests
    response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
    if response.status_code == 200:
        print(f"SUCCESS! You have a new account :)\n{response.text}")
        status = "Success"
    else:
        print(f"ERROR! Response: \n{response.text}")
        status = "Error"

    message = response.text
    return {"secret": secret, "public_key": public_key, "message": message,
            "status": status}

@router.post("/accounts/")
def new():
    from stellar_sdk.keypair import Keypair

    pair = Keypair.random()
    print(f"Secret: {pair.secret}")
    secret = pair.secret
    # Secret: SCMDRX7A7OVRPAGXLUVRNIYTWBLCS54OV7UH2TF5URSG4B4JQMUADCYU
    print(f"Public Key: {pair.public_key}")
    public = pair.public
    # Public Key: GAG7SXULMNWCW6LX42JKZOZRA2JJXQT23LYY32OXA6XECUQG7RZTQJHO
    return {"secret": secret, "public": public}
