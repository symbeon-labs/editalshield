# EditalShield MCP Integration

## Overview

EditalShield provides a **Model Context Protocol (MCP)** server that allows any AI agent or IDE to use its IP protection capabilities autonomously.

## Quick Start

### 1. Install MCP package

```bash
pip install mcp
```

### 2. Run the MCP server

```bash
python mcp_server.py
```

### 3. Configure your AI agent/IDE

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "editalshield": {
      "command": "python",
      "args": ["path/to/editalshield/mcp_server.py"]
    }
  }
}
```

## Available Tools

### 🎯 match_project

Find the best matching innovation grants (editals) for a project.

**Input:**
```json
{
  "description": "Startup developing AI for agritech...",
  "sector": "agritech"
}
```

**Output:**
```json
{
  "status": "success",
  "matches_found": 5,
  "top_matches": [
    {
      "name": "Centelha SP",
      "score": 85.5,
      "value_range": [50000, 100000],
      "reason": "High compatibility with agritech sector"
    }
  ]
}
```

### 🔍 analyze_memorial

Analyze a technical memorial for IP exposure risk.

**Input:**
```json
{
  "text": "Your memorial text here..."
}
```

**Output:**
```json
{
  "status": "success",
  "overall_risk_score": 67,
  "total_paragraphs": 12,
  "high_risk_paragraphs": 3,
  "risk_level": "HIGH - Significant IP exposure",
  "paragraphs": [...]
}
```

### 🛡️ protect_memorial

Automatically protect a memorial by replacing sensitive content.

**Input:**
```json
{
  "text": "Memorial with sensitive content..."
}
```

**Output:**
```json
{
  "status": "success",
  "protected_text": "Memorial with [PROTECTED] content...",
  "original_risk_score": 85,
  "paragraphs_modified": 5,
  "patterns_replaced": 12
}
```

### 📊 analyze_paragraph

Analyze a single paragraph for IP exposure.

**Input:**
```json
{
  "text": "Single paragraph to analyze..."
}
```

**Output:**
```json
{
  "status": "success",
  "risk_score": 75,
  "section_type": "technical",
  "entropy": 3.45,
  "sensitive_patterns": ["BehaviorAnalyzer V2", "W=0.7"],
  "suggestions": ["Replace with generic algorithm name"]
}
```

### 🔎 detect_sensitive_patterns

Scan text for sensitive patterns.

**Input:**
```json
{
  "text": "Text to scan..."
}
```

**Output:**
```json
{
  "status": "success",
  "patterns_found": {
    "algorithm": ["SmartAnalyzer V3"],
    "parameters": ["threshold=0.85"],
    "contacts": ["email@domain.com"]
  },
  "total_patterns": 3
}
```

### 📐 calculate_entropy

Calculate Shannon entropy of text.

**Input:**
```json
{
  "text": "Text to measure..."
}
```

**Output:**
```json
{
  "status": "success",
  "entropy": 4.2,
  "entropy_normalized": 0.65,
  "interpretation": "High information density - potentially sensitive"
}
```

### 📋 generate_report

Generate a detailed analysis report.

**Input:**
```json
{
  "text": "Memorial text...",
  "format": "text"
}
```

**Output:**
```json
{
  "status": "success",
  "report": "======== EDITALSHIELD REPORT ========\n...",
  "format": "text"
}
```

### 💡 get_protection_suggestions

Get suggestions for protecting sensitive content.

**Input:**
```json
{
  "categories": ["algorithm", "parameters", "contacts"]
}
```

**Output:**
```json
{
  "status": "success",
  "suggestions": {
    "algorithm": "Replace with: 'proprietary algorithm developed internally'",
    "parameters": "Remove specific values, use: 'empirically optimized parameters'",
    "contacts": "Remove personal contact information"
  }
}
```

### ⚖️ compare_risk

Compare risk between original and protected versions.

**Input:**
```json
{
  "original": "Original text with IP...",
  "protected": "Protected text..."
}
```

**Output:**
```json
{
  "status": "success",
  "original_risk": 85,
  "protected_risk": 15,
  "risk_reduction": 70,
  "risk_reduction_percent": 82.4,
  "protection_effective": true
}
```

## Resources

The MCP server exposes these resources:

| URI | Description |
|-----|-------------|
| `editalshield://info` | EditalShield capabilities and version info |
| `editalshield://patterns` | List of all sensitive patterns detected |
| `editalshield://suggestions` | Protection suggestions by category |

## Example Usage with AI Agent

```python
# Example: AI agent using EditalShield MCP

# 1. Agent receives a memorial to review
memorial = user_input

# 2. Agent calls analyze_memorial
result = await mcp.call_tool("analyze_memorial", {"text": memorial})

# 3. If risk is high, agent protects it
if result["overall_risk_score"] > 50:
    protected = await mcp.call_tool("protect_memorial", {"text": memorial})
    
    # 4. Compare results
    comparison = await mcp.call_tool("compare_risk", {
        "original": memorial,
        "protected": protected["protected_text"]
    })
    
    # 5. Report to user
    print(f"Risk reduced by {comparison['risk_reduction_percent']}%")
```

## IDE Configuration

### VS Code with Claude Extension

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "editalshield": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

### Cursor IDE

Add to Cursor settings:

```json
{
  "ai.mcpServers": {
    "editalshield": {
      "command": "python",
      "args": ["path/to/mcp_server.py"]
    }
  }
}
```

## Sensitive Pattern Categories

| Category | Examples | Replacement |
|----------|----------|-------------|
| `algorithm` | BehaviorAnalyzer V2 | [PROPRIETARY ALGORITHM] |
| `parameters` | W=0.7, threshold=0.8 | [OPTIMIZED PARAMETERS] |
| `dataset` | 2M records, 94.2% accuracy | [REPRESENTATIVE DATABASE] |
| `contacts` | emails, phone numbers | [CONTACT OMITTED] |
| `metrics` | ROI 5x, CAC: R$ 2500 | [CONFIDENTIAL METRICS] |
| `clients` | Specific company names | [STRATEGIC CLIENTS] |

## Error Handling

All tools return structured responses:

```json
{
  "status": "success" | "error",
  "message": "Error description if status is error",
  ...
}
```

## License

MIT License - See [LICENSE](LICENSE) for details.
