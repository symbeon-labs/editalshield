"""
EditalShield MCP Server
Model Context Protocol server for AI agent integration
Allows any AI agent or IDE to use EditalShield autonomously
"""

import json
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Tool,
        TextContent,
        Resource,
        ResourceTemplate,
    )
except ImportError:
    print("MCP not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

from editalshield.modules.memorial_protector import MemorialProtector, MemorialAnalysis
from editalshield.modules.edital_matcher import EditalMatcher


# Initialize MCP Server
server = Server("editalshield")

# Initialize modules
protector = MemorialProtector()
matcher = EditalMatcher()
matcher.load_editals_from_db()


# ============================================================================
# TOOLS
# ============================================================================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available EditalShield tools"""
    return [
        Tool(
            name="match_project",
            description="""Find the best matching innovation grants (editals) for a project.
            
Uses TF-IDF and Cosine Similarity to compare project description against database.
Returns a ranked list of opportunities with compatibility scores and reasons.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description of the startup or project"
                    },
                    "sector": {
                        "type": "string",
                        "description": "Optional sector filter (e.g. agritech, healthtech)"
                    }
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="analyze_memorial",
            description="""Analyze a technical memorial for intellectual property exposure risk.
            
Returns:
- Overall risk score (0-100)
- High/medium/low risk paragraph counts
- Detailed analysis per paragraph
- Sensitive patterns detected
- Protection suggestions

Use this to evaluate if a memorial is safe to submit to innovation grants.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The memorial text to analyze"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="protect_memorial",
            description="""Protect a technical memorial by replacing sensitive IP content.
            
Automatically replaces:
- Algorithm names with generic terms
- Specific parameters with ranges
- Client names with "[STRATEGIC CLIENTS]"
- Contact information with "[CONTACT OMITTED]"
- Specific metrics with ranges

Returns the protected text and analysis.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The memorial text to protect"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="analyze_paragraph",
            description="""Analyze a single paragraph for IP exposure risk.
            
Returns:
- Risk score (0-100)
- Section type (technical, market, team, admin)
- Entropy value
- Sensitive patterns found
- Protection suggestions""",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The paragraph text to analyze"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="detect_sensitive_patterns",
            description="""Detect sensitive patterns in text that could expose IP.
            
Categories detected:
- algorithm: Proprietary algorithm names
- parameters: Specific parameter values
- dataset: Dataset sizes and accuracies
- contacts: Emails, phone numbers, names
- metrics: ROI, CAC, LTV values
- clients: Specific client names""",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to scan for sensitive patterns"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="calculate_entropy",
            description="""Calculate Shannon entropy of text.
            
Shannon entropy measures information density.
Higher entropy = more unique information = potentially more IP exposure.

Returns:
- entropy: Raw entropy value
- entropy_normalized: Normalized to [0, 1] range""",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to calculate entropy for"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="generate_report",
            description="""Generate a detailed analysis report for a memorial.
            
Formats available:
- text: Human-readable text report
- json: Machine-readable JSON format

The report includes:
- Summary statistics
- Risk assessment
- High-risk paragraph details
- Protection recommendations""",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Memorial text to generate report for"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "default": "text",
                        "description": "Report format"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="get_protection_suggestions",
            description="""Get protection suggestions for detected sensitive patterns.
            
Returns category-specific suggestions for how to rewrite
sensitive content in a safer way while maintaining clarity.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Categories to get suggestions for: algorithm, parameters, dataset, contacts, metrics, clients"
                    }
                },
                "required": ["categories"]
            }
        ),
        Tool(
            name="compare_risk",
            description="""Compare risk scores between original and protected versions.
            
Useful for validating that protection was effective.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "original": {
                        "type": "string",
                        "description": "Original memorial text"
                    },
                    "protected": {
                        "type": "string",
                        "description": "Protected memorial text"
                    }
                },
                "required": ["original", "protected"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute an EditalShield tool"""
    
    try:
        if name == "match_project":
            description = arguments.get("description", "")
            sector = arguments.get("sector")
            
            matches = matcher.match_project(description, sector=sector)
            
            result = {
                "status": "success",
                "matches_found": len(matches),
                "top_matches": [
                    {
                        "name": m.name,
                        "agency": m.agency,
                        "score": m.match_score,
                        "value_range": [m.min_value, m.max_value],
                        "reason": m.relevance_reason
                    }
                    for m in matches
                ]
            }

        elif name == "analyze_memorial":
            text = arguments.get("text", "")
            analysis = protector.analyze_memorial(text)
            
            result = {
                "status": "success",
                "overall_risk_score": analysis.overall_risk_score,
                "total_paragraphs": analysis.total_paragraphs,
                "high_risk_paragraphs": analysis.high_risk_paragraphs,
                "medium_risk_paragraphs": analysis.medium_risk_paragraphs,
                "low_risk_paragraphs": analysis.low_risk_paragraphs,
                "risk_level": get_risk_level(analysis.overall_risk_score),
                "paragraphs": [
                    {
                        "index": p.index,
                        "risk_score": p.risk_score,
                        "section_type": p.section_type,
                        "has_exposure": p.has_exposure,
                        "patterns_found": p.sensitive_patterns[:5],
                        "suggestions": p.suggestions[:2]
                    }
                    for p in analysis.paragraphs if p.risk_score >= 40
                ]
            }
            
        elif name == "protect_memorial":
            text = arguments.get("text", "")
            protected_text, analysis = protector.generate_protected_memorial(text)
            
            result = {
                "status": "success",
                "protected_text": protected_text,
                "original_risk_score": analysis.overall_risk_score,
                "paragraphs_modified": analysis.high_risk_paragraphs + analysis.medium_risk_paragraphs,
                "patterns_replaced": sum(len(p.sensitive_patterns) for p in analysis.paragraphs)
            }
            
        elif name == "analyze_paragraph":
            text = arguments.get("text", "")
            analysis = protector.analyze_paragraph(text, 0)
            
            result = {
                "status": "success",
                "risk_score": analysis.risk_score,
                "section_type": analysis.section_type,
                "entropy": analysis.entropy,
                "entropy_normalized": analysis.entropy_normalized,
                "has_exposure": analysis.has_exposure,
                "sensitive_patterns": analysis.sensitive_patterns,
                "suggestions": analysis.suggestions
            }
            
        elif name == "detect_sensitive_patterns":
            text = arguments.get("text", "")
            patterns = protector.detect_sensitive_patterns(text)
            
            result = {
                "status": "success",
                "patterns_found": patterns,
                "total_patterns": sum(len(v) for v in patterns.values()),
                "categories_with_patterns": list(patterns.keys())
            }
            
        elif name == "calculate_entropy":
            text = arguments.get("text", "")
            entropy, entropy_norm = protector.calculate_entropy(text)
            
            result = {
                "status": "success",
                "entropy": entropy,
                "entropy_normalized": entropy_norm,
                "interpretation": get_entropy_interpretation(entropy_norm)
            }
            
        elif name == "generate_report":
            text = arguments.get("text", "")
            format_type = arguments.get("format", "text")
            
            analysis = protector.analyze_memorial(text)
            report = protector.generate_report(analysis, format_type)
            
            result = {
                "status": "success",
                "report": report,
                "format": format_type
            }
            
        elif name == "get_protection_suggestions":
            categories = arguments.get("categories", [])
            
            suggestions = {}
            for cat in categories:
                if cat in protector.PROTECTION_SUGGESTIONS:
                    suggestions[cat] = protector.PROTECTION_SUGGESTIONS[cat]
            
            result = {
                "status": "success",
                "suggestions": suggestions
            }
            
        elif name == "compare_risk":
            original = arguments.get("original", "")
            protected = arguments.get("protected", "")
            
            original_analysis = protector.analyze_memorial(original)
            protected_analysis = protector.analyze_memorial(protected)
            
            reduction = original_analysis.overall_risk_score - protected_analysis.overall_risk_score
            reduction_pct = (reduction / max(original_analysis.overall_risk_score, 1)) * 100
            
            result = {
                "status": "success",
                "original_risk": original_analysis.overall_risk_score,
                "protected_risk": protected_analysis.overall_risk_score,
                "risk_reduction": round(reduction, 1),
                "risk_reduction_percent": round(reduction_pct, 1),
                "protection_effective": protected_analysis.overall_risk_score < original_analysis.overall_risk_score
            }
            
        else:
            result = {
                "status": "error",
                "message": f"Unknown tool: {name}"
            }
            
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
    except Exception as e:
        error_result = {
            "status": "error",
            "message": str(e)
        }
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]


