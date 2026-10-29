# Rota 0 — Etapa 1 | Matriz de evidências e afirmações

Esta matriz mapeia afirmações executivas para fontes verificáveis, evitando alegações de causalidade não comprovadas.

| ID | Afirmação / evidência | Fonte primária | Estado |
|---|---|---|---|
| EV-01 | Receita anual DRE R$ 48,5 mi x produtos R$ 47,4 mi | `05_Financas_Orcado_vs_Realizado.xlsx`: aba `DRE_Trimestral_Orcado_Real` linha 5 e `Receita_por_Linha_Produto` linha 6 | Verificado; causa aberta como DQ-001 |
| EV-02 | EBITDA R$ 5,77 mi, orçado R$ 9,848 mi | `05_Financas_Orcado_vs_Realizado.xlsx`: DRE; `reports/audit_result.json` | Verificado |
| EV-03 | Fretes realizados R$ 3,74 mi x R$ 2,38 mi | `05_Financas_Orcado_vs_Realizado.xlsx`: DRE linha 16 | Verificado |
| EV-04 | Reentregas/multas realizadas R$ 725 mil x R$ 210 mil | `05_Financas_Orcado_vs_Realizado.xlsx`: DRE linha 17 | Verificado |
| EV-05 | Homologação de crédito: 48h vs. 4h | `05_Financas_Orcado_vs_Realizado.xlsx`: `Gargalos_Operacionais_Custos` linha 3 | Informado pelo kit |
| EV-06 | Triagem manual: 40 min por proposta | `06_Descritivo_Processo_Operacional_SIPOC.docx`, Passo 2 | Informado pelo kit |
| EV-07 | Prazo proposta-expedição: acima de 5 dias úteis vs meta 24h úteis | `06_Descritivo_Processo_Operacional_SIPOC.docx`, seção 1 | Informado pelo kit |
| EV-08 | Fechamento: 7 dias úteis vs. meta 2 | `05_Financas_Orcado_vs_Realizado.xlsx`: `Gargalos_Operacionais_Custos` linha 2 | Informado pelo kit |
| EV-09 | 3 planilhas não integradas com ERP | `06_Descritivo_Processo_Operacional_SIPOC.docx`, Passo 2, Ishikawa Máquina | Informado pelo kit |

## Afirmações não autorizadas pela evidência disponível

- A divergência de receita é um prejuízo, fraude ou perda recuperável.
- O projeto já reduziu 44h de aprovação ou 5 dias de fechamento.
- A IA já classifica o risco de atrasos com alguma precisão medida.
- As despesas contábeis podem ser somadas a impactos estimados sem sobreposição.
- O ChatGPT está integrado ao ERP ou decide crédito.

## Instrução de apresentação

Em slides, relatório e vídeo, apresentar sempre **«contexto informado pelo kit»**, **«achado de auditoria»**, **«hipótese»** ou **«meta futura»** junto aos números relevantes. Os originais ficam fora do GitHub até haver permissão de redistribuição.
