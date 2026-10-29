# Rota 0 — Etapa 2 | Hipóteses de valor, ROI e sensibilidade

## O que pode e o que não pode ser quantificado

**Pode ser calculado com segurança:** desvio realizado versus orçamento, tempo de processo descrito no kit, inconsistências entre fontes e cenários algébricos definidos por hipóteses.  
**Não pode ser afirmado:** economia já obtida pela solução, aumento de faturamento, ROI real, redução de inadimplência causada por IA, performance de modelo preditivo ou recuperação de R$ 1,1 milhão da reconciliação.

O kit **não contém volumes mensais de propostas, custo-hora completo, investimento de implantação nem manutenção**. Portanto, não existe base suficiente para ROI financeiro de produção. Para cumprir o requisito pedagógico, documentamos **sensibilidade ilustrativa** do C01, sem apresentá-la como business case homologado.

## Hipóteses explícitas (todas não confirmadas, exceto o tempo-base)

| Parâmetro | Valor adotado | Situação |
|---|---:|---|
| Tempo-base por triagem | **40 min/pedido** | Informado no documento operacional do kit |
| Redução de tempo | **25%** (10 min/pedido) | Hipótese de demonstração, não medição |
| Custo-hora carregado | **R$ 60** | Hipótese, não custo da empresa |
| Volumes mensais | **100 / 200 / 400 propostas** | Faixas hipotéticas; falta base oficial |
| Implantação | **R$ 15.000** | Premissa ilustrativa |
| Manutenção | **R$ 300 por mês** | Premissa ilustrativa |
| Horizonte | **12 meses** | Escolha de modelagem |

**Fórmulas:**

- `horas liberadas/mês = volume × 40min × 25% ÷ 60`.
- `capacidade anual valorizada = horas liberadas/mês × R$60/h × 12`.
- `custo anual do cenário = R$15.000 + 12 × R$300 = R$18.600`.
- `ROI TEÓRICO se a capacidade for monetizada = (valor de capacidade - custo anual) / custo anual ×100`.

| Volume hipotético (pedidos/mês) | Tempo liberado/mês | Capacidade anual valorizada | Custo anual hipotético | ROI teórico *condicional* |
|---:|---:|---:|---:|---:|
| 100 | 16,67 horas | R$ 12.000 | R$ 18.600 | -35,48% |
| 200 | 33,33 horas | R$ 24.000 | R$ 18.600 | 29,03% |
| 400 | 66,67 horas | R$ 48.000 | R$ 18.600 | 158,06% |

Ponto de equilíbrio teórico: **155 propostas mensais** (assumindo realização integral do valor, os custos escolhidos e aplicação em 12 meses). Essa medida **não valida a decisão de investimento**: disponibilizar tempo de funcionários pode melhorar atendimento e capacidade sem reduzir desembolsos efetivos.

## Como transformar em ROI legítimo após o challenge

1. Registrar volume real por mês, classificação de propostas e tempo de triagem por amostra representativa.
2. Validar custos efetivos (tecnologia, licenciamento, treinamentos, monitoramento, armazenamento, auditoria, contingência e hora carregada).
3. Medir horas antes/depois com grupo comparável e verificação da qualidade, inclusive retrabalho da revisão humana.
4. Identificar **benefício financeiro efetivamente realizado** (custos evitados ou vendas incrementais comprovadas), distinguindo de capacidade liberada.
5. Aprovar cálculo e contabilização com Controladoria; acompanhar sensitividade de adoção, erros e sazonalidade.

## Benefícios do C02 não contabilizados

O C02 tem linhas de base de 7 dias de fechamento e R$ 1,1 milhão de discrepância entre fontes, mas **não** é possível determinar o benefício monetário do reconciliador sem histórico de horas, quantidade de itens, custo de correção e cobertura. Por isso, **não incluímos um ROI inventado para o C02**.

**Controle de dupla contagem:** estimativas de impacto operacional da aba de gargalos podem se sobrepor a despesas já registradas na DRE. Não somá-las como benefício independentemente.

**Reprodutibilidade:** parâmetros em `configs/prioritization_2026.json`; cálculos e relatório em `src/taranis_black/prioritization.py` e `reports/rota0_etapa2_resumo.md`.
