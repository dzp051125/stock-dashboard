# 当前演示数据库内容与完整账户目标

读取日期：2026-10-24（上海）。以下是本次只读查询的静态记录，全部为虚构演示数据；以后数据库修改时需重新核对。

数据库：`C:/Users/dzp11/stock-dashboard/data/dashboard.db`。

## 三张表里实际有什么

### accounts：账户基本资料

| account_id | account_type | name | base_currency | source |
| --- | --- | --- | --- | --- |
| demo_paper | paper | paper_account | usd | demo |
| demo_live | live | live_account | usd | demo |

### snapshots：各个时点的账户快照

| snapshot_id | account_id | as_of | received_at | netvalue |
| --- | --- | --- | --- | --- |
| 1 | demo_paper | 2026-10-20T20:00:00+08:00 | 2026-10-20T20:01:00+08:00 | 15000.00 |
| 2 | demo_paper | 2026-10-21T20:00:00+08:00 | 2026-10-21T20:01:00+08:00 | 15200.00 |
| 3 | demo_live | 2026-10-20T20:00:00+08:00 | 2026-10-20T20:01:00+08:00 | 14000.00 |

### holdings：对应快照的持仓

| snapshot_id | symbol | quantity |
| --- | --- | --- |
| 1 | TSM | 2.5 |
| 2 | TSM | 2.5 |
| 3 | GOOGL | 3 |

## 怎样拼成一个完整账户

- `account_id`：账户编号，用它把账户基本资料与多天快照对应起来。`demo_paper`的两份快照都属于同一个账户。
- `snapshot_id`：某一份快照的编号，用它找到那个时点的持仓。它与账户编号作用不同。
- 总览目标：基本资料取`accounts`，时点与净值取该账户最新的`snapshots`记录，持仓取这份快照对应的`holdings`。这里模拟账户最新快照为编号2。
- 历史接口`/accounts/paper/snapshots`保留多个时点，供以后查看净值变化；它不代替完整账户资料。当前Vue请求的是`/accounts`。

## 完整模拟账户返回目标（尚未全部接库）

```json
{
  "account_id": "demo_paper",
  "account_type": "paper",
  "name": "paper_account",
  "base_currency": "usd",
  "source": "demo",
  "as_of": "2026-10-21T20:00:00+08:00",
  "received_at": "2026-10-21T20:01:00+08:00",
  "netvalue": "15200.00",
  "currency": "usd",
  "holding": [
    {
      "symbol": "TSM",
      "quantity": "2.5"
    }
  ]
}
```

`currency`目前沿用基础币种`base_currency`；这是当前演示的显示约定。响应中的`holding`是既有组件使用的键名，数据库表名是`holdings`，由后端明确转换。

## 当前已经完成和接下来要做什么

学生已经把`accounts`的五项基本资料查出并正确对应到返回字典。当前`read_paper_account()`只有这五项；完整返回还需补上快照、币种显示和持仓，已有Vue需要这些字段。
接下来围绕同一个完整目标：先选择模拟账户最新快照并接入时点/净值，再按该快照编号取得持仓；保留已写查询和既有接口/组件。每次引入新SQL语法前说明执行方式，熟悉字段由学生自己对应，不重写整站。
