#!/bin/bash
# ════════════════════════════════════════════════════════════════════
#  市场晨报系统 - 一键部署脚本（规则引擎版，无需大模型）
#  用法：bash deploy.sh
# ════════════════════════════════════════════════════════════════════
set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()    { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()     { echo -e "${GREEN}[OK]${NC} $1"; }
warn()   { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  三地股市智能晨报/晚报系统  一键部署    ║"
echo "║  规则引擎版 · 无需大模型 · 零API成本    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── 1. 检查依赖 ─────────────────────────────────────────────────────
log "检查系统依赖..."

check_cmd() {
    if command -v "$1" &> /dev/null; then
        ok "$1 已安装"
    else
        error "$1 未安装，请先安装后重试"
    fi
}

# 优先使用 Docker（推荐）
USE_DOCKER=false
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    USE_DOCKER=true
    ok "Docker + Docker Compose 已安装，将使用 Docker 部署"
elif command -v docker &> /dev/null && docker compose version &> /dev/null 2>&1; then
    USE_DOCKER=true
    COMPOSE_CMD="docker compose"
    ok "Docker + Docker Compose Plugin 已安装，将使用 Docker 部署"
else
    warn "未检测到 Docker，将使用本地 Python 部署"
    check_cmd python3
    check_cmd pip3
fi

# ── 2. 配置 .env 文件 ────────────────────────────────────────────────
log "检查配置文件..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    warn ".env 文件已创建，请填写以下必填配置："
    echo ""
    echo "  1. FEISHU_WEBHOOK_URLS - 飞书机器人Webhook（飞书群 > 设置 > 机器人）"
    echo ""
    echo "  编辑命令：nano .env 或 vim .env"
    echo ""
    read -p "是否现在打开编辑器配置 .env？[y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    else
        warn "请手动编辑 .env 后重新运行 deploy.sh"
        exit 0
    fi
else
    ok ".env 文件已存在"
fi

# 验证必填配置
source .env 2>/dev/null || true
if [ -z "$FEISHU_WEBHOOK_URLS" ]; then
    error "请在 .env 中设置 FEISHU_WEBHOOK_URLS"
fi

# ── 3. 创建缓存目录 ──────────────────────────────────────────────────
mkdir -p cache
ok "缓存目录已创建"

# ── 4. 部署 ──────────────────────────────────────────────────────────
if $USE_DOCKER; then
    log "正在构建 Docker 镜像（首次约 3-5 分钟）..."
    ${COMPOSE_CMD:-docker-compose} build --no-cache

    log "正在启动服务..."
    ${COMPOSE_CMD:-docker-compose} up -d

    sleep 3

    log "验证飞书推送配置..."
    ${COMPOSE_CMD:-docker-compose} exec market-brief python src/main.py --test || \
        warn "飞书测试失败，请检查 FEISHU_WEBHOOK_URLS 配置"

    ok "Docker 部署完成！"
    echo ""
    echo "  查看日志：docker-compose logs -f"
    echo "  立即触发：docker-compose exec market-brief python src/main.py --now premarket_asia"
    echo "  停止服务：docker-compose down"
    echo "  重启服务：docker-compose restart"

else
    # 本地 Python 部署
    log "安装 Python 依赖..."
    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --quiet

    log "验证飞书推送配置..."
    CACHE_DIR=./cache python3 src/main.py --test || \
        warn "飞书测试失败，请检查配置"

    ok "本地 Python 环境配置完成！"
    echo ""
    echo "  启动服务（前台）：python3 src/main.py"
    echo "  启动服务（后台）：nohup python3 src/main.py > cache/nohup.log 2>&1 &"
    echo "  立即触发：python3 src/main.py --now premarket_asia"

    # 可选：systemd 服务
    if command -v systemctl &> /dev/null && [ "$(id -u)" -eq 0 ]; then
        read -p "是否创建 systemd 服务（开机自启）？[y/N] " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            WORKDIR=$(pwd)
            cat > /etc/systemd/system/market-brief.service << EOF
[Unit]
Description=三地股市智能晨报/晚报系统
After=network.target

[Service]
Type=simple
WorkingDirectory=${WORKDIR}
ExecStart=/usr/bin/python3 ${WORKDIR}/src/main.py
Restart=always
RestartSec=30
EnvironmentFile=${WORKDIR}/.env
StandardOutput=append:${WORKDIR}/cache/service.log
StandardError=append:${WORKDIR}/cache/service.log

[Install]
WantedBy=multi-user.target
EOF
            systemctl daemon-reload
            systemctl enable market-brief
            systemctl start market-brief
            ok "systemd 服务已创建并启动"
            echo "  查看状态：systemctl status market-brief"
        fi
    fi
fi

echo ""
echo "════════════════════════════════════════"
echo " 部署完成！"
echo ""
echo " 特点："
echo "   无需大模型API  · 零API成本"
echo "   规则引擎分析  · 即装即用"
echo ""
echo " 调度时间（CST）："
echo "   09:00  A股+港股 开盘前分析"
echo "   15:30  A股+港股 收盘复盘"
echo "   21:00  美股 开盘前分析"
echo ""
echo " 数据来源（全部免费/可溯源）："
echo "   财联社 · 东方财富 · 新浪财经 · 新华社"
echo "   Yahoo Finance · AKShare · 美联储 · 港交所"
echo "   中国证监会 · 中国人民银行"
echo "════════════════════════════════════════"
