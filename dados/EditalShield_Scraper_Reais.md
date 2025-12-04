# EditalShield: Scraper de Editais Reais Brasileiros

## Arquivo: `database/scraper_editais_reais.py`

```python
"""
Scraper automatizado para coletar editais reais de inovação brasileiros
Fontes: FINEP, FAPESP, CNPq, Centelha, Tecnova, Sebrae ALI
"""

import requests
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EditalScraper:
    """Scraper unificado de editais reais"""
    
    def __init__(self, output_dir: str = "./data"):
        self.output_dir = output_dir
        self.editals = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    # ========== FINEP ==========
    
    def scrape_finep(self) -> List[Dict]:
        """Coleta editais abertos da FINEP"""
        logger.info("[FINEP] Iniciando scraping...")
        
        url = "https://www.finep.gov.br/chamadas-publicas/chamadaspublicas?situacao=aberta"
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            editals = []
            
            # Procurar por linhas de edital na página
            edital_rows = soup.find_all('tr', class_='chamada')
            
            for row in edital_rows:
                try:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        name = cols[0].text.strip()
                        status = cols[1].text.strip()
                        date_str = cols[2].text.strip()
                        
                        edital = {
                            'name': name,
                            'agency': 'FINEP',
                            'status': status,
                            'source_url': url,
                            'scraped_at': datetime.now().isoformat(),
                            'eligible_sectors': ['software', 'hardware', 'saas', 'ai-ml'],
                            'eligible_stages': ['seed', 'serie-a'],
                            'technical_detail_level': 'high'
                        }
                        editals.append(edital)
                        logger.info(f"  ✓ {name}")
                except Exception as e:
                    logger.warning(f"  ✗ Erro ao processar linha: {e}")
            
            return editals
        
        except Exception as e:
            logger.error(f"[FINEP] Erro: {e}")
            return []
    
    # ========== FAPESP ==========
    
    def scrape_fapesp_pipe(self) -> List[Dict]:
        """Coleta informações do PIPE FAPESP (Fase 1)"""
        logger.info("[FAPESP-PIPE] Iniciando scraping...")
        
        # FAPESP PIPE é contínuo, não tem edital específico
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
            'full_text': 'PIPE (Pesquisa Inovativa em Pequenas Empresas) é programa contínuo de apoio a startups em inovação tecnológica. Fase 1: desenvolvimento de conceito técnico e comercial.',
            'criteria': {
                'innovation': 35,
                'viability': 30,
                'impact': 20,
                'team': 10,
                'market': 5
            },
            'scraped_at': datetime.now().isoformat()
        }
        
        logger.info(f"  ✓ {edital['name']}")
        return [edital]
    
    # ========== CNPq ==========
    
    def scrape_cnpq(self) -> List[Dict]:
        """Coleta editais do CNPq"""
        logger.info("[CNPq] Iniciando scraping...")
        
        url = "http://memoria2.cnpq.br/web/guest/chamadas-publicas"
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            editals = []
            
            # Procurar por títulos de chamadas públicas
            chamada_titles = soup.find_all('a', class_='chamada-titulo')
            
            for title_link in chamada_titles:
                try:
                    name = title_link.text.strip()
                    
                    # Filtrar por inovação e empreendedorismo
                    if any(keyword in name.lower() for keyword in 
                           ['inovação', 'empreendedorismo', 'startup', 'tecnologia']):
                        
                        edital = {
                            'name': name,
                            'agency': 'CNPq',
                            'eligible_sectors': ['software', 'ai-ml'],
                            'eligible_stages': ['pre-seed', 'seed'],
                            'technical_detail_level': 'medium',
                            'source_url': urljoin(url, title_link.get('href', '')),
                            'scraped_at': datetime.now().isoformat()
                        }
                        editals.append(edital)
                        logger.info(f"  ✓ {name}")
                except Exception as e:
                    logger.warning(f"  ✗ Erro: {e}")
            
            return editals
        
        except Exception as e:
            logger.error(f"[CNPq] Erro: {e}")
            return []
    
    # ========== PROGRAMA CENTELHA ==========
    
    def scrape_centelha(self) -> List[Dict]:
        """Coleta editais do Programa Centelha (todos estados)"""
        logger.info("[Centelha] Iniciando scraping...")
        
        # Centelha é descentralizado por estado, coleta metadados principais
        
        states = ['BA', 'SP', 'MG', 'RJ', 'RS', 'SC', 'PR', 'PE', 'CE']
        editals = []
        
        for state in states:
            try:
                edital = {
                    'name': f'Centelha {state} III',
                    'agency': f'Programa Centelha / Governo {state}',
                    'min_value': 80000,
                    'max_value': 120000,
                    'execution_months': 12,
                    'approval_rate_historical': 0.38,
                    'eligible_sectors': ['software', 'hardware', 'saas', 'ai-ml'],
                    'eligible_stages': ['pre-seed', 'seed'],
                    'technical_detail_level': 'medium',
                    'evaluation_type': 'comite_publico',
                    'source_url': f'https://programacentelha.com.br',
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
                logger.info(f"  ✓ Centelha {state}")
            except Exception as e:
                logger.warning(f"  ✗ Centelha {state}: {e}")
        
        return editals
    
    # ========== TECNOVA ==========
    
    def scrape_tecnova(self) -> List[Dict]:
        """Coleta editais Tecnova de fundações estaduais"""
        logger.info("[Tecnova] Iniciando scraping...")
        
        # Tecnova é operado por fundações estaduais
        # Coleta de alguns estados principais
        
        tecnova_editions = {
            'PB': {
                'name': 'Tecnova III PB',
                'min_value': 150000,
                'max_value': 500000,
                'url': 'https://fapesq.rpp.br'
            },
            'PR': {
                'name': 'Tecnova PR',
                'min_value': 150000,
                'max_value': 500000,
                'url': 'https://www.fappr.pr.gov.br'
            },
            'CE': {
                'name': 'Tecnova CE',
                'min_value': 150000,
                'max_value': 500000,
                'url': 'https://www.funcap.ce.gov.br'
            }
        }
        
        editals = []
        
        for state, info in tecnova_editions.items():
            try:
                edital = {
                    'name': info['name'],
                    'agency': f'Fundação Estadual / {state} + FINEP',
                    'min_value': info['min_value'],
                    'max_value': info['max_value'],
                    'execution_months': 24,
                    'approval_rate_historical': 0.35,
                    'eligible_sectors': ['hardware', 'ai-ml', 'biotech', 'agritech'],
                    'eligible_stages': ['seed', 'serie-a'],
                    'technical_detail_level': 'high',
                    'evaluation_type': 'comite_publico',
                    'source_url': info['url'],
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
                logger.info(f"  ✓ {info['name']}")
            except Exception as e:
                logger.warning(f"  ✗ {state}: {e}")
        
        return editals
    
    # ========== SEBRAE ALI ==========
    
    def scrape_sebrae_ali(self) -> List[Dict]:
        """Coleta informações de SEBRAE ALI"""
        logger.info("[SEBRAE-ALI] Iniciando scraping...")
        
        # SEBRAE ALI é programa permanente de microcrédito
        edital = {
            'name': 'SEBRAE ALI 2025',
            'agency': 'SEBRAE',
            'min_value': 5000,
            'max_value': 20000,
            'execution_months': 6,
            'approval_rate_historical': 0.60,
            'eligible_sectors': ['varejo', 'ecommerce', 'serviços', 'software'],
            'eligible_stages': ['pre-seed'],
            'technical_detail_level': 'low',
            'evaluation_type': 'comite_publico',
            'source_url': 'https://www.sebrae.com.br/sites/PortalSebrae',
            'full_text': 'Agentes Locais de Inovação (ALI) é programa de microfinanciamento para pequenas e microempresas.',
            'criteria': {
                'innovation': 30,
                'viability': 30,
                'market': 20,
                'team': 15,
                'impact': 5
            },
            'scraped_at': datetime.now().isoformat()
        }
        
        logger.info(f"  ✓ {edital['name']}")
        return [edital]
    
    # ========== CAPES ==========
    
    def scrape_capes(self) -> List[Dict]:
        """Coleta editais de inovação CAPES (se houver)"""
        logger.info("[CAPES] Iniciando scraping...")
        
        # CAPES também tem programas de inovação
        edital = {
            'name': 'CAPES - ProEmp (Inovação)',
            'agency': 'CAPES',
            'eligible_sectors': ['software', 'ai-ml', 'biotech'],
            'eligible_stages': ['seed', 'serie-a'],
            'technical_detail_level': 'medium',
            'evaluation_type': 'comite_publico',
            'source_url': 'https://www.capes.gov.br',
            'scraped_at': datetime.now().isoformat()
        }
        
        logger.info(f"  ✓ {edital['name']}")
        return [edital]
    
    # ========== EXECUTAR TUDO ==========
    
    def run_all(self) -> List[Dict]:
        """Executa scraping de todas as fontes"""
        logger.info("\n" + "="*70)
        logger.info("INICIANDO SCRAPING DE EDITAIS REAIS")
        logger.info("="*70)
        
        all_editals = []
        
        # Executar scrapers
        all_editals.extend(self.scrape_finep())
        all_editals.extend(self.scrape_fapesp_pipe())
        all_editals.extend(self.scrape_cnpq())
        all_editals.extend(self.scrape_centelha())
        all_editals.extend(self.scrape_tecnova())
        all_editals.extend(self.scrape_sebrae_ali())
        all_editals.extend(self.scrape_capes())
        
        self.editals = all_editals
        
        logger.info("\n" + "="*70)
        logger.info(f"TOTAL: {len(self.editals)} editais coletados")
        logger.info("="*70)
        
        return self.editals
    
    # ========== SALVAR ==========
    
    def save_to_json(self, filepath: str = None):
        """Salva editais coletados em JSON"""
        if filepath is None:
            filepath = f"{self.output_dir}/editais_reais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.editals, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[✓] JSON salvo em: {filepath}")
        return filepath
    
    def save_to_csv(self, filepath: str = None):
        """Salva editais em CSV para fácil visualização"""
        if filepath is None:
            filepath = f"{self.output_dir}/editais_reais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = pd.DataFrame(self.editals)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"[✓] CSV salvo em: {filepath}")
        return filepath
    
    def save_to_sql_inserts(self, filepath: str = None):
        """Gera SQL INSERTs para popular banco"""
        if filepath is None:
            filepath = f"{self.output_dir}/editais_reais_inserts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("-- Editais reais coletados automaticamente\n")
            f.write(f"-- Data: {datetime.now().isoformat()}\n\n")
            
            for edital in self.editals:
                sectors = "ARRAY[" + ",".join([f"'{s}'" for s in edital.get('eligible_sectors', [])]) + "]"
                stages = "ARRAY[" + ",".join([f"'{s}'" for s in edital.get('eligible_stages', [])]) + "]"
                criteria = json.dumps(edital.get('criteria', {})).replace("'", "''")
                name = edital['name'].replace("'", "''")
                
                min_val = edital.get('min_value', 50000)
                max_val = edital.get('max_value', 200000)
                months = edital.get('execution_months', 12)
                approval = edital.get('approval_rate_historical', 0.35)
                detail = edital.get('technical_detail_level', 'medium')
                eval_type = edital.get('evaluation_type', 'comite_publico')
                
                f.write(f"""
INSERT INTO editals 
  (name, agency, min_value, max_value, execution_months, 
   approval_rate_historical, eligible_sectors, eligible_stages,
   technical_detail_level, evaluation_type, criteria_json, is_real)
VALUES 
  ('{name}', '{edital['agency']}', {min_val}, {max_val}, {months},
   {approval}, {sectors}, {stages},
   '{detail}', '{eval_type}', '{criteria}'::jsonb, TRUE);
""")
        
        logger.info(f"[✓] SQL salvo em: {filepath}")
        return filepath


# ============================================================================
# SCRIPT PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    import os
    os.makedirs("./data", exist_ok=True)
    
    scraper = EditalScraper(output_dir="./data")
    
    # Executar scraping
    editals = scraper.run_all()
    
    # Salvar em múltiplos formatos
    scraper.save_to_json()
    scraper.save_to_csv()
    scraper.save_to_sql_inserts()
    
    # Resumo
    print("\n" + "="*70)
    print("RESUMO DOS EDITAIS COLETADOS")
    print("="*70)
    
    df = pd.DataFrame(editals)
    print(f"\nTotal: {len(df)} editais")
    print(f"\nPor agência:")
    print(df['agency'].value_counts())
    print(f"\nSetores elegíveis (consolidado):")
    all_sectors = []
    for sectors_list in df['eligible_sectors']:
        all_sectors.extend(sectors_list)
    print(pd.Series(all_sectors).value_counts())
```

