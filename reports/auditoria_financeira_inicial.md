# Auditoria financeira inicial — Taranis Black

**Fonte:** `05_Financas_Orcado_vs_Realizado.xlsx` (Mock Data Kit da Alura).
**Natureza:** cenário sintético. **Escopo:** quatro trimestres disponíveis; valores anuais em BRL.

## Resumo executivo

- Receita bruta realizada (DRE): **R$ 48.500.000,00**.
- EBITDA: **R$ 5.770.000,00** frente a R$ 9.848.000,00 orçados (-41,41%).
- Lucro líquido: **R$ 3.108.600,00** frente a R$ 5.965.080,00 orçados (-47,89%).
- Verificações automatizadas: **48/48** aprovadas; **0** falhas de cálculos internos.

## Conciliação de receitas — atenção prioritária

| Referência | DRE | Linhas de produto | Diferença (DRE − produtos) |
|---|---:|---:|---:|
| Receita orçada | R$ 48.600.000,00 | R$ 48.000.000,00 | **R$ 600.000,00** |
| Receita realizada | R$ 48.500.000,00 | R$ 47.400.000,00 | **R$ 1.100.000,00** |

A divergência **não é um prejuízo apurado**: pode refletir escopo, classificação ou inconsistência na base. A causa permanece não determinada.

## Desvios desfavoráveis em despesas operacionais

| Conta da DRE | Orçado | Realizado | Excesso |
|---|---:|---:|---:|
| Despesas com Fretes e Logística de Entrega CD | R$ 2.380.000,00 | R$ 3.740.000,00 | **R$ 1.360.000,00** |
| Reentregas e Multas por Divergência de Pedido | R$ 210.000,00 | R$ 725.000,00 | **R$ 515.000,00** |
| Provisão para Devedores Duvidosos (Inadimplência B2B) | R$ 440.000,00 | R$ 1.110.000,00 | **R$ 670.000,00** |

Os valores acima são desvios contábeis, **não** economias já realizadas. Estimativas de impacto dos gargalos não devem ser somadas sem conciliação.

## Participação por produto — conferência

| Linha | Informado | Calculado com valores realizados | Divergência (p.p.) | Situação |
|---|---:|---:|---:|---|
| Taranis ErgoPro (Cadeiras Corporativas) | 48.5% | 50.32% | 1.82 | REVIEW |
| Taranis SmartDesk (Mesas Elevatórias) | 27.5% | 26.69% | -0.81 | REVIEW |
| Taranis Silence (Cabines Acústicas) | 18.0% | 17.09% | -0.91 | REVIEW |
| Acessórios e Periféricos Ergonômicos | 6.0% | 5.91% | -0.09 | OK |

## Registro de qualidade de dados

### DQ-001 — Receita bruta anual não reconcilia entre abas
**Risco:** high  
**Evidência:** A DRE difere do total por linhas de produto no orçado e no realizado.  
**Tratamento proposto:** Confirmar critérios de escopo, canais, período e regras de consolidação. Não somar nem substituir bases sem validação.

### DQ-002 — Participações por produto não correspondem integralmente aos valores realizados
**Risco:** medium  
**Evidência:** Os percentuais informados somam 100%, mas diferem dos percentuais calculados a partir dos valores reais por produto.  
**Tratamento proposto:** Definir a base do percentual informado e sinalizar divergências maiores que 0,5 ponto percentual.

### DQ-003 — Impactos operacionais estimados podem sobrepor despesas da DRE
**Risco:** medium  
**Evidência:** Gargalos_Operacionais_Custos apresenta impactos estimados, enquanto a DRE apresenta despesas contabilizadas.  
**Tratamento proposto:** Não somar diretamente as estimativas de impacto aos desvios contábeis; solicitar rastreio e conciliação.

### DQ-004 — Histórico insuficiente para afirmar precisão preditiva
**Risco:** medium  
**Evidência:** A DRE disponibilizada tem quatro observações trimestrais.  
**Tratamento proposto:** Usar cenários com premissas explícitas; não anunciar previsão estatisticamente validada.

## Critérios de conclusão desta etapa

- [x] Totais anuais conciliados com os trimestres em cada linha da DRE.
- [x] Identidades contábeis anuais verificadas.
- [ ] Divergências entre abas explicadas por fonte autorizada (pendência aberta).
- [x] Hipóteses, estimativas e fatos identificados separadamente.

## Próximo passo

Construir o AI Canvas e a matriz Esforço × Impacto a partir dos gargalos confirmados, preservando a revisão humana para crédito e faturamento.
