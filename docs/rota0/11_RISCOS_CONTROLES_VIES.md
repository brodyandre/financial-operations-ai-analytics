# Rota 0 — Etapa 3 | Matriz de riscos, vieses e controles de IA

**Escopo:** simulação de consultoria. Classificações de probabilidade e impacto são **avaliações propostas**, não evidências estatísticas de ocorrência.

## Metodologia

Risco inerente = **probabilidade (1–5) × impacto (1–5)**; sem quantificar chance real. Níveis sugeridos: 1–5 baixo, 6–11 moderado, 12–19 alto, 20–25 crítico. Prioridade de tratamento não substitui decisão do Comitê. Risco residual só pode ser pontuado depois da verificação de implementação dos controles.

| Risco | P | I | Score | Nível | Contenção / salvaguarda |
|---|---:|---:|---:|---|---|
| R-01 Exposição em prompts ou logs | 3 | 5 | 15 | Alto | Apenas dados sintéticos no MVP; homologação de fornecedor |
| R-02 Erro em extração de PDF / prompt injection | 4 | 4 | 16 | Alto | PDF como dado não confiável; conferir evidência por campo |
| R-03 Crédito ou alteração contábil indevida | 2 | 5 | 10 | Moderado | Bloquear escrita e exigir autorização humana |
| R-04 Divergência tratada indevidamente como perda/fraude | 4 | 4 | 16 | Alto | Evidenciar R$ 1,1 milhão como reconciliação pendente |
| R-05 Predição viesada por insuficiência de dados | 5 | 4 | 20 | Crítico | **C03 bloqueado** até histórico granular e testes |
| R-06 Falta de rastreabilidade de cálculos | 3 | 4 | 12 | Alto | Hash, versionamento, testes, fórmulas e revisão |
| R-07 Confiança excessiva em análises geradas | 4 | 3 | 12 | Alto | Separar fatos, interpretação e hipótese; fonte explícita |
| R-08 Fornecedor ou transferência não homologados | 3 | 5 | 15 | Alto | Due diligence e revisão jurídico-privacidade |

Os responsáveis e gates completos estão em `configs/governance_controls_2026.json`, registro sujeito à validação das áreas designadas.

## Como mitigar vieses concretamente

- **C01 (generativa):** criar conjunto sintético representativo de pedidos fáceis, incompletos e adversariais. Verificar erros de extração, justificativas, tratamento de documentos com instruções maliciosas e correções por revisor. Nenhum modelo foi avaliado nesta etapa.
- **C02 (analítica determinística):** revisar convenções contábeis, mapeamento entre DRE e linhas de produto e consistência de denominadores. Não existe modelo de ML em operação; o viés relevante aqui pode surgir de escopo de fontes, seleção de indicadores e interpretação.
- **C03 (preditiva):** sem histórico por pedido rotulado, não há base válida para testar vieses, precisão nem generalização. O **gate de dados** impede alegar um produto preditivo funcional.
- **Todos:** registrar reclamações, erros/decisões humanas, avaliações por período e por segmento apenas quando houver base legal, propósito e tamanho amostral adequados; não criar atributos pessoais sensíveis apenas para avaliar modelo.

## Critério de bloqueio e auditoria

Interromper uso de IA ou publicação de resultados quando houver dados reais sem autorização, decisão de crédito automatizada, ausência de fonte para valor material, erro crítico não corrigido, transferência não homologada ou recomendação sem possibilidade de revisão humana. O comitê registra causa, responsável e decisão de retomada; o demonstrador local não substitui esses procedimentos.
