# FASE 3 - PRE-IMPLEMENTATION AUDIT

## OBJETIVO
Mapear o repositorio atual antes de implementar o Rule Engine (CYCLE 2) para garantir que componentes legados nao sejam destruidos e dependencias sejam compreendidas.

## COMPONENTES REUTILIZAVEIS E DEPENDENCIAS
- **MemorialProtector** (src/editalshield/modules/memorial_protector.py): Modulo maduro de analise de padroes sensiveis (Bayesiano/RegEx). Completamente ortogonal a logica de elegibilidade normativa. Seu funcionamento esta isolado e nao sofre riscos no Cycle 2.
- **EditalMatcher** (src/editalshield/modules/edital_matcher.py): Atualmente acumula "Discovery" (TF-IDF) e "Eligibility" (hard filters de sector/stage). 
  - *Decisao*: Sera estritamente preservado. O Rule Engine nascera como um motor lateral (EVALUATION) sem canibalizar o match_project() imediatamente, cumprindo a diretriz de nao substituir componentes sem integracao paralela.

## DOMAIN MODELS (DATABASE/MODELS.PY)
- A inspecao aponta que o banco nao possui representacoes relacionais profundas do AST de Regras. A implementacao dos Domain Models (Rule, AST, Fact, Context, Evaluation) ocorrera em purismo logico inicial (em memoria / dataclasses / Pydantic) antes de esbarrar na camada de persistencia, evitando viciar o design.

## RISCOS DE REGRESSAO
- **Interfaces**: Modificar as assinaturas de entrada de NLP/Text Mining pode quebrar o matcher. O Deterministic Core recebera apenas estruturas puras (JSON/Objetos) sem demandar que o texto seja a fonte primaria durante a execucao da AST.

## STATUS
O cenario esta livre de bloqueios. A arquitetura legada (Discovery Probabilistico) e totalmente isolavel do novo Core Deterministico (Rule Engine). O caminho esta livre para implementacao do AST.
