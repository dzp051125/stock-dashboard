from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from market_data import get_paper_account
load_dotenv()
deepseek_api_key= os.getenv('DEEPSEEK_API_KEY')
app = FastAPI()
class NoteCreate(BaseModel):
    content: str
def generate_account_summary(accounts):
    if not deepseek_api_key:
        raise ValueError('deepseek_api_key is missing')
    client=OpenAI(
            api_key=deepseek_api_key,
            base_url='https://api.deepseek.com',
            timeout=30,
            max_retries=0
    )
    account_data= json.dumps(accounts)
    messages= [
        {'role':'system',
         'content': 'Summarize the supplied fictional account data in CHINESE.Use only provided facts. Mention the snapshot times and note if they differ'},
        {'role': 'user',
         'content': account_data}
    ]
    response= client.chat.completions.create(
        model='deepseek-flash',
        messages=messages,
        max_tokens=1000,
        extra_body={'thinking':{'type':'disabled'}}
    )
    return response.choices[0].message.content
def read_account(account_id):
    connection = sqlite3.connect('data/dashboard.db')
    try:
        query_result = connection.execute('SELECT account_id, account_type, name, base_currency,source FROM accounts WHERE account_id =?',
                                          (account_id,))
        row = query_result.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail='Account not found.')
        snapshot_query = connection.execute('SELECT snapshot_id, as_of, received_at, netvalue FROM snapshots WHERE account_id = ? ORDER BY as_of DESC LIMIT 1',
                                            (account_id,))
        snapshot_row = snapshot_query.fetchone()
        if not snapshot_row:
            raise HTTPException(status_code=404, detail='Account snapshot not found.')
        holding_query = connection.execute('SELECT snapshot_id, symbol, quantity FROM holdings WHERE snapshot_id =?',
                                           (snapshot_row[0],))
        holding_rows = holding_query.fetchall()
    finally:
        connection.close()
    records = {}
    records['as_of']= snapshot_row[1]
    records['account_id']= row[0]
    records['account_type']= row[1]
    records['name']= row[2]
    records['base_currency']= row[3]
    records['currency'] = records['base_currency']
    records['netvalue'] = snapshot_row[3]
    records['source']= row[4]
    records['received_at']= snapshot_row[2]
    records['holding']= []
    for holding_row in holding_rows:
        holding_record ={}
        holding_record['symbol'] = holding_row[1]
        holding_record['quantity'] = holding_row[2]
        records['holding'].append(holding_record)
    return records
@app.get('/accounts/{account_id}/snapshots')
def read_snapshots(account_id: str):
    connection = sqlite3.connect('data/dashboard.db')
    try:
        snapshot_query = connection.execute('SELECT account_id, as_of, netvalue, snapshot_id ,note FROM snapshots WHERE account_id = ? ORDER BY as_of ASC',
                                            (account_id,))
        rows = snapshot_query.fetchall()
    finally:
        connection.close()
    records = []
    for row in rows:
        record = {}
        record['account_id']= row[0]
        record["as_of"]= row[1]
        record['netvalue']= row[2]
        record['snapshot_id']= row[3]
        record['note']= row[4]
        records.append(record)
    return records
@app.get('/accounts')
def read_live_account():
    paper_account = read_account('demo_paper')
    live_account = read_account('demo_live')
    return [paper_account, live_account]
@app.post('/accounts/{account_id}/account-summary')
def create_account_summary(account_id:str):
    accounts= read_account(account_id)
    summary=generate_account_summary(accounts)
    return{'summary':summary
    }


@app.put('/accounts/{account_id}/snapshots/{snapshot_id}/note')
def updata_snapshot_note(account_id: str, snapshot_id: int, note: NoteCreate):
    content= note.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail='note cannot be empty')
    connection= sqlite3.connect('data/dashboard.db')
    try:
        update_result= connection.execute('UPDATE snapshots SET note = ? WHERE account_id = ? AND snapshot_id= ?',
                                          (content, account_id, snapshot_id))

        if update_result.rowcount== 0:
            raise HTTPException(status_code=404, detail='snapshot not found')
        connection.commit()
    finally:
        connection.close()
    return{'note': content}

@app.delete('/accounts/{account_id}/snapshots/{snapshot_id}/note')
def delete_snapshot_note(account_id: str, snapshot_id: int):
    connection = sqlite3.connect('data/dashboard.db')
    try:
        delete_result = connection.execute(
            'UPDATE snapshots SET note = NULL WHERE account_id = ? AND snapshot_id = ?',
            (account_id, snapshot_id)
        )
        if delete_result.rowcount == 0:
            raise HTTPException(status_code=404, detail='Snapshot not found')

        connection.commit()
    finally:
        connection.close()

    return {'note': None}

@app.get('/accounts/paper')
async def read_paper():
    return await get_paper_account()

