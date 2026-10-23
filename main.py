from fastapi import FastAPI
from fastapi.responses import FileResponse
import sqlite3
app = FastAPI()


@app.get("/")
def read_index():
    return FileResponse("index.html")


@app.get("/accounts/paper")
def read_paper_account():
    return{"account_type": "paper",
           "account_id": "demo_paper",
           "base_currency": "usd",
           "source": "demo",
           "as_of": "2026-10-20T20:00:00+08:00",
           "received_at": "2026-10-20T20:01:00+08:00",
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
           "account_id": "demo_live",
           "base_currency": "usd",
           "source": "demo",
           "as_of": "2026-10-20T20:00:00+08:00",
           "received_at": "2026-10-20T20:01:00+08:00",
           "name": "live_account",
           "netvalue": "14000.00",
           "currency": "usd",          
           "holding":[
            {"symbol": "GOOGL", "quantity": "3"}
           ]}
    return[paper_account, live_account]
@app.get('/accounts/paper/snapshots')
def read_paper_snapshots():
    connection = sqlite3.connect('data/dashboard.db')
    query_result = connection.execute('SELECT account_id, as_of, netvalue FROM snapshots WHERE account_id=?',
    ('demo_paper',))
    rows = query_result.fetchall()
    print(rows)
    connection.close()
    records = []
    for row in rows:
        record = {"account_id" : row[0],'as_of' : row[1], 'netvalue' : row[2]}
        records.append(record)
    return records
