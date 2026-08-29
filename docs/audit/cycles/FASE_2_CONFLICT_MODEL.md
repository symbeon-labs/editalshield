# FASE 2 - CONFLICT MODEL

## TIPOLOGIA DE CONFLITOS
O sistema reconhece e representa formalmente:
1. **Normative Conflict (RULE vs RULE)**: Duas regras no mesmo escopo estabelecem limites mutualmente exclusivos.
2. **Evidentiary Conflict (EVIDENCE vs EVIDENCE)**: Projeto apresenta duas evidencias autenticas mas contraditorias.
3. **Temporal/Version Conflict (VERSION vs VERSION)**: A aplicacao de uma regra retificada produz resultado diferente da original, e a reference_date cruza as linhas do tempo.

## SEMANTICA DE AVALIACAO
- Quando um conflito e detectado, a avaliacao assume o estado CONFLICT.
- CONFLICT e diferente de FAILED e de UNKNOWN.
- O estado CONFLICT requer resolucao manual ou precedencia normativa, nao sendo resolvido automaticamente.
