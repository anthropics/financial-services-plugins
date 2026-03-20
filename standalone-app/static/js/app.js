/**
 * 中国股市分析工具 - 前端逻辑
 */

// ============================================================
// Tab 切换
// ============================================================

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + tabName).classList.add('active');
    event.target.classList.add('active');
}

// ============================================================
// 工具函数
// ============================================================

function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

async function fetchAPI(url, options = {}) {
    showLoading();
    try {
        const resp = await fetch(url, options);
        const data = await resp.json();
        return data;
    } catch (e) {
        return { error: '网络请求失败: ' + e.message };
    } finally {
        hideLoading();
    }
}

function formatMoney(val) {
    if (!val || val === 0) return '-';
    if (val >= 1e12) return (val / 1e12).toFixed(2) + '万亿';
    if (val >= 1e8) return (val / 1e8).toFixed(2) + '亿';
    if (val >= 1e4) return (val / 1e4).toFixed(2) + '万';
    return val.toFixed(2);
}

function formatPct(val) {
    if (val === null || val === undefined) return '-';
    const cls = val > 0 ? 'val-up' : val < 0 ? 'val-down' : '';
    const sign = val > 0 ? '+' : '';
    return `<span class="${cls}">${sign}${val.toFixed(2)}%</span>`;
}

function formatNum(val, decimals = 2) {
    if (val === null || val === undefined || val === 0) return '-';
    return Number(val).toFixed(decimals);
}

// ============================================================
// 市场概览
// ============================================================

async function loadMarketOverview() {
    const data = await fetchAPI('/api/market/overview');
    if (data.error) {
        document.getElementById('market-indices').innerHTML =
            '<p style="color:red">错误: ' + data.error + '</p>';
        return;
    }
    let html = '';
    if (data.indices && data.indices.length > 0) {
        data.indices.forEach(idx => {
            const dir = idx.change_pct > 0 ? 'up' : idx.change_pct < 0 ? 'down' : '';
            const sign = idx.change_pct > 0 ? '+' : '';
            html += `
                <div class="card ${dir}">
                    <div class="name">${idx.name}</div>
                    <div class="price ${dir}">${formatNum(idx.price)}</div>
                    <div class="change ${dir}">${sign}${formatNum(idx.change_pct)}%</div>
                    <div class="meta">成交额: ${formatMoney(idx.amount)}</div>
                </div>`;
        });
    }
    if (data.north_flow) {
        html += `
            <div class="card">
                <div class="name">北向资金净流入</div>
                <div class="price">${formatMoney(data.north_flow.value * 1e4)}</div>
                <div class="meta">${data.north_flow.date}</div>
            </div>`;
    }
    document.getElementById('market-indices').innerHTML = html || '<p>暂无数据</p>';
}

async function loadIndustries() {
    const data = await fetchAPI('/api/market/industries');
    if (data.error) {
        document.getElementById('industry-boards').innerHTML =
            '<p style="color:red">错误: ' + data.error + '</p>';
        return;
    }
    if (!data.data || data.data.length === 0) {
        document.getElementById('industry-boards').innerHTML = '<p>暂无数据</p>';
        return;
    }
    // Sort by change_pct
    const sorted = data.data.sort((a, b) => b.change_pct - a.change_pct);
    let html = '<table><tr><th>排名</th><th>板块名称</th><th>涨跌幅</th><th>领涨股</th><th>领涨幅</th></tr>';
    sorted.slice(0, 15).forEach((b, i) => {
        html += `<tr>
            <td>${i + 1}</td>
            <td>${b.name}</td>
            <td>${formatPct(b.change_pct)}</td>
            <td>${b.leader}</td>
            <td>${formatPct(b.leader_pct)}</td>
        </tr>`;
    });
    html += '</table>';
    // Bottom 5
    html += '<h3 style="margin-top:16px">领跌板块</h3><table><tr><th>排名</th><th>板块名称</th><th>涨跌幅</th><th>领涨股</th><th>领涨幅</th></tr>';
    sorted.slice(-5).reverse().forEach((b, i) => {
        html += `<tr>
            <td>${i + 1}</td>
            <td>${b.name}</td>
            <td>${formatPct(b.change_pct)}</td>
            <td>${b.leader}</td>
            <td>${formatPct(b.leader_pct)}</td>
        </tr>`;
    });
    html += '</table>';
    document.getElementById('industry-boards').innerHTML = html;
}

