# 双账户看板：全栈学习项目

使用演示账户，逐步学习网页、后端、数据库、权限、部署与AI应用。

## 学习监督入口

- [完整最终计划 v2.2](learning/FINAL_PLAN.md)：一份阅读目标、系统地图、七章路线、教学方式与当前停点。

- [全系统分工图](ARCHITECTURE.md)：系统职责、当前链路与待验证依赖。
- [最新教学模式整改](learning/TEACHING_REVIEW_DECISIONS_2026-10-24.md)：整体框架先行、功能中学习及试用观察。

- [总计划](learning/PLAN.md)：v2.2七章路线、29阶段和完成标准，复用已有成果。
- [教学规则](learning/TEACHING_RULES.md)：整体骨架、讲解/练习方式和帮助记录。
- [三轮评审整合](learning/FINAL_REVIEW_DECISIONS.md)：Grok、Claude、Gemini建议的采用、修正和证据边界。
- [当前状态与未来三次安排](learning/STATUS.md)：监督者优先读取的最新状态。
- [最新课堂记录](learning/daily/2026-10-25.md)：主链路接库、账户显示整理与全部持仓；前一日起点及早期证据保留在对应日报。
- [数据流对照](REQUEST_FLOW.md)：新Vue组件流程与旧版后端流程。

日常进度以 `learning/STATUS.md` 为准，历史日报保留当时状态。一次代码运行成功和独立掌握分别记录。

## 当前可运行内容

`frontend/` 是当前Vue/Vite项目：两个演示账户、账户切换、概览、持仓、组件事件和全局提示。App.vue初始无账户数据并有显示保护；页面打开后自动请求/accounts，经Vite代理转给8001的FastAPI，从SQLite读取两个账户后更新组件。按钮可重新加载。

根目录 `main.py` 是当前演示数据后端；`/accounts/paper/snapshots`读取历史快照，首页`/accounts`通过read_account(account_id)读取两账户及各自最新快照与全部持仓。根目录旧index.html及其后端首页路由已删除，保留frontend/index.html。前端不再维护初始资产样本，按account_type识别账户，并用computed.current_account驱动一套展示组件；旧内存改名功能已移除。

已处理加载中、网络/读取异常、HTTP失败、非数组、空数组及单项回复。上述分支保留上次数据；前端不依赖两账户返回顺序。尚未检查所有异常账户组合（例如两项均paper），并未完成外部数据结构校验。

本项目展示和分析账户资料，交易执行在网站之外。当前没有真实券商连接、真实持仓或交易操作。

## 启动前端

本机可在项目根目录运行以下入口，它优先使用已安装的Node/pnpm，找不到时使用当前可用的本地Codex运行时。路径调整仅作用于本次启动进程；依赖该本机运行时的回退方式不作为VPS部署方案。

```powershell
.\start_frontend.cmd
```

本机最近核对环境：Node.js 24.22.1、pnpm 11.25.0；具体工具版本见 `frontend/package.json` 和锁文件。

在已安装Node.js和pnpm的终端中执行：

```powershell
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

保持服务运行，浏览器打开 http://127.0.0.1:5173/ 。不要直接双击 `.vue` 文件运行。

构建检查：在同一目录执行 `pnpm build`。

## 准备本地演示数据库

首次学习数据库时，由教师准备的脚本创建虚构账户、快照与持仓；已有数据库会保留。数据库文件被Git排除，脚本与演示记录可复现。

```powershell
.\.venv\Scripts\python.exe scripts/prepare_demo_database.py
```

快照接口：http://127.0.0.1:8001/accounts/paper/snapshots 。首页账户接口和此历史快照接口分别接入，不能因快照已接库就认定首页已完成。

## 启动后端

在项目根目录、已激活的Python虚拟环境中执行：

```powershell
python -m pip install -r requirements.txt
python -m fastapi dev main.py --host 127.0.0.1 --port 8001
```

后端运行期间保持终端开启。账户接口：http://127.0.0.1:8001/accounts ；通过开发代理也可访问 http://127.0.0.1:5173/accounts 。8001根首页返回404符合已删除旧页面入口的设计；实际看板入口为5173，其自动加载和加载按钮都需要后端运行。

## 同步约定

每次学习收尾时，整理实际代码、学习日报和滚动安排，经检查后提交到约定GitHub仓库。没有上课时保留原记录，不编造学习活动。

只上传代码、演示素材和学习记录。密钥、真实券商导出、数据库、备份及本地依赖不进入仓库。

GitHub仓库：[dzp051125/stock-dashboard](https://github.com/dzp051125/stock-dashboard)，可见性为私有，使用main分支。上传结果以仓库实际提交历史为准。
