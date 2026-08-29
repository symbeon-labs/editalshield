# FASE 2 - FINEP RULE TEST (BENCHMARK)

| ELEMENT | REPRESENTATION | OPERATOR | CONDITION | CONSEQUENCE | SOURCE | REPRESENTABLE | GAP |
|---|---|---|---|---|---|---|---|
| Receita ate 16M | project.revenue | LTE (16M BRL) | N/A | INELIGIBLE | Sec 3.1 | SIM | - |
| TRL minimo 3 | project.trl | GTE (3 Level) | N/A | INELIGIBLE | Sec 4.2 | SIM | - |
| Contrapartida 10% N/NE | project.counterpart | GTE (0.10) | project.region IN [N, NE] | FAIL | Sec 6.1 | SIM | - |
| Contrapartida 20% | project.counterpart | GTE (0.20) | project.region NOT_IN [N, NE] | FAIL | Sec 6.1 | SIM | - |
| CND Receita Federal | project.cnd | EXISTS | N/A | WARNING | Sec 7 | SIM | CND possui validade temporal. |
| Avaliacao (Peso 3) | val.technical | MULTIPLY (3) | N/A | SCORE_BONUS | Sec 8 | SIM | - |