// ============================================================
// A股查询
// ============================================================

function quickSearchA(code) {
    document.getElementById('a-stock-input').value = code;
    searchAStock();
}

async function searchAStock() {
    const symbol = document.getElementById('a-stock-input').value.trim();
    if (!symbol) { alert('请输入股票代码或名称'); return; }

    const data = await fetchAPI('/api/a-stock/realtime/' + encodeURIComponent(symbol));
    if (data.error) {
        document.getElementById('a-stock-result').innerHTML =
            '<p style="color:red">' + data.error + '</p>';
        return;
    }

    const dir = data.change_pct > 0 ? 'up' : data.change_pct < 0 ? 'down' : '';
    const sign = data.change_pct > 0 ? '+' : '';

    let html = `
        <div class="stock-detail">
            <div class="stock-header">
                <div>
                    <div class="name-code">${data.name} (${data.code})</div>
                    <div class="meta">A股 · 实时行情</div>
                </div>
                <div style="text-align:right">
                    <div class="big-price ${dir}">¥${formatNum(data.price)}</div>
                    <div class="change ${dir}">${sign}${formatNum(data.change_amt)} (${sign}${formatNum(data.change_pct)}%)</div>
                </div>
            </div>
            <div class="stock-metrics">
                <div class="metric"><div class="label">今开</div><div class="value">${formatNum(data.open)}</div></div>
                <div class="metric"><div class="label">昨收</div><div class="value">${formatNum(data.prev_close)}</div></div>
                <div class="metric"><div class="label">最高</div><div class="value">${formatNum(data.high)}</div></div>
                <div class="metric"><div class="label">最低</div><div class="value">${formatNum(data.low)}</div></div>
                <div class="metric"><div class="label">成交额</div><div class="value">${formatMoney(data.amount)}</div></div>
                <div class="metric"><div class="label">换手率</div><div class="value">${formatNum(data.turnover_rate)}%</div></div>
                <div class="metric"><div class="label">市盈率(动)</div><div class="value">${formatNum(data.pe)}</div></div>
                <div class="metric"><div class="label">市净率</div><div class="value">${formatNum(data.pb)}</div></div>
                <div class="metric"><div class="label">总市值</div><div class="value">${formatMoney(data.total_mv)}</div></div>
                <div class="metric"><div class="label">流通市值</div><div class="value">${formatMoney(data.circ_mv)}</div></div>
                <div class="metric"><div class="label">振幅</div><div class="value">${formatNum(data.amplitude)}%</div></div>
                <div class="metric"><div class="label">量比</div><div class="value">${formatNum(data.volume_ratio)}</div></div>
                <div class="metric"><div class="label">60日涨跌</div><div class="value">${formatPct(data.chg_60d)}</div></div>
                <div class="metric"><div class="label">年初至今</div><div class="value">${formatPct(data.chg_ytd)}</div></div>
            </div>
        </div>`;
    document.getElementById('a-stock-result').innerHTML = html;

    // Load history
    loadAStockHistory(data.code);
    // Load financial
    loadAStockFinancial(data.code);
}

async function loadAStockHistory(code) {
    const data = await fetchAPI('/api/a-stock/history/' + code + '?days=180');
    if (data.error || !data.data) {
        document.getElementById('a-stock-chart').innerHTML = '';
        return;
    }
    let html = '<h3>近半年行情走势</h3><table><tr><th>日期</th><th>开盘</th><th>收盘</th><th>最高</th><th>最低</th><th>涨跌幅</th><th>成交额</th></tr>';
    // Show last 20 days
    const recent = data.data.slice(-20).reverse();
    recent.forEach(r => {
        html += `<tr>
            <td>${r.date}</td>
            <td>${formatNum(r.open)}</td>
            <td>${formatNum(r.close)}</td>
            <td>${formatNum(r.high)}</td>
            <td>${formatNum(r.low)}</td>
            <td>${formatPct(r.change_pct)}</td>
            <td>${formatMoney(r.amount)}</td>
        </tr>`;
    });
    html += '</table>';
    document.getElementById('a-stock-chart').innerHTML = html;
}

