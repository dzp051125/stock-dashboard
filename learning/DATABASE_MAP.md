# 当前演示数据库内容与完整账户目标

读取日期：2026-10-24（上海）。以下是本次只读查询的静态记录，全部为虚构演示数据；以后数据库修改时需重新核对。

数据库：`C:/Users/dzp11/stock-dashboard/data/dashboard.db`。

## 原三张演示表里实际有什么

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
- 历史接口`/accounts/{account_id}/snapshots`按账户保留多个时点，供以后查看净值变化；它不代替完整账户资料。当前Vue请求的是`/accounts`。

## 当前完整模拟账户返回样例（已接库）

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

## 当前查询结果怎样对应下标

数据库表的列顺序与查询结果的列顺序可以不同。row中的下标以这次SELECT写出的列顺序为准。

当前快照查询是`SELECT snapshot_id, as_of, received_at, netvalue ...`，省略了表中的account_id列，因此返回：

```python
(2, "2026-10-21T20:00:00+08:00", "2026-10-21T20:01:00+08:00", "15200.00")
```

| 下标 | 这次查询中的列 |
| --- | --- |
| 0 | snapshot_id |
| 1 | as_of |
| 2 | received_at |
| 3 | netvalue |

## 当前已完成与下次接续

2026-10-25收尾：read_account(account_id)已经用三张表组装完整账户，/accounts返回demo_paper和demo_live两账户及各自最新快照、基础币种和全部持仓。每轮新建字典后append；多条与空持仓已用内存数据库验证，真实演示表仍保持上方样本。独立/accounts/paper检查路由已删除；历史接口已于后续泛化为/accounts/{account_id}/snapshots。

持仓连接：最新快照snapshot_id=2 → holdings表的snapshot_id=2 → symbol/quantity → 独立字典列表 → 返回账户holding。编号1与2虽都持有TSM，仍按选定快照查询，不能把两天持仓合并成一次持仓。

2026-10-25晚间已完成单条查询整理：账户和最新快照通过fetchone直接得到一行或None，持仓继续fetchall。持仓参数使用snapshot_row[0]，不能传snapshot_query查询对象；正常HTTP与两类404已验证，返回形状保持。


## 通用历史接口（2026-10-26）

SELECT account_id, as_of, netvalue FROM snapshots WHERE account_id = ? ORDER BY as_of ASC；参数为(account_id,)。每行映射下标0/1/2，组装成独立字典后加入列表。demo_paper两条15000.00/15200.00，demo_live一条14000.00，均由真实HTTP核对；无匹配返回[]。记录来源仍为演示种子，不冒称真实券商历史。

## 旧notes备注表与新目标（2026-10-27）

当前实际notes列为id、account_id、content、created_at、snapshot_id，快照编号有唯一索引。两条review risk演示备注属于demo_paper，但snapshot_id均为NULL，不能推断具体快照。当前旧GET/POST可用。用户要求删除零散SQL文件；为了在新环境暂时维持旧接口，演示初始化脚本目前仍创建该表与索引。

用户决定将单条备注直接放进snapshots表，教师已备份并增加note列，三条现有快照的note均为NULL；初始化脚本同步更新。下一步调整接口和页面；旧表及两条未关联备注先保留，不自动分配、不直接删除。未来同步来源数据应避免覆盖用户备注。

## 单条快照备注已接通（2026-10-28）

当前snapshots.note允许NULL；真实演示库三条均为空。历史GET返回snapshot_id和note；PUT按账户+快照更新正文并拒绝空白，DELETE清空note。页面显示一条备注和添加/修改/删除；隔离浏览器/数据库验证及服务重启持久化通过。旧notes表两条未关联记录与旧接口暂留，后续由用户决定数据处理。
