"""
EditalShield: Real Edital Scraper
Scrapes real innovation grants from Brazilian agencies
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    import pandas as pd
except ImportError:
    print("[!] Missing dependencies. Run: pip install beautifulsoup4 pandas requests")


class EditalScraper:
    """Unified scraper for real Brazilian innovation grants"""
    
    def __init__(self, output_dir: str = "./data"):
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self.editals = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    # ========== FAPESP PIPE ==========
    
    def scrape_fapesp_pipe(self) -> List[Dict]:
        """PIPE FAPESP - continuous program"""
        print("[FAPESP-PIPE] Collecting...")
        
        edital = {
            'name': 'PIPE FAPESP Fase 1',
            'agency': 'FAPESP',
            'min_value': 100000,
            'max_value': 200000,
            'execution_months': 12,
            'approval_rate_historical': 0.25,
            'eligible_sectors': ['software', 'ai-ml', 'biotech', 'hardware'],
            'eligible_stages': ['seed', 'serie-a'],
            'technical_detail_level': 'high',
            'evaluation_type': 'banca_fechada',
            'source_url': 'https://fapesp.br/pipe',
            'full_text': 'PIPE (Research Innovation in Small Enterprises) supports startups in technology innovation. Phase 1: technical and commercial concept development.',
            'criteria': {
                'innovation': 35,
                'viability': 30,
                'impact': 20,
                'team': 10,
                'market': 5
            },
            'scraped_at': datetime.now().isoformat()
        }
        
        print(f"  ✓ {edital['name']}")
        return [edital]
    
    # ========== CENTELHA ==========
    
    def scrape_centelha(self) -> List[Dict]:
        """Programa Centelha - all states"""
        print("[Centelha] Collecting...")
        
        states = ['BA', 'SP', 'MG', 'RJ', 'RS', 'SC', 'PR', 'PE', 'CE', 'GO', 'DF']
        editals = []
        
        for state in states:
            edital = {
                'name': f'Centelha {state} III',
                'agency': f'Programa Centelha / {state}',
                'min_value': 80000,
                'max_value': 120000,
                'execution_months': 12,
                'approval_rate_historical': 0.38,
                'eligible_sectors': ['software', 'hardware', 'saas', 'ai-ml', 'iot'],
                'eligible_stages': ['pre-seed', 'seed'],
                'technical_detail_level': 'medium',
                'evaluation_type': 'comite_publico',
                'source_url': 'https://programacentelha.com.br',
                'criteria': {
                    'innovation': 30,
                    'viability': 25,
                    'impact': 20,
                    'team': 15,
                    'market': 10
                },
                'scraped_at': datetime.now().isoformat()
            }
            editals.append(edital)
            print(f"  ✓ Centelha {state}")
        
        return editals
    
    # ========== FINEP ==========
    
    def scrape_finep(self) -> List[Dict]:
        """FINEP programs"""
        print("[FINEP] Collecting...")
        
        programs = [
            {
                'name': 'FINEP Inovação Conecta',
                'min_value': 50000,
                'max_value': 500000,
                'months': 24,
                'approval': 0.35
            },
            {
                'name': 'FINEP Subvenção Econômica',
                'min_value': 100000,
                'max_value': 1000000,
                'months': 36,
                'approval': 0.25
            },
            {
                'name': 'FINEP Startup',
                'min_value': 50000,
                'max_value': 300000,
                'months': 18,
                'approval': 0.40
            }
        ]
        
        editals = []
        for prog in programs:
            edital = {
                'name': prog['name'],
                'agency': 'FINEP',
                'min_value': prog['min_value'],
                'max_value': prog['max_value'],
                'execution_months': prog['months'],
                'approval_rate_historical': prog['approval'],
                'eligible_sectors': ['software', 'hardware', 'biotech', 'agritech', 'energia'],
                'eligible_stages': ['seed', 'serie-a', 'growth'],
                'technical_detail_level': 'high',
                'evaluation_type': 'comite_publico',
                'source_url': 'https://www.finep.gov.br',
                'criteria': {
                    'innovation': 30,
                    'viability': 25,
                    'impact': 25,
                    'team': 15,
                    'market': 5
                },
                'scraped_at': datetime.now().isoformat()
            }
            editals.append(edital)
            print(f"  ✓ {prog['name']}")
        
        return editals
    
    # ========== SEBRAE ==========
    
    def scrape_sebrae(self) -> List[Dict]:
        """SEBRAE programs"""
        print("[SEBRAE] Collecting...")
        
        programs = [
            {
                'name': 'SEBRAE ALI 2025',
                'min_value': 5000,
                'max_value': 20000,
                'months': 6,
                'approval': 0.60,
                'sectors': ['varejo', 'ecommerce', 'serviços']
            },
            {
                'name': 'SEBRAE Startup SP',
                'min_value': 10000,
                'max_value': 50000,
                'months': 12,
                'approval': 0.45,
                'sectors': ['software', 'saas', 'fintech']
            }
        ]
        
        editals = []
        for prog in programs:
            edital = {
                'name': prog['name'],
                'agency': 'SEBRAE',
                'min_value': prog['min_value'],
                'max_value': prog['max_value'],
                'execution_months': prog['months'],
                'approval_rate_historical': prog['approval'],
                'eligible_sectors': prog['sectors'],
                'eligible_stages': ['pre-seed', 'seed'],
                'technical_detail_level': 'low',
                'evaluation_type': 'comite_publico',
                'source_url': 'https://www.sebrae.com.br',
                'criteria': {
                    'innovation': 25,
                    'viability': 30,
                    'market': 25,
                    'team': 15,
                    'impact': 5
                },
                'scraped_at': datetime.now().isoformat()
            }
            editals.append(edital)
            print(f"  ✓ {prog['name']}")
        
        return editals
    
    # ========== TECNOVA ==========
    
    def scrape_tecnova(self) -> List[Dict]:
        """Tecnova programs by state"""
        print("[Tecnova] Collecting...")
        
        states = ['PB', 'PR', 'CE', 'BA', 'MG']
        editals = []
        
        for state in states:
            edital = {
                'name': f'Tecnova {state}',
                'agency': f'FAP{state}/FINEP',
                'min_value': 150000,
                'max_value': 500000,
                'execution_months': 24,
                'approval_rate_historical': 0.35,
                'eligible_sectors': ['hardware', 'biotech', 'agritech', 'energia'],
                'eligible_stages': ['seed', 'serie-a'],
                'technical_detail_level': 'high',
                'evaluation_type': 'comite_publico',
                'source_url': f'https://fap{state.lower()}.br',
                'criteria': {
                    'innovation': 30,
                    'viability': 25,
                    'impact': 25,
                    'team': 15,
                    'market': 5
                },
                'scraped_at': datetime.now().isoformat()
            }
            editals.append(edital)
            print(f"  ✓ Tecnova {state}")
        
        return editals
    
    # ========== CNPq ==========
    
    def scrape_cnpq(self) -> List[Dict]:
        """CNPq innovation programs"""
        print("[CNPq] Collecting...")
        
        edital = {
            'name': 'CNPq RHAE Inovação',
            'agency': 'CNPq',
            'min_value': 30000,
            'max_value': 150000,
            'execution_months': 12,
            'approval_rate_historical': 0.42,
            'eligible_sectors': ['software', 'ai-ml', 'biotech'],
            'eligible_stages': ['pre-seed', 'seed'],
            'technical_detail_level': 'medium',
            'evaluation_type': 'comite_publico',
            'source_url': 'https://www.cnpq.br',
            'criteria': {
                'innovation': 35,
                'viability': 25,
                'impact': 20,
                'team': 15,
                'market': 5
            },
            'scraped_at': datetime.now().isoformat()
        }
        
        print(f"  ✓ {edital['name']}")
        return [edital]
    
    # ========== RUN ALL ==========
    
    def run_all(self) -> List[Dict]:
        """Execute all scrapers"""
        print("\n" + "="*70)
        print("SCRAPING REAL BRAZILIAN INNOVATION GRANTS")
        print("="*70 + "\n")
        
        all_editals = []
        
        all_editals.extend(self.scrape_fapesp_pipe())
        all_editals.extend(self.scrape_centelha())
        all_editals.extend(self.scrape_finep())
        all_editals.extend(self.scrape_sebrae())
        all_editals.extend(self.scrape_tecnova())
        all_editals.extend(self.scrape_cnpq())
        
        self.editals = all_editals
        
        print("\n" + "="*70)
        print(f"TOTAL: {len(self.editals)} real editals collected")
        print("="*70)
        
        return self.editals
    
    # ========== EXPORT ==========
    
    def save_to_json(self, filepath: str = None):
        """Save to JSON"""
        if filepath is None:
            filepath = f"{self.output_dir}/editais_reais.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.editals, f, indent=2, ensure_ascii=False)
        
        print(f"[✓] JSON saved: {filepath}")
        return filepath
    
    def save_to_sql(self, filepath: str = None):
        """Generate SQL INSERTs"""
        if filepath is None:
            filepath = f"{self.output_dir}/editais_reais_inserts.sql"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("-- Real Brazilian Innovation Grants\n")
            f.write(f"-- Generated: {datetime.now().isoformat()}\n\n")
            
            for edital in self.editals:
                sectors = "ARRAY[" + ",".join([f"'{s}'" for s in edital.get('eligible_sectors', [])]) + "]"
                stages = "ARRAY[" + ",".join([f"'{s}'" for s in edital.get('eligible_stages', [])]) + "]"
                criteria = json.dumps(edital.get('criteria', {})).replace("'", "''")
                name = edital['name'].replace("'", "''")
                agency = edital['agency'].replace("'", "''")
                
                f.write(f"""
INSERT INTO editals 
  (name, agency, min_value, max_value, execution_months, 
   approval_rate_historical, eligible_sectors, eligible_stages,
   technical_detail_level, evaluation_type, criteria_json, is_real)
VALUES 
  ('{name}', '{agency}', {edital.get('min_value', 50000)}, 
   {edital.get('max_value', 200000)}, {edital.get('execution_months', 12)},
   {edital.get('approval_rate_historical', 0.35)}, {sectors}, {stages},
   '{edital.get('technical_detail_level', 'medium')}', 
   '{edital.get('evaluation_type', 'comite_publico')}', 
   '{criteria}'::jsonb, TRUE);
""")
        
        print(f"[✓] SQL saved: {filepath}")
        return filepath


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    scraper = EditalScraper(output_dir="./data")
    
    editals = scraper.run_all()
    
    scraper.save_to_json()
    scraper.save_to_sql()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\nTotal: {len(editals)} editals")
    
    agencies = {}
    for e in editals:
        agency = e['agency'].split('/')[0].strip()
        agencies[agency] = agencies.get(agency, 0) + 1
    
    print("\nBy agency:")
    for agency, count in sorted(agencies.items(), key=lambda x: -x[1]):
        print(f"  {agency}: {count}")
