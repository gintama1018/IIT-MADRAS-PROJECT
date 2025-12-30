# 🛡️ DebtRisk AI | Reimagining DCA Management through Digital & AI Solutions

> **FedEx SMART Hackathon 2025** | AI-Driven Risk Classification for Debt Collection Cases

<div align="center">

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  📊 Real-time Dashboards  │  🤖 AI Risk Classification  │  🏢 DCA Management  ║
║  ⏱️ SLA Tracking          │  📜 Complete Audit Trail    │  🎯 Smart Priority   ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

</div>

---

## 🎯 Problem Statement Alignment

### The Challenge (from FedEx)
> "Reimagining Debt Collection Agency (DCA) Management through Digital & AI Solutions"

### Our Solution
We built an **AI-powered debt collection management platform** that:
- ✅ **Centralizes** case allocation, tracking, and closure
- ✅ **Enforces** SOP-driven workflows and SLAs
- ✅ **Improves** recovery efficiency and accountability
- ✅ **Provides** real-time dashboards and KPIs
- ✅ **Enables** structured collaboration with DCAs

---

## 📊 Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           DebtRisk AI Platform                                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐               │
│  │  Database   │───▶│  Preprocessing  │───▶│   Gemini AI     │               │
│  │  (20 Cases) │    │  (Context Gen)  │    │   (Risk Logic)  │               │
│  └─────────────┘    └─────────────────┘    └────────┬────────┘               │
│         │                                           │                         │
│         │                                           ▼                         │
│         │                              ┌─────────────────────┐               │
│         │                              │   Result Storage    │               │
│         │                              │   (Audit Trail)     │               │
│         │                              └────────┬────────────┘               │
│         │                                       │                             │
│         ▼                                       ▼                             │
│  ┌───────────────────────────────────────────────────────────────────┐       │
│  │                      Streamlit UI Layer                            │       │
│  ├─────────────────┬─────────────────────┬───────────────────────────┤       │
│  │   📊 Dashboard  │   🔍 Case Analysis  │     📜 Audit Log          │       │
│  │                 │                     │                            │       │
│  │  • KPI Metrics  │  • Case File View   │  • Decision History        │       │
│  │  • SLA Charts   │  • DCA Assignment   │  • Filter by Risk          │       │
│  │  • DCA Perf     │  • SLA Status       │  • Export Reports          │       │
│  │  • Risk Dist    │  • AI Assessment    │  • Full Traceability       │       │
│  └─────────────────┴─────────────────────┴───────────────────────────┘       │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Performance Indicators (KPIs)

| KPI | Description | How We Track It |
|-----|-------------|-----------------|
| **SLA Compliance Rate** | % of cases resolved within SLA | `(Cases within SLA / Total Cases) × 100` |
| **Portfolio Value** | Total outstanding debt amount | Sum of all case amounts |
| **Critical Cases** | High-priority cases needing action | Count of cases with priority = Critical |
| **DCA Performance** | Case allocation across agencies | Cases & amount per DCA |
| **Risk Distribution** | AI classification breakdown | High/Medium/Low counts |
| **Resolution Time** | Days to close cases | SLA days vs days overdue |

---

## 🏢 DCA Management Features

### Assigned DCAs in System
| DCA Name | Specialization | Case Volume |
|----------|---------------|-------------|
| **Alpha Collections** | High-value retail | 7 cases |
| **Beta Recovery Services** | Standard recovery | 7 cases |
| **Gamma Legal Collections** | Legal/escalated | 6 cases |

### SLA Enforcement
- Each case has an **SLA target** (15-90 days based on priority)
- Visual **SLA status indicators**: ✅ On Track, ⚠️ At Risk, 🚨 Breached
- Real-time **SLA compliance dashboard** with donut chart

---

## 🔄 Process Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. INGEST  │────▶│  2. ASSIGN  │────▶│  3. ANALYZE │────▶│  4. ACTION  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼
 Load case from     Assign to DCA      Run AI Risk         Store decision
 database with      based on region    Classification      for audit trail
 all attributes     and priority       with Gemini         and reporting