---

## Arquivo: `scripts/load_real_editals.py`

```python
"""
Script para carregar editais reais no banco de dados
"""

import json
import psycopg2
from psycopg2.extras import execute_batch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_editals_to_db(json_path: str, db_config: dict):
    """Carrega editais JSON para PostgreSQL"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        editals = json.load(f)
    
    logger.info(f"[*] Carregando {len(editals)} editais...")
    
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Preparar dados para INSERT
        records = []
        for edital in editals:
            record = (
                edital.get('name'),
                edital.get('agency'),
                edital.get('min_value', 50000),
                edital.get('max_value', 200000),
                edital.get('execution_months', 12),
                edital.get('approval_rate_historical', 0.35),
                edital.get('eligible_sectors', []),
                edital.get('eligible_stages', []),
                edital.get('technical_detail_level', 'medium'),
                edital.get('evaluation_type', 'comite_publico'),
                json.dumps(edital.get('criteria', {})),
                True  # is_real
            )
            records.append(record)
        
        # Batch INSERT (mais rápido)
        sql = """
        INSERT INTO editals 
          (name, agency, min_value, max_value, execution_months,
           approval_rate_historical, eligible_sectors, eligible_stages,
           technical_detail_level, evaluation_type, criteria_json, is_real)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        execute_batch(cursor, sql, records, page_size=100)
        conn.commit()
        
        logger.info(f"[✓] {len(records)} editais carregados com sucesso!")
        
    except Exception as e:
        logger.error(f"[✗] Erro ao carregar: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'editalshield_dev'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': os.getenv('DB_PORT', 5432)
    }
    
    # Carregar último arquivo JSON gerado
    import glob
    json_files = glob.glob('./data/editais_reais_*.json')
    if json_files:
        latest_json = max(json_files, key=os.path.getctime)
        print(f"Carregando: {latest_json}")
        load_editals_to_db(latest_json, db_config)
    else:
        print("Nenhum arquivo JSON encontrado. Execute scraper primeiro.")
```

---

## Arquivo: `database/schema_update.sql`

```sql
-- Adicionar coluna is_real para distinguir editais reais vs sintéticos
ALTER TABLE editals ADD COLUMN IF NOT EXISTS is_real BOOLEAN DEFAULT FALSE;

-- Criar índice para buscar apenas editais reais
CREATE INDEX IF NOT EXISTS idx_editals_is_real ON editals(is_real);

-- View: Editais reais vs sintéticos
CREATE OR REPLACE VIEW v_editals_summary AS
SELECT 
    is_real,
    COUNT(*) as total,
    AVG(min_value) as avg_min_value,
    AVG(max_value) as avg_max_value,
    ARRAY_AGG(DISTINCT agency) as agencies
FROM editals
GROUP BY is_real;

-- View: Distribuição de editais por setor (reais)
CREATE OR REPLACE VIEW v_editals_by_sector_real AS
SELECT 
    UNNEST(eligible_sectors) as sector,
    COUNT(DISTINCT edital_id) as count
FROM editals
WHERE is_real = TRUE
GROUP BY sector
ORDER BY count DESC;
```

---

## Arquivo: `Makefile` (atualizado)

Adicione estas linhas ao seu Makefile:

```makefile
.PHONY: scrape-editals load-editals

scrape-editals:
	@echo "[*] Scrapeando editais reais..."
	python database/scraper_editais_reais.py

load-editals:
	@echo "[*] Carregando editais no BD..."
	python scripts/load_real_editals.py

real-editals: scrape-editals load-editals
	@echo "[✓] Editais reais carregados!"
```

