from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
def read_index():
    return FileResponse("index.html")


@app.get("/accounts/paper")
def read_paper_account():
    return{"account_type": "paper",
           "name": "paper_account",
           "netvalue": "15000.00",
           "currency": "usd",          
           "holding":[
            {"symbol": "TSM", "quantity": "2.5"}
           ]
           }
@app.get('/accounts')
def read_live_account():
    paper_account = read_paper_account()
    live_account={"account_type": "live",
           "name": "live_account",
           "netvalue": "14000.00",
           "currency": "usd",          
           "holding":[
            {"symbol": "GOOGL", "quantity": "3"}
           ]}
    return[paper_account, live_account]
