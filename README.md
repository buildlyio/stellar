##Getting Started

Install VirtualEnv
pip3 install virtualenv

### start a new virtual env in folder
python3 -m virtualenv venv

### activate envrionment
source venv/bin/activate

### install requirements
pip3 install -f requirements.txt

## Start the Server
uvicorn main:app --reload

### Local Server API Docs URL
http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc
