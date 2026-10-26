# 当前学习状态与滚动安排

收尾：2026-10-27 00:18:38（上海）。本课段开始于2026-10-26 19:59:31，跨午夜至10月27日，用户明确停止；聊天跨度含交流/等待，有效学习分钟未统计。

## 下次直接从这里继续

**第1章4/4功能目标完成，第一版历史展示补充已通过。当前第2章2.1“账户备注新增与读回”进行中，尚未验收完成。**

打开main.py底部create_notes：学生已将路由改成POST /accounts/{account_id}/notes，函数参数改成(account_id: str, note: NoteCreate)，但INSERT参数仍为(account_id, content, created_at)。当前content与created_at未定义，请求会失败；收尾在隔离内存数据库确认NameError，未对真实库提交备注。不要把语法/导入通过当作接口可用。

上次已讲但学生尚未保存的任务：导入datetime/timezone，在函数内生成UTC时间并isoformat为created_at，把SQL参数content改为note.content。恢复时先读实际文件，再按新知识逐步带写，不替学生补完。然后在同一功能内处理空白正文和未知账户，再用/docs亲手提交；之后添加读回接口和网页备注输入/显示。NoteCreate仅验证必需字符串，并不会自动拒绝空字符串。

当前选择直接改现有create_notes为POST处理函数，复用已写INSERT/commit/lastrowid/finally，不额外造重复保存函数。created_at由后端生成，不让用户填写；未知账户检查不能依赖要求存在快照的read_account。

## 已保存成果及帮助

- 历史：学生创建AccountHistory.vue，props接收account，data保存snapshots/history_message，mounted请求通用历史接口；App.vue以account_id作为组件key，切账户重建并重新请求；v-for显示时点/净值/币种，行key为as_of。主体学生写，组件归属、状态独立、mounted与key机制经多次具体指导，不算独立熟练。
- notes表：scripts/creat_notes.sql已由学生逐步带写完成（保留实际文件名）：id INTEGER PRIMARY KEY、account_id TEXT NOT NULL REFERENCES accounts(account_id)、content TEXT NOT NULL、created_at TEXT NOT NULL。教师备份后执行DDL；实际库现在有四张表，notes为0行，原账户/快照/持仓未改。NOT NULL不拒绝空白文本，外键需每个写连接开启。
- 保存逻辑：学生经指导完成连接、PRAGMA foreign_keys=ON、参数化INSERT、commit、lastrowid、finally关闭并返回ID。改成POST之前的完整低层函数曾在隔离库验证合法写入可被另一连接读到、ID匹配、未知账户拒绝及连接关闭。**当前源码正在接HTTP，旧函数的通过不代表当前POST通过。**
- 请求结构：from pydantic import BaseModel与class NoteCreate(BaseModel): content: str已保存并可导入。路径取账户编号、正文取note.content的联系已讲；时间生成尚未写入源码。
- 新知识/没亲手写过的内容必须解释并带写；反复练过且学生想尝试的内容才给目标与小提示。见过/复制/运行/发1均不是掌握证据。收尾记录集中更新，课堂优先推进动手，避免长时间等教师整理文档。

## 当前实际链路

```text
演示种子 → SQLite(accounts / snapshots / holdings)
          → read_account → GET /accounts → App.vue.load_accounts
          → 按account_type分配 → computed.current_account → 概览/持仓组件
snapshots → read_snapshots → GET /accounts/{account_id}/snapshots
          → AccountHistory → 历史列表
notes结构已存在 → POST接收/时间/校验尚未接完 → 读回与网页表单未实现
```

- 账户/最新快照fetchone，无匹配404；持仓fetchall，每轮新建字典append，空持仓[]，finally关闭连接。历史按as_of升序，未知账户或无历史均[]，尚未区分。
- 前端初始null有保护、mounted自动加载，按类型识别两账户而非位置；source/as_of/received_at已显示；无前端重复初始资产。根旧HTML删除，当前frontend/index.html入口。
- 虚构库：paper两快照15000.00/15200.00，live一快照14000.00；金额和数量字符串。真实IBKR、导入、模型、登录、部署均未实现。

## 验证与边界

- 历史阶段已有：真实HTTP与5173代理paper2/live1升序；实际保存方法配真实/控制回复验证成功、空数组清旧、非数组早返回；实际Vue渲染器验证账户往返与迟到回复不污染当前实例；实际模板逐行字段和key编译通过，pnpm build通过。不是本轮真实浏览器点击。
- notes表DDL已用隔离库验证列/外键/主键/非空及空字符串语义；教师执行真实DDL前SQLite备份。备份只在本机backups，数据库与备份不入Git。
- 收尾只读确认真实notes为0行；隔离执行当前保存POST确认content未定义，不写真实库。当前API未完成，没有成功提交或读回证据。
- DB路径依赖项目根启动；前端未覆盖所有异常账户组合。现有种子脚本仅创建原三表，新环境需另执行scripts/creat_notes.sql创建备注表，见README。

## 薄弱点与下次复用

SQL结果行/字段、元组逗号、列表与字典及append引用、Vue props与data独立、mounted与key、this/await/JSON、服务启动与路径继续在真实功能复用。CREATE TABLE/INSERT/事务/lastrowid/BaseModel仍是指导学习，不因写过一次就改成独立任务。下一课datetime/UTC/isoformat先解释输入输出和执行位置。

## 下一两三次安排

1. 补完现有POST的正文取值、后端时间及空白/错误账户处理，隔离验证后由学生用/docs实际提交。
2. 备注GET读回与Vue输入/保存/显示，核对选中账户归属、刷新持久化和失败提示；至此才验收2.1。
3. 接续2.2修改/删除，再按既定路线考虑有用途的导入与学生Git。券商样本、岗位资格/出勤、模型渠道/预算仍待核实，不冒称完成。

## 恢复与协作

项目C:/Users/dzp11/stock-dashboard。根目录后端：.\.venv\Scripts\python.exe -m fastapi dev main.py --host 127.0.0.1 --port 8001；另一终端根目录.\start_frontend.cmd。网页http://127.0.0.1:5173/，接口测试http://127.0.0.1:8001/docs。8001根路径404正常；已有服务正常时不重复重启。

代码/英文界面由学生按指导写，教师负责必要支架、检查和记录；不将教师测试/代提交算学生独立。章百分比为功能成果，不等同掌握。教学规则和七章路线继续原版，不再重排。课后按授权一次提交到私有仓库main，保留未完成停点，不提交数据库/备份/凭据/依赖/空杂项；实际推送结果另按命令确认。
