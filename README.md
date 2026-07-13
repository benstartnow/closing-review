# 📊 盘后复盘完整版 · A股收盘报告生成器

<p align="center">
  <strong>每日 A 股收盘复盘 · 四维度策略对账 · 次日预判与操作策略</strong>
  <br>
  调取 Tushare Pro 真实收盘数据，输出黑金风格 8 章完整 HTML 报告。
  兼容 WorkBuddy、OpenClaw、Tango 等主流 AI Agent 平台。
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version 1.0.0"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license MIT"/>
  <img src="https://img.shields.io/badge/category-finance-orange" alt="category finance"/>
  <img src="https://img.shields.io/badge/data%20source-Tushare%20Pro-red" alt="Tushare Pro"/>
</p>

---

## 📋 功能概览

每个交易日收盘后，自动生成一份**专业级 A 股盘后复盘报告**（黑金风格 HTML），覆盖：

| 章节 | 内容 |
|------|------|
| ① **全天行情概览** | 六大指数 + 市场宽度 + 涨跌停连板梯队 |
| ② **资金流向全景** | 大盘资金结构 + 板块净额 TOP5 |
| ③ **板块龙头解析** | 领涨/领跌板块 TOP5 + 轮动逻辑与持续性 |
| ④ **策略复盘对账** | 开盘/操作/个股/规避四维度 + 综合评分 |
| ⑤ **次日开盘预判** | 消息面 + 技术点位 + 三情景概率 |
| ⑥ **次日操作策略** | 仓位建议 + 关注方向 + 规避方向 |
| ⑦ **风险提示** | 六类风险（含极端行情止损失效） |
| ⑧ **对账数据归档** | 四维度回写入长期跟踪日志 |

## 🚀 快速开始

### 作为 AI Agent Skill 使用

本 Skill 兼容主流 AI Agent 平台，安装后通过自然语言即可触发：

**WorkBuddy / OpenClaw / Tango 等平台：**

```
# 生成今日收盘复盘
生成今日盘后总结

# 指定日期
生成7月10日的收盘复盘

# 自然语言触发
收盘复盘
写个今日A股复盘
```

**通用 Agent 平台集成方式：**

1. 将本仓库导入你的 Agent 平台作为 Skill
2. 平台自动读取 `SKILL.md` 中的触发规则与执行流程
3. 需配置 `TUSHARE_TOKEN` 环境变量
4. Agent 收到指令后自动执行：取数 → 聚合 → 生成 HTML 报告 → 交付

### 独立使用

```bash
git clone https://github.com/benstartnow/closing-review.git
cd closing-review

# 需要 Tushare Pro Token（https://tushare.pro）
export TUSHARE_TOKEN=your_token_here
python scripts/run.py 20260710
```

## 🏗️ 项目结构

```
closing-review/
├── SKILL.md                        # Skill 核心定义 — 触发规则、执行流程、合规红线
├── scripts/
│   ├── run.py                      # 一键入口脚本
│   ├── fetch.py                    # Tushare Pro 数据获取（指数/个股/资金流）
│   ├── aggregate.py                # 数据聚合与结构化
│   └── build_report.py             # HTML 报告生成（黑金风格 8 章）
└── .gitignore
```

## 🔧 技术栈

| 组件 | 用途 |
|------|------|
| **Python 3** | 数据获取与报告生成 |
| **Tushare Pro API** | A 股实时数据（指数/个股/资金流/涨跌停） |
| **HTML + CSS** | 报告渲染（黑金风格 `#0a0b0e` + `#c9a86a`，涨红跌绿） |
| **requests** | HTTP 数据请求 |

## 📖 执行流程

1. **数据获取** — 从 Tushare Pro 拉取六大指数、全市场个股、涨跌停、行业资金流、大盘资金结构
2. **数据聚合** — 聚合成结构化 JSON
3. **报告生成** — 渲染黑金风格 8 章 HTML 报告
4. **交付** — 输出 `盘后复盘与次日策略_<日期>.html`

## ⚙️ 数据来源

- [Tushare Pro](https://tushare.pro) — A 股全量数据接口
- 需自行申请 Tushare Pro Token 并配置环境变量

## ⚠️ 合规红线

- ❌ 不出现"推荐/买入/看好/目标/建仓"等引导词
- ❌ 不引导私信代码、加群、跟车
- ✅ 个股对账标注"非推荐，仅为已发生事实的回顾性对账"
- ✅ 预测性内容标注"情绪参考，非精确预测"
- ✅ 必须带"不构成投资建议"声明

## 📄 License

本项目基于 MIT License 开源 — 详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  <sub>Made by <a href="https://github.com/benstartnow">@benstartnow</a></sub>
</p>
