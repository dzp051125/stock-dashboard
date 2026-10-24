from fastapi import FastAPI, HTTPException
import sqlite3
app = FastAPI()



def read_account(account_id):
    connection = sqlite3.connect('data/dashboard.db')
    try:
        query_result = connection.execute('SELECT account_id, account_type, name, base_currency,source FROM accounts WHERE account_id =?',
                                          (account_id,))
        rows = query_result.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail='Account not found.')
        snapshot_query = connection.execute('SELECT snapshot_id, as_of, received_at, netvalue FROM snapshots WHERE account_id = ? ORDER BY as_of DESC LIMIT 1',
                                            (account_id,))
        snapshot_rows = snapshot_query.fetchall()
        if not snapshot_rows:
            raise HTTPException(status_code=404, detail='Account snapshot not found.')
        snapshot_row = snapshot_rows[0]
        holding_query = connection.execute('SELECT snapshot_id, symbol, quantity FROM holdings WHERE snapshot_id =?',
                                           (snapshot_row[0],))
        holding_rows = holding_query.fetchall()
    finally:
        connection.close()
    row = rows[0]
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
@app.get('/accounts')
def read_live_account():
    paper_account = read_account('demo_paper')
    live_account = read_account('demo_live')
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
