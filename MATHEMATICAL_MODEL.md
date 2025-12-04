# 🧮 Fundamentação Matemática Formal do EditalShield

Este documento apresenta a formalização matemática completa do EditalShield, seguindo padrões acadêmicos rigorosos e prontos para publicação científica.

---

## 1. Definições e Notação

### 1.1 Conjuntos Fundamentais

- **Conjunto de Editais:** $\mathcal{E} = \{e_1, \ldots, e_M\}$
- **Conjunto de Memoriais:** $\mathcal{T} = \{T_1, \ldots, T_N\}$
- **Cada memorial** $T_j$ é uma sequência de parágrafos: $T_j = \{p_{j1}, \ldots, p_{jn_j}\}$
- **Vocabulário:** $V$ — conjunto de tokens (palavras) relevantes nos textos

---

## 2. Entropia de Informação em Parágrafos

### 2.1 Distribuição Empírica de Palavras

Para um parágrafo $p$, obtemos a distribuição empírica:

1. Conte frequências $f(w)$ para cada $w \in V$ em $p$
2. Defina a probabilidade empírica:

$$p(w) = \frac{f(w)}{\sum_{u \in V} f(u)}$$

### 2.2 Entropia de Shannon

A entropia do parágrafo é definida como:

$$H(p) = - \sum_{w \in V_p} p(w) \log_2 p(w)$$

onde $V_p \subseteq V$ são as palavras que aparecem em $p$.

**Interpretação:**
- $H(p)$ **baixo** → texto genérico, repetitivo
- $H(p)$ **alto** → texto denso, rico em informação técnica

### 2.3 Normalização

$$H_{\text{norm}}(p) = \frac{H(p) - H_{\min}}{H_{\max} - H_{\min}} \in [0,1]$$

com $H_{\min}, H_{\max}$ estimados a partir do corpus de memoriais.

---

## 3. Modelo Bayesiano de Risco de Exposição de PI

### 3.1 Variável Alvo

$$X_p \in \{\text{safe}, \text{exposed}\}$$

Estado de exposição de Propriedade Intelectual do parágrafo $p$.

### 3.2 Vetor de Evidências

Para cada parágrafo $p$, definimos:

| Variável | Descrição |
|----------|-----------|
| $E_1(p)$ | Entropia normalizada $H_{\text{norm}}(p)$ |
| $E_2(p)$ | Número de padrões sensíveis detectados |
| $E_3(p)$ | Tipo de edital (público/fechado) |
| $E_4(p)$ | Tipo de tecnologia (software/hardware/serviço) |

Vetor agregado: $\mathbf{E}(p) = (E_1(p), E_2(p), E_3(p), E_4(p))$

### 3.3 Inferência Bayesiana

Queremos calcular $P(X_p = \text{exposed} \mid \mathbf{E}(p))$.

**Teorema de Bayes:**

$$P(X_p = \text{exposed} \mid \mathbf{E}(p)) = \frac{P(\mathbf{E}(p) \mid X_p = \text{exposed}) \cdot P(X_p = \text{exposed})}{P(\mathbf{E}(p))}$$

onde:

$$P(\mathbf{E}(p)) = \sum_{x \in \{\text{safe}, \text{exposed}\}} P(\mathbf{E}(p) \mid X_p = x) \cdot P(X_p = x)$$

### 3.4 Simplificação Naive Bayes

Assumindo independência condicional:

$$P(\mathbf{E}(p) \mid X_p = x) \approx \prod_{k=1}^{4} P(E_k(p) \mid X_p = x)$$

### 3.5 Score de Risco

**Score do parágrafo:**

$$R(p) = 100 \cdot P(X_p = \text{exposed} \mid \mathbf{E}(p)) \in [0, 100]$$

**Score do memorial** (agregação ponderada):

$$R(T_j) = \frac{\sum_{p \in T_j} \alpha_p \cdot R(p)}{\sum_{p \in T_j} \alpha_p}$$

onde $\alpha_p$ é o peso do parágrafo (maior para seções técnicas críticas).

---

## 4. Similaridade Projeto–Edital (TF-IDF + Cosseno)

### 4.1 Representação Vetorial TF-IDF

Para um projeto $P$ e um edital $e$, representamos como vetores em $\mathbb{R}^{|V|}$:

$$\mathbf{v}_P = \left( \text{tfidf}(w_1, P), \ldots, \text{tfidf}(w_{|V|}, P) \right)$$

$$\mathbf{v}_e = \left( \text{tfidf}(w_1, e), \ldots, \text{tfidf}(w_{|V|}, e) \right)$$

### 4.2 Similaridade de Cosseno

$$\text{sim}(P, e) = \frac{\mathbf{v}_P \cdot \mathbf{v}_e}{\|\mathbf{v}_P\| \cdot \|\mathbf{v}_e\|} \in [0, 1]$$

### 4.3 Fit Score

$$\text{Fit}(P, e) = 100 \cdot \text{sim}(P, e)$$

Este valor alimenta o **Módulo 1 (Edital Selector)**.

---

## 5. Efeito de Rede (Lei de Metcalfe)

### 5.1 Variáveis de Rede

- $n$ = número de startups usando o EditalShield
- $m$ = número de memoriais anotados na base
- $p$ = número de editais mapeados

### 5.2 Valor da Rede

$$V_{\text{rede}}(n) = k \cdot \frac{n(n-1)}{2}$$

### 5.3 Precisão do Modelo (Crescimento com Saturação)

$$\text{Prec}(m) = \min\left( \text{Prec}_0 + \gamma \cdot \frac{m(m-1)}{2},\; \text{Prec}_{\max} \right)$$

onde:
- $\text{Prec}_0$ = precisão inicial (regex + heurística)
- $\gamma$ = ganho incremental por par de memoriais
- $\text{Prec}_{\max}$ = limite superior (ex: 0.95)

### 5.4 Índice de Maturidade da Rede (IMR)

$$\text{IMR}(n,m,p) = w_1 \cdot \frac{n^2}{N_0} + w_2 \cdot \frac{m^2}{M_0} + w_3 \cdot \frac{p^2}{P_0}$$

com $w_1 + w_2 + w_3 = 1$ e $N_0, M_0, P_0$ constantes de normalização.

---

## 6. Resumo do Bloco Matemático Integrado

| # | Componente | Fórmula Principal | Aplicação |
|---|------------|-------------------|-----------|
| 1 | **Entropia** | $H(p) = -\sum p(w) \log_2 p(w)$ | Densidade de informação |
| 2 | **Bayes** | $P(X \mid E) = \frac{P(E \mid X) P(X)}{P(E)}$ | Score de risco |
| 3 | **TF-IDF** | $\text{sim} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$ | Matching de editais |
| 4 | **Metcalfe** | $V(n) = k \cdot n(n-1)/2$ | Valor da rede |

---

## 7. Referências

1. Shannon, C. E. (1948). "A Mathematical Theory of Communication". *Bell System Technical Journal*.
2. Salton, G., & McGill, M. J. (1983). "Introduction to Modern Information Retrieval". McGraw-Hill.
3. Pearl, J. (1988). "Probabilistic Reasoning in Intelligent Systems". Morgan Kaufmann.
4. Metcalfe, B. (2013). "Metcalfe's Law after 40 Years of Ethernet". *IEEE Computer*.
