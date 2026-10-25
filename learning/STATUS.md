# 当前学习状态与滚动安排

更新：2026-10-26课后。用户已明确结束。此课段开始于2026-10-25 22:22:37（上海），跨午夜，收尾首次核对为2026-10-26 00:47:15；有效学习分钟未知，聊天跨度不算连续投入。

## 下次直接从这里继续

**第1章功能目标4/4（100%）完成；当前先补第一版产品的历史展示，备注新增与读回随后接续。** 七章主线与已有成果保留，不重置进度。调整依据：用户要求重新审视产品大框架，随后继续学习；优先补齐总览、持仓、历史、来源/时点说明的第一版闭环。

- 历史后端已通过：`GET /accounts/{account_id}/snapshots`，模拟盘两条、实盘一条，时间升序。
- 前端历史区尚未实现。最后布置的新文件`frontend/src/AccountHistory.vue`在收尾检查时**不存在**，不能算已写/已接页面。
- 下次先让学生创建该组件的取数部分：template标题`Account history`；props接收account；data返回snapshots空数组及history_message；methods中async load_snapshots按`'/accounts/' + this.account.account_id + '/snapshots'`请求并保存解析数组、处理失败提示。参考现有App.vue加载函数，但历史一条记录是正常结果。
- 验证取数后接入App.vue，再完成历史列表、加载/空/失败反馈以及账户切换时旧历史与异步请求的隔离。当前未生成组件支架或代写核心代码。

## 功能成果与实际帮助

| 范围 | 已有成果 | 帮助与理解证据 |
| --- | --- | --- |
| 1.1 运行入口/全图 | 项目环境、两服务、实际文件与请求入口 | 教师准备环境，学生按指导恢复正确服务；独立恢复仍待观察 |
| 1.2 快照查询 | 参数查询、逐行字典、无匹配空列表 | 经局部示范及元组/字段/列表字典提示完成；历史接口已在产品补充中泛化 |
| 1.3 完整账户到页面 | 两账户最新快照和全部持仓接通；前端统一显示 | 早期有助手较多实现；学生后续完成身份分配、computed合并模板、持仓逐条字典和fetchone整理，经提示完成 |
| 1.4 自然字段变化 | 概览来源、估值时点、接收时点及标签显示；正常/无账户边界通过 | 给目标后学生组织模板，无整段答案；学生已讲述主要数据流，连接/查询及HTTP/Vue中间过程经教师补准 |
| 产品补充：历史展示 | 后端泛化完成；前端未开始 | 学生写路由与SQL，表名/参数元组/列表字典混用、误删/accounts、关闭连接经提示修复；不计独立组织 |

功能完成度与独立能力分开。学生能够指出fetch、数据库、组件导入、props及模板显示，仍需复用具体数据巩固中间结果；不要求因遗忘重学整章或追加考试。

## 当前真实链路

```text
演示种子 → SQLite(accounts / snapshots / holdings)
                    ↓ read_account(account_id)
                GET /accounts
                    ↓ App.vue.load_accounts
       按account_type分配 → computed.current_account
                    ↓ 一套标题/概览/持仓组件

snapshots → read_snapshots(account_id)
          → GET /accounts/{account_id}/snapshots
          → 历史组件/页面：尚未接入
```

- main.py中账户和最新快照使用fetchone；持仓使用fetchall，每行创建独立字典append。未知账户/缺快照在read_account中404；空持仓[]；finally关闭连接。
- 通用历史接口按account_id参数查询，ORDER BY as_of ASC；每条返回account_id/as_of/netvalue。连接在try前创建，finally关闭，调试print已移除。旧/accounts/paper/snapshots已被泛化替代；实际账户编号使用demo_paper/demo_live。
- 历史查询无匹配返回[]，当前不能区分未知账户与已知账户无历史，尚未宣称完整输入/权限校验。
- App.vue初始null、有显示保护、mounted自动加载；按account_type识别账户，computed供一套组件使用。概览显示source/as_of/received_at。前端入口为frontend/index.html，根旧HTML及后端首页路由已删除。
- 演示库paper两时点15000.00/15200.00，live一时点14000.00；金额/数量仍为字符串。真实IBKR、模型、登录、导入、部署尚未实现。

## 验证与边界

- 最新真实HTTP：8001主账户接口及两个账户历史均200，历史数量2/1且升序；5173代理同样通过。无匹配历史返回[]。
- 收尾Python语法和pnpm build通过。
- 概览新字段通过实际Vue模板渲染脚本核对paper/live及初始null边界；这是脚本渲染，不是本课重新操作浏览器。
- fetchone整理后用内存SQLite核对未知账户/缺快照的404；此前完整持仓的多条与空结果检查继续保留，不冒称本课重测全部路径。真实数据库未修改。
- 后端数据库路径仍依赖项目根启动；前端现有数组长度检查未覆盖所有坏账户组合。历史UI、账户切换并发等尚未实现，不能报告完成。

## 薄弱点及下次复用

| 概念 | 真实观察/复用位置 |
| --- | --- |
| 查询对象、行、字段下标 | 曾将snapshot_query对象当SQL参数；fetchone取下一整行，row[0]取行内第一项，后续历史请求继续复用 |
| 单元素参数元组 | 逗号放括号外不能组成元组；多次具体提示后修正 |
| 列表与字典、record/records | 历史循环曾覆盖一字典、向列表按字符串键赋值；收集多行时继续原位巩固 |
| 字典引用与append | 必须每轮新建字典，避免多项共享同一对象；已修正，不等于独立熟练 |
| computed/this/await/JSON | 已接通实际页面；历史组件沿已用写法组织，按需补解释 |
| 服务、路径、关闭连接 | 恢复时核对正确项目；connection在try前，finally关闭；服务运行中无需重启 |

## 下一两三次安排

1. 创建并验证AccountHistory.vue的真实取数函数；不造前端固定历史样本，不要求两条记录才算成功。
2. 接入当前账户区域，完成历史列表及加载/空/失败状态，隔离切换时旧数据与迟到回复；用实际账户和相关边界验证。
3. 回到第2章2.1备注新增与读回，先明确存储归属与完整输入/保存/读回链路。并行准备最小券商样本资料清单，实盘/模拟盘可读性如实标有/无/未知，2.3前决定写入路径；岗位届别/出勤初筛仍待做，目标2026年11月底前，模型渠道/预算在第2章准备。

## 恢复与协作约定

项目C:/Users/dzp11/stock-dashboard。根目录后端命令`.\.venv\Scripts\python.exe -m fastapi dev main.py --host 127.0.0.1 --port 8001`；另一终端根目录`.\start_frontend.cmd`；网页http://127.0.0.1:5173/。8001根首页404符合当前设计。详见[README](../README.md)。

网站建设为主，教师先说明整体位置和设计理由，学生组织核心代码；新机制完整局部示范，熟悉改动合并任务。能运行也审查实质质量和实际效率；不为假设性能或无关排版反复重写。1表示提交/继续，不是掌握证据；40分钟仅参考，由用户说停。

路线：[PLAN](PLAN.md)、[FINAL_PLAN](FINAL_PLAN.md)；规则：[TEACHING_RULES](TEACHING_RULES.md)；结构：[ARCHITECTURE](../ARCHITECTURE.md)；表与样本：[DATABASE_MAP](DATABASE_MAP.md)；当前流转：[REQUEST_FLOW](../REQUEST_FLOW.md)；本课证据：[10-25](daily/2026-10-25.md)、[10-26](daily/2026-10-26.md)。归档目的地为私有仓库dzp051125/stock-dashboard的main，Muse读取权限未验证。实际推送以Git结果与最终回复为准。
