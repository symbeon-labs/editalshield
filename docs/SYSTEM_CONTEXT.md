# 🧠 EditalShield - System Context
### Internal Knowledge Base for AI Agents & MCP Integrations

**Version:** 0.3.0  
**Last Updated:** 2025-12-05  
**Purpose:** This document serves as the definitive reference for AI agents, MCP servers, and internal tools to understand EditalShield's capabilities, architecture, and usage patterns.

---

## 🎯 What is EditalShield?

EditalShield is an **AI-powered IP Protection Framework** designed to help Brazilian startups navigate the critical dilemma when submitting innovation grant proposals:

> **Reveal too much = Lose competitive advantage**  
> **Reveal too little = Lose the grant**

### Core Mission
Automatically detect, classify, and protect intellectual property in grant proposals (memoriais descritivos) while maintaining technical clarity for evaluators.

---

## 🏗️ System Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────┐
│                    EditalShield Core                     │
├─────────────────────────────────────────────────────────┤
│  1. Memorial Protector (IP Risk Analysis)               │
│  2. Juridical Agent (Legal Interpretation)              │
│  3. Knowledge Connectors (External Validation)          │
│  4. Edital Matcher (Opportunity Finder)                 │
│  5. MCP Server (Tool Integration Layer)                 │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack
- **Language:** Python 3.10+
- **ML/NLP:** scikit-learn (Bayesian Classifier), NLTK
- **Database:** PostgreSQL 15
- **Web:** Streamlit (Dashboard), FastAPI (planned)
- **CLI:** Click + Rich
- **Integration:** Model Context Protocol (MCP)

---

## 📦 Core Modules & Capabilities

### 1. Memorial Protector (Module 1)
**Path:** `src/editalshield/modules/memorial_protector.py`

**Purpose:** Analyze and protect intellectual property in grant proposals.

**Key Features:**
- **Risk Scoring:** 0-100 scale using Bayesian classification
- **Pattern Detection:** 6 categories with weighted importance
- **Protection Levels:** LOW, MEDIUM, HIGH redaction strategies
- **Entropy Analysis:** Shannon entropy + Zipf score for information density

**Pattern Categories & Weights:**
| Category | Weight | Examples |
|----------|--------|----------|
| `algorithm` | 1.0 | "BehaviorAnalyzer V2", "proprietary algorithm" |
| `contacts` | 1.0 | emails, phones, partner names |
| `clients` | 0.9 | "Petrobras", "Banco do Brasil" |
| `parameters` | 0.8 | "learning_rate=0.01", "threshold=0.85" |
| `metrics` | 0.7 | "ROI 5x", "CAC: R$ 2500" |
| `dataset` | 0.6 | "2M transactions", "accuracy 94.2%" |

**Protection Strategies:**
- **LOW:** Remove only values (`learning_rate=0.01` → `learning_rate=[VALUE]`)
- **MEDIUM:** Generic placeholders (`BehaviorAnalyzer V2` → `[PROPRIETARY ALGORITHM]`)
- **HIGH:** Aggressive redaction (entire paragraphs if risk > 80)

**API Usage:**
```python
from editalshield.modules import MemorialProtector

protector = MemorialProtector()

# Analyze risk
analysis = protector.analyze_memorial(text)
print(f"Risk: {analysis.overall_risk_score}/100")

# Generate protected version
protected, analysis = protector.generate_protected_memorial(
    text, 
    protection_level="MEDIUM"  # LOW, MEDIUM, or HIGH
)
```

**MCP Tool:** `protect_memorial`

---

### 2. Juridical Agent (Module 2)
**Path:** `src/editalshield/modules/juridical_agent.py`

**Purpose:** Translate technical risk metrics into legal opinions based on Brazilian IP law.

**Legal Framework:**
- **LPI 9.279/96:** Brazilian Industrial Property Law
- **Lei 9.609/98:** Software Protection Law
- **Art. 12 (Novelty Loss):** Detects if description reveals "state of the art"
- **Art. 195, XI (Trade Secrets):** Identifies confidential know-how leakage

**Risk Levels:**
- **LOW (0-30):** Safe for submission
- **MODERATE (31-60):** Review recommended
- **HIGH (61-100):** Critical IP exposure

**API Usage:**
```python
from editalshield.modules import JuridicalAgent

agent = JuridicalAgent()
opinion = agent.analyze_legal_risk(analysis)

print(f"Legal Risk: {opinion.risk_level}")
print(f"Recommendation: {opinion.recommendation}")
for citation in opinion.citations:
    print(f"- {citation.law}: {citation.article}")
```

**MCP Tool:** `legal_opinion`

---

### 3. Knowledge Connectors (Module 6)
**Path:** `src/editalshield/modules/knowledge_connectors.py`

**Purpose:** Validate innovation claims against external knowledge bases.