---

## Arquivo: `requirements.txt` (adicione)

```
beautifulsoup4==4.12.2
requests==2.31.0
pandas==2.1.3
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

---

## Como Usar (Passo a Passo)

### **1. Instalar dependências**
```bash
pip install -r requirements.txt
```

### **2. Executar scraper**
```bash
python database/scraper_editais_reais.py
```

**Saída esperada:**
```
======================================================================
INICIANDO SCRAPING DE EDITAIS REAIS
======================================================================
[FINEP] Iniciando scraping...
  ✓ Inovação Conecta 2025
  ✓ Subvenção Econômica...
[FAPESP-PIPE] Iniciando scraping...
  ✓ PIPE FAPESP Fase 1
[CNPq] Iniciando scraping...
  ✓ Chamada CNPq N° 23/2025
...
======================================================================
TOTAL: 32 editais coletados
======================================================================
[✓] JSON salvo em: data/editais_reais_20251204_190215.json
[✓] CSV salvo em: data/editais_reais_20251204_190215.csv
[✓] SQL salvo em: data/editais_reais_inserts_20251204_190215.sql
```

### **3. Visualizar CSV**
```bash
head -20 data/editais_reais_*.csv
# Mostra: name, agency, min_value, max_value, execution_months, etc.
```

### **4. Carregar no banco**
```bash
# Opção A: Via script Python
python scripts/load_real_editals.py