async function loadAStockFinancial(code) {
    const data = await fetchAPI('/api/a-stock/financial/' + code);
    if (data.error || !data.data) {
        document.getElementById('a-stock-financial').innerHTML = '';
        return;
    }
    let html = '<h3>财务数据</h3><table>';
    if (data.data.length > 0) {
        const keys = Object.keys(data.data[0]);
        html += '<tr>';
        keys.forEach(k => { html += '<th>' + k + '</th>'; });
        html += '</tr>';
        data.data.forEach(row => {
            html += '<tr>';
            keys.forEach(k => {
                const v = row[k];
                html += '<td>' + (v !== null ? v : '-') + '</td>';
            });
            html += '</tr>';
        });
    }
    html += '</table>';
    document.getElementById('a-stock-financial').innerHTML = html;
}

// ============================================================
// 港股查询
// ============================================================

function quickSearchHK(code) {
    document.getElementById('hk-stock-input').value = code;
    searchHKStock();
}

async function searchHKStock() {
    const symbol = document.getElementById('hk-stock-input').value.trim();
    if (!symbol) { alert('请输入港股代码'); return; }

    const data = await fetchAPI('/api/hk-stock/realtime/' + encodeURIComponent(symbol));
    if (data.error) {
        document.getElementById('hk-stock-result').innerHTML =
            '<p style="color:red">' + data.error + '</p>';
        return;
    }

    const prevClose = data.prev_close || 0;
    const change = prevClose ? data.price - prevClose : 0;
    const changePct = prevClose ? (change / prevClose * 100) : 0;
    const dir = change > 0 ? 'up' : change < 0 ? 'down' : '';
    const sign = change > 0 ? '+' : '';

    let html = `
        <div class="stock-detail">
            <div class="stock-header">
                <div>
                    <div class="name-code">${data.name} (${data.code}.HK)</div>
                    <div class="meta">港股 · ${data.currency}</div>
                </div>
                <div style="text-align:right">
                    <div class="big-price ${dir}">HK$${formatNum(data.price)}</div>
                    <div class="change ${dir}">${sign}${formatNum(change)} (${sign}${formatNum(changePct)}%)</div>
                </div>
            </div>
            <div class="stock-metrics">
                <div class="metric"><div class="label">今开</div><div class="value">${formatNum(data.open)}</div></div>
                <div class="metric"><div class="label">昨收</div><div class="value">${formatNum(data.prev_close)}</div></div>
                <div class="metric"><div class="label">最高</div><div class="value">${formatNum(data.high)}</div></div>
                <div class="metric"><div class="label">最低</div><div class="value">${formatNum(data.low)}</div></div>
                <div class="metric"><div class="label">成交量</div><div class="value">${formatMoney(data.volume)}</div></div>
                <div class="metric"><div class="label">市值</div><div class="value">${formatMoney(data.market_cap)}</div></div>
                <div class="metric"><div class="label">市盈率</div><div class="value">${formatNum(data.pe)}</div></div>
                <div class="metric"><div class="label">市净率</div><div class="value">${formatNum(data.pb)}</div></div>
                <div class="metric"><div class="label">股息率</div><div class="value">${data.dividend_yield ? formatNum(data.dividend_yield * 100) + '%' : '-'}</div></div>
                <div class="metric"><div class="label">Beta</div><div class="value">${formatNum(data.beta)}</div></div>
                <div class="metric"><div class="label">52周高</div><div class="value">${formatNum(data.fifty_two_week_high)}</div></div>
                <div class="metric"><div class="label">52周低</div><div class="value">${formatNum(data.fifty_two_week_low)}</div></div>
            </div>
        </div>`;
    document.getElementById('hk-stock-result').innerHTML = html;

    // Load history
    loadHKStockHistory(symbol);
}

async function loadHKStockHistory(code) {
    const data = await fetchAPI('/api/hk-stock/history/' + code + '?period=6mo');
    if (data.error || !data.data) {
        document.getElementById('hk-stock-chart').innerHTML = '';
        return;
    }
    let html = '<h3>近半年行情走势</h3><table><tr><th>日期</th><th>开盘</th><th>收盘</th><th>最高</th><th>最低</th><th>成交量</th></tr>';
    const recent = data.data.slice(-20).reverse();
    recent.forEach(r => {
        html += `<tr>
            <td>${r.date}</td>
            <td>${formatNum(r.open)}</td>
            <td>${formatNum(r.close)}</td>
            <td>${formatNum(r.high)}</td>
            <td>${formatNum(r.low)}</td>
            <td>${formatMoney(r.volume)}</td>
        </tr>`;
    });
    html += '</table>';
    document.getElementById('hk-stock-chart').innerHTML = html;
}

