# Request Flow

> 2026-10-21 教师整理：这是代码对照笔记，不是学生独立解释的证据，也不参与程序运行。

## Current stage 3.4: frontend component flow

- Current page: http://127.0.0.1:5173/, served by the Vite development server.
- Entry: frontend/index.html -> frontend/src/main.js -> frontend/src/App.vue.
- Data: App.vue 的 data() 返回两个演示账户和 select_account；当前前端不请求 Python、数据库或券商。
- Selection: AccountSelector button -> $emit('select-paper' / 'select-live') -> App.vue @ listener -> select_account -> v-if shows the matching account group.
- Header: matching account.name -> DashboardHeader heading prop -> h1.
- Overview: matching account object -> AccountSummary account prop -> three p elements.
- Rename: AccountSummary button -> $emit('rename') -> matching App.vue listener changes that account.name -> header and overview update.
- Holdings: matching account.holding array -> HoldingsList positions prop -> v-for takes one position object per li -> position.symbol / position.quantity.
- Status: App.vue status_message -> StatusMessage message prop -> p. This component is outside both account conditions, so the demo notice stays visible for either account.
- Metadata material: account_id is a fictional stable ID, account_type is paper/live, source is demo, as_of is the fictional snapshot time, received_at is the fictional receipt time, and base_currency is usd. These are teacher-prepared fixtures; neither timestamp represents a live broker update or page refresh.
- Stage 3.5: reconnect the backend and reconcile fields, then integrate loading/network/empty/error states.

## Prior stage 3.3: backend flow retained for comparison

The following records the previous root index.html/main.py version; it does not describe the new frontend's current network behavior.

> 2026-10-20 教师示范：按当前保存的代码整理，供对照理解；不是学生独立填写的证据。本文件是学习笔记，不参与程序运行。

## Page delivery

- Page URL: http://127.0.0.1:8001/
- HTML file: index.html
- Backend function: main.py 中的 read_index()，用 FileResponse 返回 index.html。

## Account data

- Page action: 点击 load accounts 按钮，调用 index.html 中 methods 内的 load_accounts()。
- Request URL: GET http://127.0.0.1:8001/accounts，由 fetch('/accounts') 发出。
- Backend function: main.py 中实际名为 read_live_account() 的函数；它注册在 @app.get('/accounts') 下，返回两份账户字典组成的列表。
- Response example: 当前演示 JSON 如下。Python 列表转换为 JSON 数组，浏览器用 await response.json() 解析为 JavaScript 数组 accounts。

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