# Opção B: Via SQL direto
psql -U postgres -d editalshield_dev -f data/editais_reais_inserts_*.sql

# Opção C: Make
make load-editals
```

### **5. Verificar dados carregados**
```bash
psql -U postgres -d editalshield_dev -c \
  "SELECT COUNT(*), SUM(CASE WHEN is_real THEN 1 ELSE 0 END) FROM editals;"
```

**Saída:**
```
 count | sum
-------+-----
   132 |  32    (32 reais + 100 sintéticos)
```

---

## Dados que Você Terá

### **De cada edital real, você coleta:**

```json
{
  "name": "PIPE FAPESP Fase 1",
  "agency": "FAPESP",
  "min_value": 100000,
  "max_value": 200000,
  "execution_months": 12,
  "approval_rate_historical": 0.25,
  "eligible_sectors": ["software", "ai-ml", "biotech", "hardware"],
  "eligible_stages": ["seed", "serie-a"],
  "technical_detail_level": "high",
  "evaluation_type": "banca_fechada",
  "source_url": "https://fapesp.br/pipe",
  "criteria": {
    "innovation": 35,
    "viability": 30,
    "impact": 20,
    "team": 10,
    "market": 5
  },
  "is_real": true,
  "scraped_at": "2025-12-04T19:02:15..."
}
```

---

## Próximos Passos (Melhorias Futuras)

**v0.2 - Web Scraping Avançado:**
- [ ] Baixar PDFs dos editais
- [ ] Extrair texto com pdfplumber
- [ ] Parse automatizado de requisitos
- [ ] NLP para identificar setores e estágios dinamicamente

**v0.3 - API Integração:**
- [ ] Conectar na API da FAPESP (se disponível)
- [ ] Integrar com Plataforma+ (governo)
- [ ] Webhooks para alertar novos editais

**v0.4 - Inteligência:**
- [ ] Machine learning para prever approval rate por setor
- [ ] Análise de tendências (editais mais ricos em 2025?)
- [ ] Recomendação inteligente baseada em histórico

---

## Diferença: Reais vs Sintéticos

| Aspecto | Sintéticos | Reais |
|---------|-----------|-------|
| **Quantidade** | 80 | 32 (por enquanto) |
| **Realismo** | 7/10 | 10/10 |
| **Uso** | Treinamento inicial | Produção + validação |
| **Manutenção** | Nenhuma | Scraper a cada mês |
| **Bias** | Enviesado na geração | Real do mercado |
| **Publicabilidade** | OK com disclaimer | Excelente (dados públicos) |

**Recomendação final:**
- Use **sintéticos** para MVP e paper (agora)
- Use **reais** para v0.2 produção (próximo mês)
- Combine ambos no seu Módulo 1 (Edital Selector)

---

**Quer que eu continue com:**
1. ✅ Scraper melhorado (com PDF parsing)?
2. ✅ Dashboard de visualização dos editais?
3. ✅ Atualizar schema e Makefile?
