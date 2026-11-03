# VPS 部署停点（2026-11-03）

## 当前已运行

- 项目位置：`/opt/stock-dashboard/releases/20261103-initial`，`current` 链接指向它。
- Python 环境：`/opt/stock-dashboard/.venv`；专用低权限用户：`stock-dashboard`。
- `stock-dashboard.service` 单进程运行，不使用开发热重载，监听 `127.0.0.1:8001`；后台读完后等待30秒再读。
- 前端在本地构建后上传到 release 的 `frontend/`。网页每1秒读取缓存，不会每秒触发 Gateway 查询。
- nginx 新入口只监听 `127.0.0.1:18080`，需要 Basic Auth。生产允许账户缓存和股票查询 GET；旧数据库、备注、AI生成、API文档未从该入口开放。
- 密码只保存在服务器 root 私有目录 `/root/.config/stock-dashboard/access.json`，nginx 使用单独的哈希文件。不要把它们放进仓库或日志。
- 没有上传 `.env`、模型密钥、数据库、券商凭据；Gateway 继续使用原登录状态。
- 原 nginx 网站、Xray、Gateway 保持运行，未改变其公网端口或防火墙。

## 验证证据

- Vue 生产构建通过；脚本验证成功、首次等待、旧数据保留、服务器重启空缓存、错误格式、网络异常和重复请求保护。
- 服务器已真实返回模拟账户和10项持仓；缓存时间两次变化；读取缓存的两次样本约18/106毫秒。
- 未登录页面与两个接口均401；登录后首页200；旧AI/文档入口404。
- 后端服务约56MiB，整机约1123MiB可用，服务重启次数0。仅短测，不代表全天稳定。
- 本次没有真实浏览器点击验收，也没有测试股票报价最终行情权限。

## 尚未公开访问

用户已报告购买 `dzp1125.me`（2026-11-03）。当前公开解析器尚返回 NXDOMAIN；注册商与订单完成状态待用户确认。准备将根域名 A 记录指向 VPS，记录值为 `142.248.136.49`。尚未配置 DNS 或签发证书。

曾准备带认证的 Cloudflare 临时预览，但自动审批拒绝启动，原因是没有明确获准把账户数据经过该第三方转发。用户随后选择自己购买域名，因此没有启动隧道或免费预览网址；此后域名由用户自己购买。

正式入口需在域名购买后配置 DNS、HTTPS 和认证。443 已被 Xray 使用，不可直接覆盖或停止；需另定 HTTPS 端口或经用户同意安排入口复用。注册域名不等于同意代理账户数据到第三方。

## 常用运维

```sh
systemctl status stock-dashboard
journalctl -u stock-dashboard -n 40 --no-pager
systemctl restart stock-dashboard
nginx -t
```

日志可能含券商标识，分享前脱敏。更新前先在本地构建验证，上传新的 release 后再切换 current、重启本服务；不要重启 Gateway 来发布网页。当前只是内存缓存，重启后会等待首轮数据；尚未实现持久连接订阅、历史落库或全天掉线维护。

2026-11-03 域名接续检查：stock-dashboard/nginx/xray active，ibgateway-login inactive。没有重启 Gateway，避免与另一对话维护冲突；正式验收前需恢复登录。

## 2026-11-04 更新：公开静态连通页

- 新静态页位于 /var/www/dzp-start/dashboard-test/index.html；IP 入口为 http://142.248.136.49/dashboard-test/。
- /etc/nginx/conf.d/dzp1125-mobile-check.conf 为 dzp1125.me 的 HTTP 根入口，只提供上述静态页，不代理账户或模型接口。未签发 HTTPS 证书。
- 阿里云权威 DNS 已返回根域名 A 记录；公共解析仍 NXDOMAIN，注册状态 clientHold。用户确认域名尚未实名，模板实名已通过；待域名认证与解除暂停后复查。
- nginx 配置校验通过；公网 IP 页面及绕过 DNS 的域名路由均 HTTP 200。没有真实手机验收证据。
- 仓库 mobile-check.html 与 deploy-mobile-check.py 保存本次页面和部署脚本；脚本在目标已存在时退出，重新部署前应先审阅现有内容。该页独立于私有看板。