# ============================================================================
# RESOURCES
# ============================================================================

@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available EditalShield resources"""
    return [
        Resource(
            uri="editalshield://info",
            name="EditalShield Info",
            description="Information about EditalShield and its capabilities",
            mimeType="application/json"
        ),
        Resource(
            uri="editalshield://patterns",
            name="Sensitive Patterns",
            description="List of all sensitive patterns that EditalShield detects",
            mimeType="application/json"
        ),
        Resource(
            uri="editalshield://suggestions",
            name="Protection Suggestions",
            description="Protection suggestions for each category",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read an EditalShield resource"""
    
    if uri == "editalshield://info":
        info = {
            "name": "EditalShield",
            "version": "0.2.0",
            "description": "Framework for protecting intellectual property in Brazilian innovation grant submissions",
            "capabilities": [
                "Analyze memorials for IP exposure risk",
                "Detect sensitive patterns (algorithms, parameters, contacts, etc)",
                "Calculate Shannon entropy for information density",
                "Generate protected versions of memorials",
                "Produce detailed analysis reports"
            ],
            "model": {
                "type": "Gaussian Naive Bayes",
                "auc": 1.0,
                "features": ["entropy", "patterns", "section_type"]
            }
        }
        return json.dumps(info, indent=2)
        
    elif uri == "editalshield://patterns":
        patterns = {
            category: patterns_list
            for category, patterns_list in protector.SENSITIVE_PATTERNS.items()
        }
        return json.dumps(patterns, indent=2)
        
    elif uri == "editalshield://suggestions":
        return json.dumps(protector.PROTECTION_SUGGESTIONS, indent=2)
        
    else:
        return json.dumps({"error": f"Unknown resource: {uri}"})


# ============================================================================
# HELPERS
# ============================================================================

def get_risk_level(score: float) -> str:
    """Get risk level description from score"""
    if score < 20:
        return "LOW - Safe to submit"
    elif score < 50:
        return "MEDIUM - Review recommended"
    elif score < 75:
        return "HIGH - Significant IP exposure"
    else:
        return "CRITICAL - Do not submit!"


def get_entropy_interpretation(entropy_norm: float) -> str:
    """Interpret normalized entropy value"""
    if entropy_norm < 0.3:
        return "Low information density - generic text"
    elif entropy_norm < 0.6:
        return "Medium information density - some unique content"
    else:
        return "High information density - potentially sensitive"


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
