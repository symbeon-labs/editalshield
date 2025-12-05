"""
EditalShield - Edital Matcher (Module 1)
Matches startup projects with the best innovation grants using TF-IDF and Cosine Similarity
"""

import json
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class MatchResult:
    edital_id: int
    name: str
    agency: str
    match_score: float
    relevance_reason: str
    min_value: float
    max_value: float
    deadline: str = "N/A"


class EditalMatcher:
    """
    Matches a project description against a database of editals.
    Uses TF-IDF for semantic matching and hard filters for eligibility.
    """

    def __init__(self, editals_data: List[Dict] = None):
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )  # In production, use Portuguese stop words
        self.editals = editals_data or []
        self.tfidf_matrix = None

        if self.editals:
            self._prepare_corpus()

    def load_editals_from_db(self, connection_string: str = None):
        """Load editals from database (mocked for now if no DB connection)"""
        # In a real scenario, we would query PostgreSQL here
        # For now, we'll try to load from the JSON file we scraped
        try:
            import os
            import glob

            # Find latest real editals file
            files = glob.glob("data/editais_reais_*.json")
            if not files:
                # Fallback to synthetic
                files = ["data/synthetic_dataset.json"]

            if files:
                latest = max(files, key=os.path.getctime)
                with open(latest, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if "editals" in data:  # Synthetic format
                    self.editals = data["editals"]
                else:  # Real scraper format is a list
                    self.editals = data

                self._prepare_corpus()
                print(f"[✓] Loaded {len(self.editals)} editals for matching")
            else:
                print("[!] No edital data found. Run 'editalshield scrape' or 'generate' first.")

        except Exception as e:
            print(f"[!] Error loading editals: {e}")

    def _prepare_corpus(self):
        """Prepare text corpus for TF-IDF"""
        self.corpus = []
        for e in self.editals:
            # Combine relevant fields for text matching
            text = f"{e.get('name', '')} {e.get('agency', '')} "
            text += " ".join(e.get("eligible_sectors", []))
            text += " ".join(e.get("eligible_stages", []))

            # Add criteria if available
            criteria = e.get("criteria", {})
            if isinstance(criteria, dict):
                text += " ".join(criteria.keys())

            self.corpus.append(text)

        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def match_project(
        self, project_description: str, sector: str = None, stage: str = None, top_k: int = 5
    ) -> List[MatchResult]:
        """
        Find best matching editals for a project.

        Args:
            project_description: Text describing the startup/project
            sector: Optional hard filter (e.g., 'agritech')
            stage: Optional hard filter (e.g., 'seed')
            top_k: Number of results to return

        Returns:
            List of MatchResult objects sorted by score
        """
        if not self.editals or self.tfidf_matrix is None:
            return []

        # 1. Text Matching (Soft Filter)
        project_vector = self.vectorizer.transform([project_description])
        cosine_sims = cosine_similarity(project_vector, self.tfidf_matrix).flatten()

        results = []

        for i, score in enumerate(cosine_sims):
            edital = self.editals[i]

            # 2. Hard Filters (Eligibility)
            if sector:
                eligible_sectors = [s.lower() for s in edital.get("eligible_sectors", [])]
                if eligible_sectors and sector.lower() not in eligible_sectors:
                    continue  # Skip if sector doesn't match

            if stage:
                eligible_stages = [s.lower() for s in edital.get("eligible_stages", [])]
                if eligible_stages and stage.lower() not in eligible_stages:
                    continue  # Skip if stage doesn't match

            # 3. Boost score based on agency or value (Heuristics)
            final_score = score * 100

            # Boost for exact sector match in text
            if sector and sector.lower() in str(edital).lower():
                final_score += 10

            results.append(
                MatchResult(
                    edital_id=i,
                    name=edital.get("name", "Unknown"),
                    agency=edital.get("agency", "Unknown"),
                    match_score=round(final_score, 1),
                    relevance_reason=self._generate_reason(final_score, edital),
                    min_value=edital.get("min_value", 0),
                    max_value=edital.get("max_value", 0),
                )
            )

        # Sort by score descending
        results.sort(key=lambda x: x.match_score, reverse=True)

        return results[:top_k]

    def _generate_reason(self, score: float, edital: Dict) -> str:
        """Generate a human-readable reason for the match"""
        sectors = ", ".join(edital.get("eligible_sectors", [])[:2])
        if score > 50:
            return f"Alta compatibilidade com setor ({sectors}) e perfil da agência."
        elif score > 20:
            return f"Compatibilidade média. Verifique requisitos de {sectors}."
        else:
            return "Compatibilidade baixa, mas pode ser elegível."


# ============================================================================
# CLI Integration Helper
# ============================================================================


def find_opportunities(description: str, sector: str = None):
    """Helper for CLI usage"""
    matcher = EditalMatcher()
    matcher.load_editals_from_db()

    matches = matcher.match_project(description, sector=sector)

    return matches


if __name__ == "__main__":
    # Test
    matcher = EditalMatcher()
    matcher.load_editals_from_db()

    print("\n--- Test Matching ---")
    project = (
        "Desenvolvimento de software de IA para monitoramento de pragas em soja usando drones."
    )
    print(f"Project: {project}")

    matches = matcher.match_project(project, sector="agritech")

    for m in matches:
        print(f"\n[{m.match_score:.1f}%] {m.name} ({m.agency})")
        print(f"   Value: R$ {m.min_value:,.2f} - {m.max_value:,.2f}")
        print(f"   Why: {m.relevance_reason}")
