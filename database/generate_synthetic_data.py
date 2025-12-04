"""
EditalShield: Synthetic Data Generator
Generates synthetic training data for the Bayesian risk model
"""

import random
import json
import math
from datetime import datetime
from typing import List, Dict, Tuple
from pathlib import Path

class SyntheticDataGenerator:
    """Generates synthetic data for EditalShield training"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.seed = seed
        
    # ========== REFERENCE DATA ==========
    
    SECTORS = [
        "software", "hardware", "saas", "iot", "ai-ml", "biotech",
        "agritech", "fintech", "healthtech", "edtech", "ecommerce",
        "varejo", "logistics", "energia", "construtech"
    ]
    
    STAGES = ["pre-seed", "seed", "serie-a", "growth"]
    
    SECTION_TYPES = ["technical", "market", "team", "admin", "budget"]
    
    TECH_TERMS = {
        "software": ["API", "microservices", "pipeline", "engine", "framework", "SDK"],
        "ai-ml": ["modelo", "rede neural", "CNN", "RNN", "transformer", "embedding"],
        "iot": ["sensor", "gateway", "protocolo", "mqtt", "edge computing"],
        "hardware": ["PCB", "FPGA", "microcontroller", "chipset"],
        "blockchain": ["smart contract", "ledger", "consensus", "wallet"],
    }
    
    COMPANY_NAMES = [
        "TechVision", "DataFlow", "InnovateLabs", "CloudCore",
        "NeuralNet", "QuantumLeap", "SwiftAI", "PureData",
        "SecureVault", "BioSync", "GreenTech", "SmartCity"
    ]
    
    EDITALS_METADATA = [
        {
            "name": "Centelha Bahia III",
            "agency": "SECTI-BA",
            "min_value": 80000,
            "max_value": 120000,
            "months": 12,
            "approval_rate": 0.38,
            "sectors": ["software", "hardware", "saas"],
            "stages": ["pre-seed", "seed"],
            "detail_level": "medium"
        },
        {
            "name": "PIPE FAPESP Fase 1",
            "agency": "FAPESP",
            "min_value": 100000,
            "max_value": 200000,
            "months": 12,
            "approval_rate": 0.25,
            "sectors": ["software", "ai-ml", "biotech"],
            "stages": ["seed", "serie-a"],
            "detail_level": "high"
        },
        {
            "name": "Finep Inovação Conecta",
            "agency": "FINEP",
            "min_value": 50000,
            "max_value": 500000,
            "months": 24,
            "approval_rate": 0.35,
            "sectors": ["hardware", "agritech", "energia"],
            "stages": ["seed", "serie-a"],
            "detail_level": "medium"
        },
        {
            "name": "CNPq RHAE",
            "agency": "CNPq",
            "min_value": 30000,
            "max_value": 150000,
            "months": 12,
            "approval_rate": 0.42,
            "sectors": ["software", "ai-ml"],
            "stages": ["pre-seed", "seed"],
            "detail_level": "low"
        },
        {
            "name": "SEBRAE ALI",
            "agency": "SEBRAE",
            "min_value": 5000,
            "max_value": 20000,
            "months": 6,
            "approval_rate": 0.60,
            "sectors": ["varejo", "ecommerce", "logistics"],
            "stages": ["pre-seed"],
            "detail_level": "low"
        }
    ]
    
    # ========== ENTROPY CALCULATION ==========
    
    def calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text"""
        words = text.lower().split()
        if not words:
            return 0.0
        
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        total = len(words)
        entropy = 0.0
        for freq in word_freq.values():
            p = freq / total
            if p > 0:
                entropy -= p * math.log2(p)
        
        return round(entropy, 4)
    
    # ========== MEMORIAL GENERATOR ==========
    
    def generate_memorial_paragraph(self, sector: str, section_type: str, 
                                   has_exposure: bool = False) -> Tuple[str, Dict]:
        """Generate a technical memorial paragraph with or without PI exposure"""
        
        company = random.choice(self.COMPANY_NAMES)
        tech_terms = self.TECH_TERMS.get(sector, ["técnicas avançadas"])
        
        if section_type == "technical":
            templates = [
                f"Nossa solução {company} utiliza {random.choice(tech_terms)} para otimizar processos de {sector}.",
                f"Desenvolvemos algoritmo proprietário para análise de dados em tempo real.",
                f"O sistema integra {random.choice(tech_terms)} com metodologias ágeis para criar pipeline eficiente.",
                f"Utilizamos validação A/B para testar a solução em ambiente de desenvolvimento.",
            ]
            
            if has_exposure:
                sensitive_additions = [
                    f" O algoritmo BehaviorAnalyzer V2 aplica parâmetros W=0.7, K=1.5.",
                    f" Dataset privado de 2M transações com acurácia 94.2%.",
                    f" Pipeline Lambda com processos parametrizados (threshold=0.8, decay=0.95).",
                    f" Contato estratégico: Dr. João Silva (j.silva@partner.com).",
                    f" ROI validado em 3 clientes: CinemaChain, RetailCorp, FinTechBR.",
                ]
                text = random.choice(templates) + random.choice(sensitive_additions)
            else:
                text = random.choice(templates)
                
        elif section_type == "market":
            if has_exposure:
                text = f"TAM estimado em R$ 500M. Clientes potenciais incluem {', '.join(random.sample(self.COMPANY_NAMES, 2))}. CAC: R$ 2500, LTV: R$ 85000 (34x)."
            else:
                text = f"Mercado de {sector} em expansão de 25-30% a.a. Nosso TAM é conservador. Modelo de receita B2B SaaS com preço estratégico."
                
        elif section_type == "team":
            text = f"Equipe com {random.randint(3, 8)} pessoas. CTO: formado em {random.choice(['Stanford', 'MIT', 'USP', 'ITA'])}. CEO com 10+ anos de experiência em startups."
            
        elif section_type == "admin":
            text = "Cronograma realista com milestones claros. Orçamento alocado conforme planejamento técnico. Rigor em gestão de riscos."
            
        else:
            text = "Seção padrão do memorial com informações gerais sobre o projeto."
        
        entropy = self.calculate_entropy(text)
        words = text.split()
        
        return text, {
            "num_words": len(words),
            "unique_words": len(set([w.lower() for w in words])),
            "entropy": entropy,
            "entropy_normalized": min(entropy / 5.0, 1.0),
            "has_exposure": has_exposure
        }
    
    def generate_memorial(self, sector: str = None, stage: str = None,
                         num_paragraphs: int = 18) -> Dict:
        """Generate a complete memorial (18-20 typical paragraphs)"""
        
        sector = sector or random.choice(self.SECTORS)
        stage = stage or random.choice(self.STAGES)
        
        memorial = {
            "sector": sector,
            "stage": stage,
            "technology_type": sector,
            "paragraphs": [],
            "total_words": 0
        }
        
        section_sequence = [
            "admin",
            "market", "market",
            "technical", "technical", "technical",
            "technical", "technical", "technical",
            "team", "team",
            "admin", "admin", "admin",
            "market",
            "admin", "admin"
        ]
        
        for i, section in enumerate(section_sequence[:num_paragraphs]):
            has_exposure = (section == "technical" and random.random() < 0.18)
            
            text, stats = self.generate_memorial_paragraph(sector, section, has_exposure)
            
            memorial["paragraphs"].append({
                "index": i,
                "section": section,
                "text": text,
                "stats": stats,
                "has_exposure": has_exposure
            })
            
            memorial["total_words"] += stats["num_words"]
        
        return memorial
    
    # ========== EDITAL GENERATOR ==========
    
    def generate_edital(self) -> Dict:
        """Generate edital metadata"""
        base = random.choice(self.EDITALS_METADATA)
        
        min_val = base["min_value"] + random.randint(-10000, 10000)
        max_val = base["max_value"] + random.randint(-10000, 10000)
        
        return {
            "name": base["name"],
            "agency": base["agency"],
            "min_value": max(min_val, 20000),
            "max_value": max(max_val, min_val + 50000),
            "execution_months": base["months"],
            "approval_rate": base["approval_rate"],
            "eligible_sectors": base["sectors"],
            "eligible_stages": base["stages"],
            "technical_detail_level": base["detail_level"],
            "evaluation_type": random.choice(["comite_publico", "banca_fechada"]),
            "criteria": {
                "innovation": random.randint(20, 40),
                "viability": random.randint(20, 35),
                "impact": random.randint(15, 30),
                "team": random.randint(10, 25),
                "market": random.randint(5, 20)
            }
        }
    
    # ========== EXPORT ==========
    
    def generate_dataset(self, num_memorials: int = 50, 
                        num_editals: int = 80) -> Dict:
        """Generate complete synthetic dataset"""
        
        print(f"[*] Generating {num_editals} editals...")
        editals = [self.generate_edital() for _ in range(num_editals)]
        
        print(f"[*] Generating {num_memorials} memorials...")
        memorials = []
        results = ["approved", "rejected", "under_review"]
        weights = [0.4, 0.35, 0.25]
        
        for i in range(num_memorials):
            if i % 10 == 0:
                print(f"    → {i}/{num_memorials}")
            memorial = self.generate_memorial()
            memorial["id"] = i + 1
            memorial["edital_id"] = random.randint(1, num_editals)
            memorial["result"] = random.choices(results, weights=weights)[0]
            memorials.append(memorial)
        
        return {
            "editals": editals,
            "memorials": memorials,
            "generated_at": datetime.now().isoformat(),
            "seed": self.seed
        }
    
    def to_json(self, dataset: Dict, filepath: str):
        """Save dataset to JSON"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        print(f"[✓] Dataset saved to: {filepath}")
    
    def to_sql_inserts(self, dataset: Dict, filepath: str):
        """Generate SQL INSERTs to populate database"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("-- EditalShield Synthetic Data\n")
            f.write(f"-- Generated: {datetime.now().isoformat()}\n\n")
            
            # Editals
            f.write("-- Inserting Editals\n")
            for i, edital in enumerate(dataset["editals"], 1):
                sectors = "ARRAY[" + ",".join([f"'{s}'" for s in edital["eligible_sectors"]]) + "]"
                stages = "ARRAY[" + ",".join([f"'{s}'" for s in edital["eligible_stages"]]) + "]"
                criteria = json.dumps(edital["criteria"]).replace("'", "''")
                name = edital["name"].replace("'", "''")
                
                f.write(f"""
INSERT INTO editals (name, agency, min_value, max_value, execution_months, 
                     approval_rate_historical, eligible_sectors, eligible_stages,
                     technical_detail_level, evaluation_type, criteria_json)
VALUES ('{name}', '{edital["agency"]}', {edital["min_value"]}, 
        {edital["max_value"]}, {edital["execution_months"]}, 
        {edital["approval_rate"]}, {sectors}, {stages},
        '{edital["technical_detail_level"]}', '{edital["evaluation_type"]}',
        '{criteria}'::jsonb);
""")
            
            # Memorials
            f.write("\n-- Inserting Memorials\n")
            for memorial in dataset["memorials"]:
                full_text = " ".join([p["text"] for p in memorial["paragraphs"]])
                text_escaped = full_text.replace("'", "''")
                
                f.write(f"""
INSERT INTO memorials (edital_id, sector, technology_type, stage, result,
                       original_text, num_words, num_paragraphs, is_synthetic)
VALUES ({memorial['edital_id']}, '{memorial['sector']}', '{memorial['technology_type']}',
        '{memorial['stage']}', '{memorial['result']}', '{text_escaped}',
        {memorial['total_words']}, {len(memorial['paragraphs'])}, TRUE);
""")
            
            # Paragraphs
            f.write("\n-- Inserting Paragraphs\n")
            for memorial in dataset["memorials"]:
                for p in memorial["paragraphs"]:
                    text_escaped = p["text"].replace("'", "''")
                    f.write(f"""
INSERT INTO paragraphs_annotated (memorial_id, paragraph_index, original_text, 
                                  section_type, has_exposure, entropy_value, 
                                  entropy_normalized, num_sensitive_patterns)
VALUES ({memorial['id']}, {p['index']}, '{text_escaped}',
        '{p['section']}', {str(p['has_exposure']).upper()}, {p['stats']['entropy']},
        {p['stats']['entropy_normalized']}, {1 if p['has_exposure'] else 0});
""")
        
        print(f"[✓] SQL INSERTs generated: {filepath}")


# ========== MAIN ==========

if __name__ == "__main__":
    generator = SyntheticDataGenerator(seed=42)
    
    dataset = generator.generate_dataset(num_memorials=50, num_editals=80)
    
    generator.to_json(dataset, "data/synthetic_dataset.json")
    generator.to_sql_inserts(dataset, "data/synthetic_inserts.sql")
    
    print("\n[✓] Synthetic dataset complete!")
    print(f"    - {len(dataset['editals'])} editals")
    print(f"    - {len(dataset['memorials'])} memorials")
    total_paragraphs = sum([len(m['paragraphs']) for m in dataset['memorials']])
    print(f"    - {total_paragraphs} paragraphs")
    print(f"    - ~{sum([m['total_words'] for m in dataset['memorials']])} words")
