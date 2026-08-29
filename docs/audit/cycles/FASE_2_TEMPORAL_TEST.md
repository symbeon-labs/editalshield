# FASE 2 - TEMPORAL ADVERSARIAL TEST

**CENARIO 1: Validade Documental vs Data de Submissao**
- **Resultado Esperado**: FAILED. O modelo representa o cenario usando operador GTE contra context.submission_date.

**CENARIO 2: Validade vs Data Desconhecida**
- **Contexto Atual**: signature_date nulo.
- **Resultado Esperado**: UNKNOWN. A avaliacao da expressao falha por carencia de fato no Contexto.

**CENARIO 3: Retificacoes do Edital**
- **Avaliacao**: O escopo (EdictVersion na Evaluation) resolve a ambiguidade temporal.
Conclusao: O Rule Model suporta operacoes cronologicas injetando Context Facts.
