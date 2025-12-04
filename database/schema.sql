-- ============================================================================
-- EditalShield: Schema de BD para Fundação Matemática
-- ============================================================================

-- Tabela: Editais (referência)
CREATE TABLE IF NOT EXISTS editals (
    edital_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    agency VARCHAR(100) NOT NULL,  -- FINEP, FAPESP, CNPq, SEBRAE, etc.
    min_value DECIMAL(15,2),
    max_value DECIMAL(15,2),
    execution_months INT,
    approval_rate_historical FLOAT,  -- 0.0 a 1.0
    eligible_sectors TEXT[],  -- array de setores
    eligible_stages TEXT[],  -- pre-seed, seed, growth
    technical_detail_level VARCHAR(20),  -- low, medium, high
    evaluation_type VARCHAR(50),  -- comite_publico, banca_fechada
    full_text TEXT,
    criteria_json JSONB,  -- {inovacao: 30, viabilidade: 25, ...}
    is_real BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: Memoriais (originais)
CREATE TABLE IF NOT EXISTS memorials (
    memorial_id SERIAL PRIMARY KEY,
    edital_id INT REFERENCES editals(edital_id),
    sector VARCHAR(100),
    technology_type VARCHAR(100),  -- software, hardware, service, hybrid
    stage VARCHAR(50),  -- pre-seed, seed, growth
    result VARCHAR(50),  -- approved, rejected, under_review
    original_text TEXT NOT NULL,
    num_words INT,
    num_paragraphs INT,
    is_synthetic BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: Parágrafos Anotados (ground truth)
CREATE TABLE IF NOT EXISTS paragraphs_annotated (
    paragraph_id SERIAL PRIMARY KEY,
    memorial_id INT REFERENCES memorials(memorial_id),
    paragraph_index INT,  -- ordem no memorial
    original_text TEXT NOT NULL,
    section_type VARCHAR(50),  -- technical, market, team, admin
    has_exposure BOOLEAN NOT NULL,  -- 0 ou 1 (ground truth)
    exposure_types TEXT[],  -- array de tipos: [algoritmo, parametros, dataset, contatos, metricas]
    entropy_value FLOAT,
    entropy_normalized FLOAT,
    num_sensitive_patterns INT,
    edital_type VARCHAR(20),  -- public, confidential
    rater_1_label BOOLEAN,  -- anotador 1
    rater_2_label BOOLEAN,  -- anotador 2
    rater_3_label BOOLEAN,  -- anotador 3
    inter_rater_agreement FLOAT,  -- proporção que concordam
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: Padrões Sensíveis (dicionário)
CREATE TABLE IF NOT EXISTS sensitive_patterns (
    pattern_id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,  -- algoritmo, parametro, dataset, contato, metrica
    pattern_text VARCHAR(255) NOT NULL,
    is_regex BOOLEAN DEFAULT FALSE,
    weight FLOAT,  -- 0.0 a 1.0
    examples TEXT[],  -- exemplos de uso
    protection_suggestions TEXT[],  -- sugestões de reescrita genérica
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: Memoriais Protegidos (output)
CREATE TABLE IF NOT EXISTS memorials_protected (
    protected_id SERIAL PRIMARY KEY,
    memorial_id INT REFERENCES memorials(memorial_id),
    protected_text TEXT NOT NULL,
    sensitivity_level VARCHAR(20),  -- low, medium, high
    risk_score_original FLOAT,
    risk_score_protected FLOAT,
    clarity_original FLOAT,
    clarity_protected FLOAT,
    num_paragraphs_modified INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: Métricas de Validação
CREATE TABLE IF NOT EXISTS validation_metrics (
    metric_id SERIAL PRIMARY KEY,
    corpus_size_memoriais INT,
    corpus_size_paragraphs INT,
    model_auc FLOAT,
    model_precision FLOAT,
    model_recall FLOAT,
    model_f1 FLOAT,
    inter_rater_kappa FLOAT,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_memorials_edital ON memorials(edital_id);
CREATE INDEX IF NOT EXISTS idx_memorials_sector ON memorials(sector);
CREATE INDEX IF NOT EXISTS idx_paragraphs_memorial ON paragraphs_annotated(memorial_id);
CREATE INDEX IF NOT EXISTS idx_paragraphs_has_exposure ON paragraphs_annotated(has_exposure);
CREATE INDEX IF NOT EXISTS idx_patterns_category ON sensitive_patterns(category);

-- Views úteis
CREATE OR REPLACE VIEW v_memorial_stats AS
SELECT 
    m.memorial_id,
    m.sector,
    m.technology_type,
    COUNT(p.paragraph_id) as num_paragraphs,
    SUM(CASE WHEN p.has_exposure THEN 1 ELSE 0 END) as exposure_count,
    AVG(p.entropy_normalized) as avg_entropy,
    AVG(p.num_sensitive_patterns) as avg_patterns
FROM memorials m
LEFT JOIN paragraphs_annotated p ON m.memorial_id = p.memorial_id
GROUP BY m.memorial_id, m.sector, m.technology_type;

CREATE OR REPLACE VIEW v_sector_analysis AS
SELECT 
    sector,
    COUNT(DISTINCT memorial_id) as num_projects,
    AVG(CASE WHEN result = 'approved' THEN 1 ELSE 0 END) as approval_rate
FROM memorials
GROUP BY sector;