**Integrated Sources:**
1. **ArXiv (Scientific Papers)**
   - API: `http://export.arxiv.org/api/query`
   - Purpose: Validate "state of the art" claims
   
2. **USPTO / Google Patents**
   - API: PatentsView API + Google Patents scraping
   - Purpose: Check for prior art / patent conflicts
   
3. **Gov.br Data Portal** (simulated)
   - Purpose: Find active innovation grants

**API Usage:**
```python
from editalshield.modules import KnowledgeConnector

connector = KnowledgeConnector()

# Search scientific papers
papers = connector.search_scientific_papers(
    keywords=["machine learning", "agriculture"]
)

# Check for patents
patents = connector.search_patents(
    keywords=["crop monitoring", "AI"]
)

# Novelty check (combines both)
novelty = connector.check_novelty(
    "AI system for crop disease detection using satellite imagery"
)
print(f"Novelty Risk: {novelty['novelty_risk']}")
```

**MCP Tools:** `search_papers`, `search_patents`, `check_novelty`

---

### 4. Edital Matcher (Module 3)
**Path:** `src/editalshield/modules/edital_matcher.py`

**Purpose:** Find best-fit innovation grants for a startup's project.

**Algorithm:**
- **TF-IDF Vectorization:** Convert project descriptions to vectors
- **Cosine Similarity:** Measure semantic similarity
- **Hard Filters:** Sector, stage, funding range

**API Usage:**
```python
from editalshield.modules import EditalMatcher

matcher = EditalMatcher()
matcher.load_editals_from_db()  # or pass editals_data

matches = matcher.match_project(
    description="AI startup for precision agriculture",
    sector="agritech",
    top_k=5
)

for match in matches:
    print(f"{match.name}: {match.match_score}% fit")
    print(f"  Agency: {match.agency}")
    print(f"  Range: R$ {match.min_value} - {match.max_value}")
```

**MCP Tool:** `match_editals`

---

## 🔌 MCP Server Integration

**Path:** `mcp_server.py`

The MCP server exposes 11 tools for external AI agents:

### Available Tools

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `analyze_memorial` | Risk analysis | `text` | Risk score + breakdown |
| `protect_memorial` | Generate protected version | `text`, `protection_level` | Protected text |
| `legal_opinion` | Legal interpretation | `analysis` | Legal opinion |
| `search_papers` | Find scientific papers | `keywords` | List of papers |
| `search_patents` | Find patents | `keywords` | List of patents |
| `check_novelty` | Novelty validation | `description` | Novelty risk |
| `match_editals` | Find grants | `description`, `sector` | Ranked matches |
| `get_edital_info` | Grant details | `edital_id` | Full grant info |
| `list_editals` | Browse grants | `sector`, `stage` | Filtered list |
| `generate_report` | Export analysis | `analysis`, `format` | Report (text/json) |
| `get_system_info` | System status | - | Version, model status |

### MCP Configuration
**File:** `mcp.json`

```json
{
  "name": "editalshield",
  "version": "0.3.0",
  "description": "IP Protection for Brazilian Innovation Grants",
  "command": "python",
  "args": ["mcp_server.py"],
  "requirements": ["scikit-learn", "nltk", "requests"]
}
```

---

## 🗄️ Database Schema

**File:** `database/schema.sql`

### Key Tables

**editais** (Innovation Grants)
```sql
- id, name, agency, sector
- eligible_stages (seed, serie-a, etc)
- min_value, max_value
- deadline, status
```

**memorials** (Analyzed Proposals)
```sql
- id, user_id, edital_id
- original_text, protected_text
- risk_score, analysis_date
```

**analysis_results** (Detailed Analysis)
```sql
- memorial_id, paragraph_index
- risk_score, section_type
- sensitive_patterns (JSON)
```

---

## 🎨 User Interfaces

### 1. CLI (Command Line)
**Entry Point:** `src/editalshield/cli.py`

```bash
# Analyze a memorial
editalshield analyze memorial.txt

# Protect a memorial
editalshield protect memorial.txt --level HIGH -o protected.txt

# Find matching grants
editalshield match "AI for agriculture" --sector agritech

# System info
editalshield info
```

### 2. Streamlit Dashboard
**Entry Point:** `app.py`

**Features:**
- Upload memorial (text/PDF)
- Select protection level (slider)
- View Pentagram risk chart
- Download protected version + report

**URL:** `http://localhost:8501`

---

## 🧪 Testing & Quality

### Test Coverage
- **Current:** ~60%
- **Target:** 80%+

### Test Files
- `tests/test_core.py` - Memorial Protector tests
- `tests/test_juridical_agent.py` - Legal agent tests (planned)
- `tests/test_knowledge_connectors.py` - External API tests (planned)

