# A2UI × LINE Flex Message Demo (Python Backend)

This is a minimal, runnable LINE Chatbot demo where an “agent” decides what UI to render:

- You send text messages to the bot in LINE
- The backend generates an **A2UI-style** declarative UI description (minimal subset)
- The server converts it into a **LINE Flex Message** and replies via LINE Reply API

## Quick Start (English)

Prerequisites:

- Python `>= 3.10`
- A LINE Messaging API channel:
  - `LINE_CHANNEL_SECRET`
  - `LINE_CHANNEL_ACCESS_TOKEN`
- A public **HTTPS** URL for LINE Webhook (recommended: deploy this service to a cloud provider)

Steps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# edit .env to fill LINE_CHANNEL_SECRET / LINE_CHANNEL_ACCESS_TOKEN
uvicorn app.main:app --host 0.0.0.0 --port 3000
```

Deploy to a public HTTPS endpoint (any provider is fine), then set LINE Console Webhook URL to:

- `https://<your-public-host>/webhook`

Test in LINE by sending:

- `你好`
- `帮我订位`
- `帮助`
- `位置` (New: 发送 location 消息)
- `确认` (New: 发送 confirm 模板消息)
- `音频` (New: 发送 audio 消息)
- `视频` (New: 发送 video 消息)
- `图片` (New: 发送 image 消息)

---

# A2UI × LINE Flex Message Demo（Python 后端）

这是一个“Agent 决定 UI”的 LINE Chatbot 示例：

- 你在 LINE 里发文字给 bot
- 后端（规则版 demo agent）生成一份 **A2UI 风格** 的声明式 UI 描述（本项目实现了最小子集）
- 服务端把该 A2UI(子集) 转成 **LINE Flex Message** 并用 Reply API 回传

本项目定位是 **可运行的最小 demo**，方便你在真实渠道（LINE）里验证“Agent -> UI”的链路。

---

## 目录结构

- `app/main.py`：FastAPI webhook server（`POST /webhook`）
- `app/agent.py`：demo agent（规则逻辑，决定回什么 UI）
- `app/a2ui_state.py`：最小 A2UI state（components/dataModel/root）
- `app/a2ui_to_flex.py`：A2UI(子集) -> LINE Flex JSON
- `app/line_api.py`：LINE webhook 验签 + reply API
- `tests/`：pytest 单测（主要覆盖转换器）
- `.env.example`：环境变量模板（**只提交这个**）

详细设计说明（中文）：见 `handbook.zh-CN.md`。

---

## 前置条件

- Python `>= 3.10`
- 一个 LINE Messaging API Channel（需要拿到 `Channel secret` 与 `Channel access token`）
- 一条可被 LINE 访问到的公网 **HTTPS** Webhook URL（建议直接部署到公网服务）

---

## （可选）A2UI 安装/背景说明

这个 demo **不依赖** 安装 `a2ui` Python 包：

- 这里用的是 “A2UI 风格/协议思想” 的最小实现（`app/a2ui_state.py`）
- 以及一个只支持少量组件的映射器（`app/a2ui_to_flex.py`）

如果你希望了解/体验完整 A2UI 项目（可选）：

1.  访问 A2UI 项目主页与文档

- https://a2ui.org/

2.  克隆官方仓库（可选）

```bash
git clone https://github.com/google/a2ui.git
```

> 注意：本 demo 的运行不需要做这一步；这一步是为了理解 A2UI 协议与完整生态。

---

## 1) 安装依赖

在本目录（`Line_sample_python/`）下执行。

### 1.1 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
```

### 1.2 安装项目依赖

```bash
pip install -e .
```

如果你要跑测试：

```bash
pip install -e ".[dev]"
```

---

## 2) 配置环境变量（重要：不要提交你的 `.env`）

复制模板：

```bash
cp .env.example .env
```

编辑 `.env`，至少需要：

- `LINE_CHANNEL_SECRET=...`
- `LINE_CHANNEL_ACCESS_TOKEN=...`

说明：

- `ALLOW_INSECURE_DEV=true` 时，开发环境可以不验签（方便本地调试）。
- 生产环境务必把 `ALLOW_INSECURE_DEV` 设为 `false`，并开启验签。

---

## 3) 启动服务

方式 A：直接用 uvicorn（推荐）

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000
```

方式 B：用项目入口（会根据 `ENV=development` 自动 reload）

```bash
python -m app
```

启动后你可以先本地验证：

```bash
curl http://127.0.0.1:3000/health
```

---

## 4) 部署到公网 HTTPS（推荐）

LINE Webhook 必须是公网可访问的 **HTTPS**，因此推荐把这个 FastAPI 服务直接部署到公网平台。

你可以选择任意平台（按你熟悉的来）：

- Render / Railway / Fly.io / Cloud Run / 自建 VPS + Caddy/Nginx

