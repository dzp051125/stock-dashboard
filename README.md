# 双账户看板：全栈学习项目

使用演示账户，逐步学习网页、后端、数据库、权限、部署与AI应用。

## 学习监督入口

- [总计划](learning/PLAN.md)：九章路线和完成标准。
- [当前状态与未来三次安排](learning/STATUS.md)：监督者优先读取的最新状态。
- [本次学习记录](learning/daily/2026-10-21.md)：3.4的成果、卡点、帮助和验证证据。
- [数据流对照](REQUEST_FLOW.md)：新Vue组件流程与旧版后端流程。

日常进度以 `learning/STATUS.md` 为准，历史日报保留当时状态。一次代码运行成功和独立掌握分别记录。

## 当前可运行内容

`frontend/` 是当前Vue/Vite项目：两个演示账户、账户切换、概览、持仓、组件事件和全局提示。数据来自 `frontend/src/App.vue`，尚未接回Python接口。

根目录 `index.html`、`main.py` 是上一阶段的参考版，使用FastAPI返回演示账户。两版演示内容并不完全相同，第3.5阶段接回接口时会核对字段。

本项目展示和分析账户资料，交易执行在网站之外。当前没有真实券商连接、真实持仓或交易操作。

## 启动前端

本轮验证环境：Node.js 24.19.0、pnpm 11.25.0；具体工具版本见 `frontend/package.json` 和锁文件。

在已安装Node.js和pnpm的终端中执行：

```powershell
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

保持服务运行，浏览器打开 http://127.0.0.1:5173/ 。不要直接双击 `.vue` 文件运行。

构建检查：在同一目录执行 `pnpm build`。

## 旧后端参考版

在项目根目录、已激活的Python虚拟环境中执行：

```powershell
python -m pip install -r requirements.txt
python -m fastapi dev main.py --host 127.0.0.1 --port 8001
```

参考首页：http://127.0.0.1:8001/ ；账户接口：http://127.0.0.1:8001/accounts 。当前新前端不依赖这个服务，第3.5阶段将恢复连接。

## 同步约定

每次学习收尾时，整理实际代码、学习日报和滚动安排，经检查后提交到约定GitHub仓库。没有上课时保留原记录，不编造学习活动。

只上传代码、演示素材和学习记录。密钥、真实券商导出、数据库、备份及本地依赖不进入仓库。

GitHub仓库：[dzp051125/stock-dashboard](https://github.com/dzp051125/stock-dashboard)，可见性为私有，使用main分支。上传结果以仓库实际提交历史为准。