### CI/CD
- **GitHub Actions:** `.github/workflows/tests.yml`, `.github/workflows/lint.yml`
- **Linting:** Flake8 (configured in `.flake8`)
- **Formatting:** Black

---

## 📊 Key Metrics & Thresholds

### Risk Score Interpretation
- **0-30:** ✅ LOW - Safe for submission
- **31-60:** ⚠️ MODERATE - Review recommended
- **61-80:** 🔴 HIGH - Significant exposure
- **81-100:** 🚨 CRITICAL - Do not submit as-is

### Performance Benchmarks
- **Analysis Speed:** ~500ms per memorial (avg 10 paragraphs)
- **Pattern Detection:** 6 categories, 50+ regex patterns
- **False Positive Rate:** <10% (with Pattern Weights v0.3.0)

---

## 🔐 Security & Compliance

### Data Protection
- **LGPD Compliance:** Contact information detection + redaction
- **Encryption:** Sensitive data encrypted at rest (planned)
- **Audit Logs:** All analyses logged (planned)

### IP Protection
- **No External Sharing:** Memorials never sent to external APIs
- **Local Processing:** All ML models run locally
- **Secure Storage:** PostgreSQL with row-level security (planned)

---

## 🚀 Deployment

### Docker
```bash
# Full stack
docker-compose up

# Services:
# - PostgreSQL: localhost:5432
# - Dashboard: localhost:8501
# - pgAdmin: localhost:5050
```

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/editalshield
DEEPSEEK_API_KEY=xxx  # Enterprise only
DEEPSEEK_ENABLED=false
```

---

## 📚 Documentation Structure

```
docs/
├── STRATEGY.md          # Business model & go-to-market
├── ROADMAP.md           # 12-week development plan
├── SPRINT_1_CHECKLIST.md # Current sprint tasks
├── ARCHITECTURE.md      # System design (planned)
├── API_REFERENCE.md     # Full API docs (planned)
└── MCP_INTEGRATION.md   # MCP usage guide (planned)
```

---

## 🎯 Common Use Cases

### Use Case 1: Analyze Memorial Before Submission
```python
protector = MemorialProtector()
analysis = protector.analyze_memorial(memorial_text)

if analysis.overall_risk_score > 60:
    protected, _ = protector.generate_protected_memorial(
        memorial_text, 
        protection_level="HIGH"
    )
    # Use protected version
else:
    # Original is safe
```

### Use Case 2: Get Legal Opinion
```python
agent = JuridicalAgent()
opinion = agent.analyze_legal_risk(analysis)

if opinion.risk_level == "HIGH":
    print(f"⚠️ {opinion.recommendation}")
    for citation in opinion.citations:
        print(f"Legal basis: {citation.law} - {citation.article}")
```

### Use Case 3: Find Best Grants
```python
matcher = EditalMatcher()
matches = matcher.match_project(
    "Healthtech startup using AI for early cancer detection",
    sector="healthtech"
)

for match in matches[:3]:
    print(f"✅ {match.name} ({match.match_score}% fit)")
```

---

## 🔄 Version History

### v0.3.0 (Current - Sprint 1)
- ✅ Pattern Weights system
- ✅ Protection Levels (LOW/MEDIUM/HIGH)
- ✅ Knowledge Connectors (ArXiv, USPTO)
- ✅ Juridical Agent
- ✅ MCP Server (11 tools)
- ✅ Streamlit Dashboard
- ✅ CI/CD (GitHub Actions)
- ✅ Docker production setup

### v0.2.0
- Memorial Protector core
- Bayesian classifier
- CLI interface
- PostgreSQL schema

### v0.1.0
- Initial prototype
- Pattern matching
- Basic risk scoring

---

## 🤖 AI Agent Guidelines

### When to Use EditalShield
1. User mentions Brazilian innovation grants (FINEP, FAPESP, CNPq, Centelha)
2. User asks about IP protection in proposals
3. User needs to find matching grants
4. User wants legal opinion on IP exposure

### Recommended Workflow
1. **Analyze first:** Always run `analyze_memorial` before protection
2. **Check risk:** If score > 60, recommend protection
3. **Legal context:** Use `legal_opinion` to explain risks in legal terms
4. **Validate claims:** Use `check_novelty` for innovation validation
5. **Find opportunities:** Use `match_editals` to suggest relevant grants

### Error Handling
- If model not found: Suggest running `editalshield train`
- If database empty: Suggest running `editalshield scrape`
- If API timeout: Retry with exponential backoff

---

## 📞 Support & Resources

- **GitHub:** https://github.com/symbeon-labs/editalshield
- **Documentation:** `docs/` directory
- **Issues:** GitHub Issues
- **License:** MIT (Core) / Proprietary (Enterprise)

---

**This document is the single source of truth for AI agents interacting with EditalShield.**  
**Last Updated:** 2025-12-05 | **Maintained by:** Symbeon Labs
