# Request Flow

## Current implementation: 2026-10-26

- Entry: frontend/index.html -> frontend/src/main.js -> App.vue, served at 5173. Backend 8001 provides JSON; the old root HTML and FileResponse homepage have been removed.
- Main request: mounted/button -> load_accounts -> fetch('/accounts') -> Vite proxy -> FastAPI read_live_account -> read_account for demo_paper/demo_live -> SQLite accounts/latest snapshots/all holdings -> dictionaries -> JSON array.
- Reply: response.json -> account_type-based assignment -> paper_account/live_account -> computed.current_account -> one set of DashboardHeader/AccountSummary/HoldingsList. Initial objects are null and guarded; no duplicate frontend asset fixtures or rename demo remain.
- Metadata: AccountSummary receives account and displays source/as_of/received_at from the reply. as_of describes the snapshot, received_at the stored receipt time; neither is a live broker update or page refresh time.
- History backend: /accounts/{account_id}/snapshots -> read_snapshots(account_id) -> parameterized snapshots query ordered by as_of ASC -> one new dictionary per row -> JSON list. Actual demo_paper/demo_live responses have two/one records; no match currently returns[].
- History frontend: AccountHistory.vue has not yet been created. The planned component receives account, requests its history, manages snapshots/history_message and displays records; App.vue integration and switching/late-response handling remain pending.
- These are teacher-maintained notes. Learner/teacher contributions and verification boundaries are recorded in learning/STATUS.md and daily logs.

## Historical notes below: superseded implementations

The following preserves earlier stage records only. They do not describe the current application.


> 2026-10-21 教师整理：这是代码对照笔记，不是学生独立解释的证据，也不参与程序运行。

## Historical stage 3.5: request and component flow

- Current page: http://127.0.0.1:5173/, served by the Vite development server.
- Entry: frontend/index.html -> frontend/src/main.js -> frontend/src/App.vue.
- Initial data: App.vue的data()返回两个内置演示账户和select_account。点击加载后才请求Python；没有数据库或券商连接。
- Request: App.vue button -> load_accounts() -> fetch('/accounts') -> Vite :5173 proxy -> FastAPI :8001/accounts -> main.py read_live_account() -> two account dictionaries -> JSON array.
- Reply: response.ok checks HTTP success; response.json() returns accounts; length 0/1 is rejected with a notice and return; positions 0/1 update paper_account/live_account. Current contract is exactly the two known demo accounts in that order, not a general broker payload validator.
- State: before waiting, status_message becomes loading; success updates both accounts then the success message. HTTP failure returns early without reading JSON; network/JSON exceptions enter catch. Empty/incomplete replies and failures preserve prior account objects.
- Selection: AccountSelector button -> $emit('select-paper' / 'select-live') -> App.vue @ listener -> select_account -> v-if shows the matching account group.
- Header: matching account.name -> DashboardHeader heading prop -> h1.
- Overview: matching account object -> AccountSummary account prop -> three p elements.
- Rename: AccountSummary button -> $emit('rename') -> matching App.vue listener changes that account.name -> header and overview update.
- Holdings: matching account.holding array -> HoldingsList positions prop -> v-for takes one position object per li -> position.symbol / position.quantity.
- Status: App.vue status_message -> StatusMessage message prop -> p. This component is outside both account conditions, so the demo notice stays visible for either account.
- Metadata material: account_id is a fictional stable ID, account_type is paper/live, source is demo, as_of is the fictional snapshot time, received_at is the fictional receipt time, and base_currency is usd. These are teacher-prepared fixtures, now present in both initial frontend objects and backend replies; neither timestamp represents a live broker update or page refresh.
- Verification: actual saved loading method + real Vite/FastAPI success, controlled waiting/network/JSON/HTTP/empty/incomplete cases, compiler and build. Learner reported account switching, rename retention and narrow-window use normal; teacher did not claim an actual browser click.

## Prior stage 3.3: backend flow retained for comparison

The following records the previous root index.html page flow. main.py now also serves the current frontend; the new frontend uses the proxy route above.

> 2026-10-20 教师示范：按当前保存的代码整理，供对照理解；不是学生独立填写的证据。本文件是学习笔记，不参与程序运行。

## Page delivery

- Page URL: http://127.0.0.1:8001/
- HTML file: index.html
- Backend function: main.py 中的 read_index()，用 FileResponse 返回 index.html。

## Account data

- Page action: 点击 load accounts 按钮，调用 index.html 中 methods 内的 load_accounts()。
- Request URL: GET http://127.0.0.1:8001/accounts，由 fetch('/accounts') 发出。
- Backend function: main.py 中实际名为 read_live_account() 的函数；它注册在 @app.get('/accounts') 下，返回两份账户字典组成的列表。
- Response example: 以下为3.3时的历史演示JSON；3.5已增加标识、来源和时间字段。Python列表转换为JSON数组，浏览器用await response.json()解析为JavaScript数组accounts。

```json
[
    {
        "account_type": "paper",
        "name": "paper_account",
        "netvalue": "15000.00",
        "currency": "usd",
        "holding": [{"symbol": "TSM", "quantity": "2.5"}]
    },
    {
        "account_type": "live",
        "name": "live_account",
        "netvalue": "14000.00",
        "currency": "usd",
        "holding": [{"symbol": "GOOGL", "quantity": "3"}]
    }
]
```

- Display location: for...of 每次从 accounts 取一个 account，按 account_type 分别赋给 this.paper_account、this.live_account。两个账户区域中的 p 读取名称、净值和币种；li 的 v-for 读取该账户的 holding，显示股票代码和数量。selected_account 与 v-if 决定显示哪个区域。
- Database: not connected。数据来自 Python 函数内的演示字典，不是券商账户或数据库。

## One click, one data flow

```text
index.html: load accounts button
    -> load_accounts()
    -> fetch('/accounts')
    -> main.py: read_live_account()
    -> Python list -> HTTP JSON response
    -> response.json() -> JavaScript accounts array
    -> for...of + account_type
    -> this.paper_account / this.live_account
    -> Vue updates p / li
```
