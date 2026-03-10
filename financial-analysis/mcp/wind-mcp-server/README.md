# Wind Financial Terminal MCP Server

A local MCP server that wraps Wind's Python API (WindPy), enabling Claude to query Wind data directly.

## Prerequisites

1. **Wind Financial Terminal** installed and logged in on your local machine
2. **WindPy** available in your Python environment (`from WindPy import w` works)
3. **Python 3.8+**

## Setup

```bash
cd financial-analysis/mcp/wind-mcp-server
pip install -r requirements.txt
```

## Configuration

The server is configured in `financial-analysis/.mcp.json` as a stdio-based MCP server:

```json
{
  "wind": {
    "type": "stdio",
    "command": "python",
    "args": ["financial-analysis/mcp/wind-mcp-server/server.py"]
  }
}
```

## Available Tools

| Tool | Wind API | Description |
|------|----------|-------------|
| `wind_wsd` | `w.wsd()` | Historical time-series data (prices, financials over date ranges) |
| `wind_wss` | `w.wss()` | Cross-sectional snapshot data (latest multiples, fundamentals) |
| `wind_wset` | `w.wset()` | Dataset queries (index constituents, IPOs, sector lists) |
| `wind_edb` | `w.edb()` | Economic database (GDP, CPI, PMI, interest rates, FX) |
| `wind_wsi` | `w.wsi()` | Intraday minute-bar data |
| `wind_wst` | `w.wst()` | Intraday tick data |
| `wind_wpf` | `w.wpf()` | Portfolio data from Wind Portfolio Manager |

## Security Codes Format

| Market | Format | Example |
|--------|--------|---------|
| A-shares (Shanghai) | XXXXXX.SH | 600519.SH |
| A-shares (Shenzhen) | XXXXXX.SZ | 000858.SZ |
| Hong Kong | XXXXX.HK | 00700.HK |
| US (NASDAQ) | XXXX.O | AAPL.O |
| US (NYSE) | XXXX.N | MSFT.N |
| Index | XXXXXX.SH/SZ | 000300.SH |
| Futures | XXXXXX.CFE/SHF/DCE/ZCE | IF2403.CFE |
| Bonds | XXXXXX.SH/SZ/IB | 019672.SH |