// ============================================================
// 股票筛选
// ============================================================

function applyStrategy(strategy) {
    switch (strategy) {
        case 'value':
            document.getElementById('pe-min').value = '';
            document.getElementById('pe-max').value = '15';
            document.getElementById('pb-max').value = '2';
            document.getElementById('mv-min').value = '50';
            document.getElementById('mv-max').value = '';
            break;
        case 'growth':
            document.getElementById('pe-min').value = '';
            document.getElementById('pe-max').value = '50';
            document.getElementById('pb-max').value = '';
            document.getElementById('mv-min').value = '30';
            document.getElementById('mv-max').value = '';
            break;
        case 'dividend':
            document.getElementById('pe-min').value = '';
            document.getElementById('pe-max').value = '20';
            document.getElementById('pb-max').value = '3';
            document.getElementById('mv-min').value = '100';
            document.getElementById('mv-max').value = '';
            break;
        case 'small_cap':
            document.getElementById('pe-min').value = '';
            document.getElementById('pe-max').value = '40';
            document.getElementById('pb-max').value = '';
            document.getElementById('mv-min').value = '20';
            document.getElementById('mv-max').value = '100';
            break;
    }
}

async function runScreener() {
    const filters = {
        pe_min: document.getElementById('pe-min').value || null,
        pe_max: document.getElementById('pe-max').value || null,
        pb_max: document.getElementById('pb-max').value || null,
        mv_min: document.getElementById('mv-min').value || null,
        mv_max: document.getElementById('mv-max').value || null,
    };

    const data = await fetchAPI('/api/screener', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters),
    });

    if (data.error) {
        document.getElementById('screener-result').innerHTML =
            '<p style="color:red">' + data.error + '</p>';
        return;
    }

    let html = `<p>共找到 ${data.count} 只符合条件的股票</p>`;
    html += '<table><tr><th>#</th><th>代码</th><th>名称</th><th>最新价</th><th>涨跌幅</th><th>PE</th><th>PB</th><th>总市值</th><th>换手率</th></tr>';
    data.data.forEach((s, i) => {
        html += `<tr>
            <td>${i + 1}</td>
            <td><a href="#" onclick="document.getElementById('a-stock-input').value='${s.code}';showTab('a-stock');searchAStock();return false;">${s.code}</a></td>
            <td>${s.name}</td>
            <td>¥${formatNum(s.price)}</td>
            <td>${formatPct(s.change_pct)}</td>
            <td>${formatNum(s.pe)}</td>
            <td>${formatNum(s.pb)}</td>
            <td>${formatMoney(s.total_mv)}</td>
            <td>${formatNum(s.turnover_rate)}%</td>
        </tr>`;
    });
    html += '</table>';
    document.getElementById('screener-result').innerHTML = html;
}

// ============================================================
// AH对比
// ============================================================

async function loadAHComparison() {
    const data = await fetchAPI('/api/market/ah-comparison');
    if (data.error) {
        document.getElementById('ah-result').innerHTML =
            '<p style="color:red">' + data.error + '</p>';
        return;
    }

    let html = `<p>共 ${data.count} 只AH两地上市股票</p>`;
    html += '<table><tr><th>#</th><th>名称</th><th>A股代码</th><th>H股代码</th><th>A股价(¥)</th><th>H股价(HK$)</th><th>AH比价</th></tr>';
    // Sort by premium desc
    const sorted = data.data.sort((a, b) => b.premium - a.premium);
    sorted.forEach((s, i) => {
        const premCls = s.premium > 1.3 ? 'val-up' : s.premium < 1.0 ? 'val-down' : '';
        html += `<tr>
            <td>${i + 1}</td>
            <td>${s.name}</td>
            <td>${s.a_code}</td>
            <td>${s.h_code}</td>
            <td>¥${formatNum(s.a_price)}</td>
            <td>HK$${formatNum(s.h_price)}</td>
            <td class="${premCls}">${formatNum(s.premium)}</td>
        </tr>`;
    });
    html += '</table>';
    document.getElementById('ah-result').innerHTML = html;
}

// ============================================================
// 页面初始化
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-load market overview
    loadMarketOverview();
});
