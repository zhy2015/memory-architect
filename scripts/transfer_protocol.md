# Bot Transfer 协议 (File Transfer & Asset Delivery)

> 本协议定义了 Agent 如何使用专属的私人中转仓库 `bot-transfer` 来进行跨设备、跨终端的大文件和多媒体素材传递。

## 场景
当大模型生成了图片、视频、PDF报告，或需要接收用户的配置打包文件时，由于 IM 渠道（如 QQ、Telegram）的附件大小和格式限制，直接发送常常失败。此时应启用 `bot-transfer` 作为中转站。

## 仓库定义
- **仓库地址**: `git@github.com:zhy2015/bot-transfer.git`
- **定位**: 私人中转站。不保留长线版本控制，仅作为快递柜。

## 工作流 (SOP)

### 1. Agent 传出 (Agent -> User)
1. 将生成的大文件或图集保存到 `bot-transfer/` 对应的目录下（如 `/bot-transfer/outputs/YYYY-MM-DD/`）。
2. 执行 `git add . && git commit -m "transfer: delivery of [资产名称]" && git push origin main`。
3. 向 IM 渠道发送消息，通知宿主：“文件已放置在快递柜，请前往 `bot-transfer` 仓库的 `outputs/` 目录自取”。

### 2. 用户传入 (User -> Agent)
1. 宿主将配置文件、大批量参考图或数据集 Push 到 `bot-transfer` 仓库的 `inputs/` 目录下。
2. 宿主在 IM 发送口令：“查收快递”。
3. Agent 执行 `cd bot-transfer && git pull origin main`，提取对应文件并在本地处理。

## 清理规则 (Cron)
为了防止 `bot-transfer` 被大文件撑爆，Agent 应在处理完 input，或确认宿主已接收 output 后，主动使用 `git rm` 清理对应文件并 Commit，保持该仓库的极度轻量。