部署完成后，你会得到一个公网域名，例如：

- `https://<your-public-host>`

你的 Webhook URL 就是：

- `https://<your-public-host>/webhook`

---

## 5) 在 LINE Developers Console 配置 Bot

参考官方文档：

- https://developers.line.biz/en/docs/messaging-api/

需要做的事情：

- 在 Messaging API channel 页面找到：
  - `Channel secret` -> 填入 `.env` 的 `LINE_CHANNEL_SECRET`
  - `Channel access token` -> 填入 `.env` 的 `LINE_CHANNEL_ACCESS_TOKEN`
- 打开 Webhook：Enable Webhook
- 填入 Webhook URL：`https://<你的域名>/webhook`
- 建议把 “Auto-reply messages / Greeting messages” 关掉，避免干扰测试

---

## 6) 在 LINE 里测试 demo

你可以发这些文字：

- `你好`
- `帮我订位`
- `帮助`
- `位置` (New: location message)
- `确认` (New: confirm template)
- `音频` (New: audio message)
- `视频` (New: video message)
- `图片` (New: image message)

demo 按钮为了简化使用的是 `message action`：点击后会发送 `@action <name>` 给 bot。

---

## 7) 运行测试

```bash
pip install -e ".[dev]"
pytest
```

---

## 常见问题排查

### 1) LINE 一直显示 Webhook 失败 / 收不到消息

- 确认你的 Webhook URL 是 **HTTPS** 且公网可访问
- 确认路径是 `/webhook`
- 确认部署后的服务实际在运行（health check：`GET /health`）

### 2) 401 Invalid signature

- 开发期可临时设 `ALLOW_INSECURE_DEV=true`
- 生产期请确认：
  - `.env` 里的 `LINE_CHANNEL_SECRET` 正确
  - LINE Console 里的 channel secret 没填错

### 3) Reply API 报 401/403

- 检查 `.env` 里的 `LINE_CHANNEL_ACCESS_TOKEN` 是否正确（通常是 long-lived token）
- 确认 token 没过期/没复制错

---

## 安全与提交到 Git 的建议（重要）

- **不要提交 `.env`**，只提交 `.env.example`
- 建议在提交前检查：

```bash
git status
git diff
```

---

## License

Demo 用途示例项目，按你的仓库约定为准。


## Important: 

The sample code provided is for demonstration purposes and illustrates the mechanics of A2UI and the Agent-to-Agent (A2A) protocol. When building production applications, it is critical to treat any agent operating outside of your direct control as a potentially untrusted entity.
重要提示：所提供的範例程式碼僅供示範用途，說明 A2UI 及代理對代理（Agent-to-Agent，A2A）協定的機制。在建置生產應用程式時，必須將任何在你直接控制之外運作的代理者視為可能不可信的實體。

All operational data received from an external agent—including its AgentCard, messages, artifacts, and task statuses—should be handled as untrusted input. For example, a malicious agent could provide crafted data in its fields (e.g., name, skills.description) that, if used without sanitization to construct prompts for a Large Language Model (LLM), could expose your application to prompt injection attacks.
從外部代理收到的所有操作資料——包括代理卡、訊息、工件及任務狀態——都應視為不受信任的輸入。例如，惡意代理人可能會在其欄位中提供精心設計的資料（例如名稱、技能描述），若未進行淨化而用於構建大型語言模型（LLM）的提示，可能會讓您的應用程式暴露於提示注入攻擊。

Similarly, any UI definition or data stream received must be treated as untrusted. Malicious agents could attempt to spoof legitimate interfaces to deceive users (phishing), inject malicious scripts via property values (XSS), or generate excessive layout complexity to degrade client performance (DoS). If your application supports optional embedded content (such as iframes or web views), additional care must be taken to prevent exposure to malicious external sites.
同樣地，任何 UI 定義或收到的資料流都必須被視為不可信。惡意代理人可能會試圖偽造合法介面以欺騙使用者（釣魚）、透過屬性值注入惡意腳本（XSS），或產生過度的版面複雜度以降低用戶端效能（DoS）。若您的應用程式支援可選的嵌入內容（如 iframes 或網頁檢視），則必須特別小心，避免暴露於惡意外部網站。

Developer Responsibility: Failure to properly validate data and strictly sandbox rendered content can introduce severe vulnerabilities. Developers are responsible for implementing appropriate security measures—such as input sanitization, Content Security Policies (CSP), strict isolation for optional embedded content, and secure credential handling—to protect their systems and users.
開發者責任：未能妥善驗證資料且嚴格沙盒呈現內容，可能帶來嚴重漏洞。開發者有責任實施適當的安全措施——例如輸入消毒、內容安全政策（Content Security Policies， CSP）、對可選嵌入內容的嚴格隔離，以及安全的憑證處理——以保護系統與使用者。
