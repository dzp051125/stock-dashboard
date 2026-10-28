from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from datetime import datetime,timezone
app = FastAPI()
class NoteCreate(BaseModel):
    content: str



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

@app.post('/accounts/{account_id}/notes')
def create_notes(account_id: str,note: NoteCreate):
    content= note.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail= 'note cannot be empty')
    current_time = datetime.now(timezone.utc)
    create_at= current_time.isoformat()
    connection = sqlite3.connect('data/dashboard.db')
    try:
        connection.execute('PRAGMA foreign_keys= ON')
        account_query= connection.execute('SELECT account_id FROM accounts WHERE account_id= ?',
                                          (account_id,))
        account_row= account_query.fetchone()
        if account_row is None:
            raise HTTPException(status_code=404,detail='account cannot found')
        insert_result= connection.execute(
        "INSERT INTO notes(account_id, content, created_at) VALUES(?, ?, ?)",
        (account_id,content,create_at)
    )
        connection.commit()
        note_id = insert_result.lastrowid
    finally: connection.close()
    return note_id

@app.get('/accounts/{account_id}/notes')
def read_notes(account_id: str):
    connection= sqlite3.connect('data/dashboard.db')
    try:
        note_query= connection.execute('SELECT account_id, content, created_at, id FROM notes WHERE account_id= ? ORDER BY created_at DESC',
                                   (account_id,))
        note_rows= note_query.fetchall()
    finally:
        connection.close()
    records= []
    for note_row in note_rows:
        record= {}
        record['account_id']= note_row[0]
        record['content']= note_row[1]
        record['created_at']= note_row[2]
        record['id']= note_row[3]
        records.append(record)
    return records
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

def save_snapshot(snapshot, holdings):
    connection= sqlite3.connect('data/dashboard.db')
    try:
        connection.execute('PRAGMA foreign_keys= ON')
        snapshot_query= connection.execute('SELECT snapshot_id, netvalue FROM snapshots WHERE account_id= ? and as_of=?',
                                           (snapshot['account_id'], snapshot['as_of']))
        snapshot_row= snapshot_query.fetchone()
        if snapshot_row is not None:
            if snapshot_row[1] != snapshot['netvalue']:
                raise ValueError('snapshot netvalue conflicts with existing data')
            holding_query= connection.execute('SELECT symbol, quantity FROM holdings WHERE snapshot_id= ?',
                                              (snapshot_row[0],))
            holding_rows= holding_query.fetchall()
            existing_holdings= []
            for holding_row in holding_rows:
                existing_holdings.append({'symbol': holding_row[0],
                                          'quantity': holding_row[1]})

            if sorted(existing_holdings, key= lambda item:item['symbol']) != sorted( holdings, key= lambda item:item['symbol']):
                raise ValueError('holdings conflicts with existing data')
            return {'snapshot_id': snapshot_row[0],
                    'status': 'existing'}


        
        save_query= connection.execute('INSERT INTO snapshots(account_id, as_of, received_at, netvalue)' \
        'VALUES(?,?,?,?)',
        (snapshot['account_id'], snapshot['as_of'], snapshot['received_at'], snapshot['netvalue']))
        snapshot_id= save_query.lastrowid
        for holding in holdings:
            connection.execute('INSERT INTO holdings(snapshot_id, symbol, quantity)VALUES(?,?,?)',
                               (snapshot_id, holding['symbol'], holding['quantity']))
        connection.commit()
            
    finally:
        connection.close()
    return {'snapshot_id': snapshot_id,
            'status': 'added success'}

