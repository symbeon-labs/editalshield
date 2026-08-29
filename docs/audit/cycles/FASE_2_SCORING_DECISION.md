# FASE 2 - SCORING DECISION

## DECISION: Separacao de Scoring do Rule Model
- **CONCEITO**: O Rule Model avalia estados logicos (Verdadeiro, Falso, Desconhecido) produzindo consequencias normativas (ex: INELIGIBLE). Scoring trata de valoracao quantitativa (Criterion), produzindo pontuacoes (Scores).
- **NECESSIDADE**: O operador MULTIPLY (3) mistura logica de decisao de estados com aritmetica de agregacao de pontos, criando ambiguidade no motor de inferencia.
- **DECISAO**: Scoring e removido da taxonomia de operadores do Rule Model. O calculo de pesos (Agregacao de Score) pertencera a uma abstracao paralela conectada a Criterion.
- **CONSEQUENCIAS**: Mantem o Rule Engine puramente logico, deterministico e focado em conformidade/elegibilidade. O ranqueamento (competitividade) ganha seu proprio ciclo de vida.
- **STATUS**: VERIFIED