```

### Detailed Steps:
1. **Case Ingestion** → Load from database with DCA, SLA, priority, region
2. **Context Generation** → Convert raw numbers to semantic descriptions
3. **AI Classification** → Gemini 1.5 Flash analyzes and reasons
4. **Decision Storage** → Full audit trail with timestamp and explanation
5. **Dashboard Update** → Real-time KPIs and visualizations

---

## 🤖 AI/ML Implementation

### Why Gemini LLM instead of Traditional ML?
| Traditional ML | Gemini LLM (Our Choice) |
|---------------|-------------------------|
| Requires labeled historical data | Works with contextual descriptions |
| Black-box predictions | Explainable reasoning |
| Needs retraining for new patterns | Adapts to new scenarios |
| Fixed feature engineering | Dynamic context understanding |

### AI Prompt Engineering
We use a **structured JSON prompt** that:
- Describes the case in semantic context (not raw numbers)
- Requests specific output format: risk_level, confidence, reason, action
- Ensures consistent, parseable responses

### Sample AI Output
```json
{
  "risk_level": "HIGH",
  "confidence": 0.87,
  "reason": "Very high outstanding amount of ₹5L+ combined with 120+ days overdue and multiple failed recovery attempts indicates severe collection risk.",
  "recommended_action": "ESCALATE: Initiate legal proceedings and consider external collection agency for specialized recovery."
}
```

---

## 📈 Dashboard Screenshots

### Executive Dashboard
- **5 KPI Cards**: Total Cases, Portfolio Value, SLA Compliance, Critical Cases, Active DCAs
- **4 Charts**: Risk Distribution, DCA Allocation, Priority Breakdown, SLA Status

### Case Analysis
- **Case File Card**: Shows all case details including DCA, SLA status, priority
- **AI Assessment**: Risk level badge, confidence score, reasoning, recommended action
- **"Under the Hood"**: Transparency into preprocessing and AI context

### Audit Log
- **Decision History**: All AI decisions with timestamps
- **Risk Filters**: Toggle buttons for High/Medium/Low
- **Export**: Download as JSON for compliance

---

## 🚀 Quick Start

### Installation
```bash
cd AI-Risk-Classification
pip install -r requirements.txt
```

### Run Application
```bash
streamlit run app.py
```

### Demo Mode (No API Key)
- App works out-of-the-box with rule-based classification
- Add Gemini API key in sidebar for full AI reasoning

---

## 📁 Project Structure

```
AI-Risk-Classification/
├── database/
│   └── cases.json              # 20 cases with DCA, SLA, priority, region
├── backend/
│   ├── case_fetcher.py         # Fetch single case
│   ├── preprocessor.py         # Context generation (raw → semantic)
│   ├── gemini_client.py        # AI classification
│   ├── result_storage.py       # Audit storage
│   └── pipeline.py             # Main orchestrator
├── results/
│   └── decisions.json          # Stored AI decisions
├── app.py                      # Streamlit UI (3 tabs)
├── requirements.txt
└── README.md
```

---

## 💎 Value Proposition

| For Business | For Operations | For Compliance |
|--------------|----------------|----------------|
| Reduced overdue aging | Automated case allocation | Complete audit trail |
| Improved recovery rates | SLA enforcement | Explainable AI decisions |
| Data-driven decisions | Real-time dashboards | Governance-ready |
| DCA performance tracking | Priority-based workflow | Decision traceability |

---

## 🎤 Judge FAQ

**Q: What makes this solution unique?**
> We combine LLM reasoning with structured DCA management, SLA tracking, and complete audit trails - addressing the full FedEx problem statement.

**Q: How does AI classification work?**
> We preprocess raw case data into semantic context, send to Gemini 1.5 Flash for reasoning, and store decisions with full explainability.

**Q: Is this auditable for enterprise use?**
> Yes! Every decision includes timestamp, input data, AI reasoning, confidence score, and recommended action.

**Q: Can this scale?**
> Yes - modular architecture allows easy scaling. Database, AI, and UI are decoupled.

---

## 👨‍💻 Team

**IIT Kharagpur** | FedEx SMART Hackathon 2025

---

<div align="center">

*Built for smart, accountable, AI-driven debt recovery management* 🎯

**DebtRisk AI** | Reimagining DCA Management through Digital & AI Solutions

</div>
