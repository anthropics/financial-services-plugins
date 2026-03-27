# 三地股市智能晨报/晚报系统

> 基于 Claude 大模型第一性原则分析。开盘前30分钟自动推送 A股/港股/美股 深度分析到飞书，收盘后真正复盘验证建议准确性，全程数据可溯源。

## 功能概览

| 推送时间 (CST) | 内容 |
|---------------|------|
| 09:00 周一至五 | A股+港股 开盘前分析（包含美股隔夜数据） |
| 15:30 周一至五 | A股+港股 收盘复盘 + 对比早盘建议准确性 + 明日策略 |
| 21:00 周一至五 | 美股 开盘前分析 + 当日亚洲盘回顾 |

## 前置准备

在开始之前，准备好以下两项：

| 项目 | 说明 | 获取方式 |
|------|------|---------|
| **Anthropic API Key** | Claude 大模型分析（强烈推荐） | [console.anthropic.com](https://console.anthropic.com/) |
| **飞书机器人 Webhook** | 接收推送消息（必填） | 飞书群 > 设置 > 群机器人 > 添加机器人 > 自定义机器人 |

> 未配置 `ANTHROPIC_API_KEY` 时，系统会降级为规则引擎（关键词匹配），分析质量明显下降，收盘复盘功能基本失效。

---

## Windows 部署（推荐）

### 第一步：安装 Python

1. 打开 https://www.python.org/downloads/，下载 Python **3.12+**
2. 运行安装程序，**务必勾选** ✅ `Add Python to PATH`
3. 安装完成后重启命令提示符

### 第二步：下载项目

```
git clone https://github.com/straggler-liu/financial-services-plugins.git
cd financial-services-plugins\market-morning-brief
```

或直接下载 ZIP 解压，进入 `market-morning-brief` 文件夹。

### 第三步：一键安装

双击 **`install.bat`**，脚本将自动：
- 安装所有 Python 依赖（使用国内镜像加速）
- 创建 `.env` 配置文件并打开记事本供填写
- 创建 `cache` 目录

### 第四步：填写配置

在记事本中填写 `.env`：

```ini
# 强烈推荐：Claude 大模型分析
ANTHROPIC_API_KEY=sk-ant-你的密钥

# 必填：飞书 Webhook
FEISHU_WEBHOOK_URLS=https://open.feishu.cn/open-apis/bot/v2/hook/你的webhook

# 关注的板块（逗号分隔）
FOCUS_SECTORS=科技,新能源,半导体,消费,医药,金融,房地产,人工智能

# 自选标的（可选，A股代码/港股代码/美股Ticker）
WATCHLIST=600519,00700,AAPL,NVDA
```

保存并关闭记事本。

### 第五步：测试推送

打开命令提示符，在项目目录下运行：

```cmd
python src\main.py --test
```

飞书群收到测试消息即表示配置正确。

### 第六步：启动服务

**方式一：前台运行**（推荐，窗口可见、方便调试）

```
双击 start.bat
```

保持窗口不关闭，电脑会在 09:00 / 15:30 / 21:00 自动推送。

**方式二：后台静默运行**（不占用桌面）

```
双击 start_background.bat
```

---

## Windows 服务管理

| 操作 | 方式 |
|------|------|
| 查看运行状态 | 双击 `check_status.bat` |
| 停止后台服务 | 双击 `stop.bat` |
| 设置开机自启 | 双击 `setup_autostart.bat` |
| 取消开机自启 | 双击 `remove_autostart.bat` |
| 立即触发（调试） | 见下方命令 |

```cmd
python src\main.py --now premarket_asia   # 立即生成亚洲盘前报告
python src\main.py --now postmarket_asia  # 立即生成收盘复盘
python src\main.py --now premarket_us     # 立即生成美股盘前报告
python src\main.py --validate             # 验证配置
```

## 注意事项

**电脑需保持开机**：系统在 09:00 / 15:30 / 21:00 定时推送，电脑关机或休眠时不会推送。

- 台式机：设置"从不睡眠"即可长期运行
- 笔记本：建议接电源，设置屏幕关闭但不休眠
- 若需彻底不间断推送：使用云服务器（见下方高级部署）

**美国夏令时调整**：

| 时期 | 美股开盘 CST | 建议设置 |
|------|-------------|---------|
| 夏令时（3月第2周 ~ 11月第1周） | 21:30 | `US_PREMARKET_HOUR=21` |
| 冬令时（其余时间） | 22:30 | `US_PREMARKET_HOUR=22` |

修改 `.env` 后重启服务生效。

---

## 分析引擎

系统优先使用 Claude 大模型对所有市场数据进行第一性原则深度分析：

```
市场价格 = f(盈利预期E, 无风险利率r, 流动性L, 风险情绪ρ)

对每个新闻事件，Claude 推理：
  1. 真实语义理解 → 正确处理否定句、同义词、上下文
  2. 影响变量判断 → 哪个变量(E/r/L/ρ)，方向和幅度
  3. 传导链条推理 → 完整逻辑路径（非模板拼接）
  4. 跨事件联动  → 综合多个事件复合影响
  5. 个股映射    → 推理受影响个股并给出理由
```

未配置 `ANTHROPIC_API_KEY` 时自动降级为规则引擎（关键词匹配），但分析质量显著下降。

---

## 数据来源（全部免费）

| 类型 | 来源 |
|------|------|
| A股行情 | AKShare、东方财富 |
| 港股行情 | Yahoo Finance、AKShare |
| 美股行情 | Yahoo Finance |
| 财经新闻 | 财联社、东方财富、新浪财经、新华社 |
| 政策动态 | 证监会、央行、美联储（官网 RSS） |
| 机构研报 | 东方财富研报中心 |
| 经济日历 | Investing.com、AKShare |

---

## 目录结构

```
market-morning-brief\
├── install.bat              ← Windows 一键安装（从这里开始）
├── start.bat                ← 前台启动（推荐调试）
├── start_background.bat     ← 后台静默启动
├── stop.bat                 ← 停止后台服务
├── check_status.bat         ← 查看运行状态和最新日志
├── setup_autostart.bat      ← 设置开机自启动
├── remove_autostart.bat     ← 取消开机自启动
├── .env.example             ← 配置模板（复制为 .env 后填写）
├── .env                     ← 实际配置（你创建的，不提交 git）
├── requirements.txt         ← Python 依赖
├── cache\                   ← 自动创建，存放日志和策略记忆
│   ├── market_brief.log     ← 运行日志
│   └── last_strategy.json   ← 策略记忆（用于收盘复盘对比）
└── src\
    ├── main.py              ← 主入口（调度器 + CLI）
    ├── config.py            ← 配置管理
    ├── analyzers\
    │   ├── claude_analyzer.py  ← Claude 大模型分析（主引擎）
    │   └── rule_analyzer.py    ← 规则引擎（无 API Key 时的降级兜底）
    ├── fetchers\            ← 数据抓取（新闻/行情/研报/经济日历）
    └── notifiers\
        └── feishu.py        ← 飞书消息卡片推送
```

---

## 常见问题

**Q: install.bat 安装失败怎么办？**

手动安装：
```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q: 测试推送（--test）报错 "FEISHU_WEBHOOK_URLS 未设置"？**

确认 `.env` 文件存在且 `FEISHU_WEBHOOK_URLS=` 后面已填写完整 URL（不是示例值）。

**Q: 推送了但飞书没收到消息？**

1. 检查飞书群是否添加了机器人
2. Webhook URL 是否完整（以 `/hook/` 结尾的完整地址）
3. 运行 `check_status.bat` 查看日志中的错误信息

**Q: 能设置多个飞书群吗？**

可以，逗号分隔：
```ini
FEISHU_WEBHOOK_URLS=https://open.feishu.cn/.../hook/xxx,https://open.feishu.cn/.../hook/yyy
```

**Q: Claude 每日费用大概多少？**

每日3次推送约 $0.06~0.15（约 ¥0.4~1.1），使用 claude-sonnet-4-6 模型。

**Q: 电脑睡眠后任务还会触发吗？**

不会。建议：控制面板 → 电源选项 → 从不睡眠（台式机），或使用云服务器。

---

## 高级部署（云服务器，7×24不间断）

若需要电脑关机时也能推送，可用云服务器（1核1G，约¥30/月）：

```bash
# Ubuntu/Linux 服务器
git clone https://github.com/straggler-liu/financial-services-plugins.git
cd financial-services-plugins/market-morning-brief
pip3 install -r requirements.txt
cp .env.example .env && nano .env

# 后台运行（systemd 方式）
# 或简单方式：
nohup python3 src/main.py > cache/nohup.log 2>&1 &

# Docker 方式（需安装 Docker）
docker-compose up -d
```

---

## 免责声明

本系统生成的分析报告基于公开可获取的数据，由 Claude AI 辅助分析生成。所有分析仅供参考，不构成任何投资建议。投资决策需自行承担风险。数据来源均已标注，但不对数据准确性作出保证。
