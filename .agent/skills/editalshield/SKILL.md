# 🛡️ EditalShield: Opportunity Engine

---
name: editalshield
description: Semantic search and project-to-grant matching logic.
---

## 1. Engine Mission (OPPORTUNITY)
The mission of **EditalShield** is to identify the best funding opportunities (editals, grants, incentives) for a given project description and ensure the project aligns with the rules of the funding body.

## 2. Core Technical Domain
- **Semantic Search**: Utilizing vector embeddings to match natural language project intents with structured edital requirements.
- **Rules Mapping**: Extracting eligibility criteria, mandatory documents, and scoring metrics from PDFs/DOCX.
- **Scoring Algorithm**: Ranking opportunities based on technical compatibility, sector, and stage.

## 3. Key Directives
- **Accuracy First**: Only suggest matches with >70% technical compatibility.
- **Data Integrity**: Always reference the official source of the edital.
- **Clarity**: Highlight precisely *why* a project matches or fails a specific requirement (Gaps).

## 4. Interaction Protocol
- **Input**: Natural language intent + project phase (MVP, Scale, etc.).
- **Output**: JSON list of ranked opportunities + Gap Analysis.
- **Handoff**: Sends matched project to **Themis** for validation.

## 5. Knowledge Path
- Core Logic: `engines/L3-Public/editalshield/src/`
- Data Sources: `engines/L3-Public/editalshield/data/editals/`

---
**Component**: OPPORTUNITY
**Architecture Layer**: L3-Public
