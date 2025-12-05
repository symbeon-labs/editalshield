"""
EditalShield - Knowledge Connectors (Module 6)
Connects the agent to external data sources (GovData, INPI, ArXiv).
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from dataclasses import dataclass
import random
from datetime import datetime, timedelta

@dataclass
class ExternalResource:
    source: str
    title: str
    url: str
    date: str
    relevance: float
    summary: str

class KnowledgeConnector:
    """
    Hub for external data connections.
    """
    
    def __init__(self):
        self.arxiv_api_url = "http://export.arxiv.org/api/query"
        self.gov_data_url = "https://dados.gov.br/api/publico/conjuntos-dados"

    def search_scientific_papers(self, keywords: List[str], max_results: int = 3) -> List[ExternalResource]:
        """
        Searches ArXiv for scientific papers to validate state-of-the-art.
        REAL IMPLEMENTATION using ArXiv Public API.
        """
        query = "+AND+".join(keywords)
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        
        try:
            response = requests.get(self.arxiv_api_url, params=params, timeout=10)
            if response.status_code != 200:
                return []
                
            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            resources = []
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')[:200] + "..."
                url = entry.find('atom:id', ns).text
                published = entry.find('atom:published', ns).text[:10]
                
                resources.append(ExternalResource(
                    source="ArXiv (Science)",
                    title=title,
                    url=url,
                    date=published,
                    relevance=0.9, # ArXiv returns sorted by relevance
                    summary=summary
                ))
            return resources
            
        except Exception as e:
            print(f"Error connecting to ArXiv: {e}")
            return []

    def search_patents(self, keywords: List[str]) -> List[ExternalResource]:
        """
        Performs REAL patent search using:
        1. USPTO API (PatentsView) - Official US Patents
        2. Google Patents (Scraping) - Global Patents
        """
        results = []
        
        # 1. USPTO Search (PatentsView API)
        try:
            # Construct query for title or abstract
            query_parts = []
            for k in keywords:
                if len(k) > 3: # Filter small words
                    query_parts.append(f'{{"_text_any": {{"patent_title": "{k}"}}}}')
                    query_parts.append(f'{{"_text_any": {{"patent_abstract": "{k}"}}}}')
            
            if query_parts:
                query = f'{{"_or": [{",".join(query_parts)}]}}'
                url = "https://api.patentsview.org/patents/query"
                params = {
                    "q": query,
                    "f": '["patent_title", "patent_date", "patent_abstract", "patent_number"]',
                    "o": '{"per_page": 3}'
                }
                
                resp = requests.get(url, params=params, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    for pat in data.get('patents', [])[:3]:
                        results.append(ExternalResource(
                            source="USPTO (US Patents)",
                            title=pat.get('patent_title', 'Unknown'),
                            url=f"https://patents.google.com/patent/US{pat.get('patent_number')}",
                            date=pat.get('patent_date', ''),
                            relevance=0.95,
                            summary=pat.get('patent_abstract', '')[:200] + "..."
                        ))
        except Exception as e:
            print(f"USPTO Search Error: {e}")

        # 2. Google Patents Scraping (Fallback/Complementary)
        try:
            from bs4 import BeautifulSoup
            
            # Search query construction
            q = "+".join(keywords)
            url = f"https://patents.google.com/?q={q}&oq={q}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                # Google Patents structure (may change, so we use generic selectors)
                articles = soup.find_all('article', limit=3)
                
                for art in articles:
                    title_el = art.find('h3') or art.find('span', {'id': 'htmlContent'})
                    link_el = art.find('a', href=True)
                    
                    if link_el and link_el['href'].startswith('/patent/'):
                        title = link_el.get_text().strip()
                        link = f"https://patents.google.com{link_el['href']}"
                        
                        # Avoid duplicates from USPTO
                        if not any(r.url == link for r in results):
                            results.append(ExternalResource(
                                source="Google Patents (Global)",
                                title=title,
                                url=link,
                                date="Unknown", # Hard to parse from list view reliably
                                relevance=0.8,
                                summary="Patent found via global search."
                            ))
        except Exception as e:
            print(f"Google Patents Scraping Error: {e}")
            
        return results

    def fetch_gov_grants(self, sector: str = None) -> List[ExternalResource]:
        """
        Simulates fetching active grants from Portal de Dados Abertos.
        """
        # In a real production env, we would scrape 'https://www.gov.br/mcti/pt-br'
        # Here we return realistic mock data for the demo
        
        grants = [
            ExternalResource(
                source="Portal Gov.br",
                title="Edital FINEP Inovação 2025 - Fluxo Contínuo",
                url="http://www.finep.gov.br/chamadas-publicas",
                date="2025-01-15",
                relevance=1.0,
                summary="Seleção pública de propostas para apoio financeiro a projetos de inovação."
            ),
            ExternalResource(
                source="CNPq",
                title="Chamada Universal CNPq/MCTI Nº 10/2025",
                url="http://memoria.cnpq.br/chamadas-publicas",
                date="2025-02-01",
                relevance=0.9,
                summary="Apoio a projetos de pesquisa científica e tecnológica em qualquer área."
            )
        ]
        
        if sector and sector.lower() == 'agritech':
            grants.append(ExternalResource(
                source="Embrapa",
                title="Edital Inova Agro 4.0",
                url="https://www.embrapa.br/editais",
                date="2025-03-10",
                relevance=0.95,
                summary="Fomento para startups com soluções de IoT e IA para o campo."
            ))
            
        return grants

    def check_novelty(self, description: str) -> Dict[str, Any]:
        """
        Performs a 'Novelty Check' by aggregating Science and Patent searches.
        """
        # Extract keywords (simple heuristic)
        keywords = [w for w in description.split() if len(w) > 5][:3]
        
        papers = self.search_scientific_papers(keywords)
        patents = self.search_patents(keywords)
        
        risk_level = "LOW"
        if patents:
            risk_level = "HIGH (Patent Conflict)"
        elif papers:
            risk_level = "MODERATE (Prior Art Found)"
            
        return {
            "novelty_risk": risk_level,
            "scientific_matches": [r.__dict__ for r in papers],
            "patent_matches": [r.__dict__ for r in patents]
        }
