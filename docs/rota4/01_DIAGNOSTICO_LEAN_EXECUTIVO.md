# Rota 4 — Etapa 1 | Diagnóstico Lean executivo

**Taranis Black — proposta consultiva, sem implantação.** Dados sintéticos oficiais da Alura. Material preparado com apoio do ChatGPT, revisto com regras e testes determinísticos em Python.

## Questão central

A operação B2B processa **180–220 pedidos por mês**, segundo o dossiê de processos. O prazo diretivo entre a proposta assinada e a expedição é **até 24 horas úteis**, mas o fluxo atual **ultrapassa cinco dias úteis**. O mesmo documento relata **cinco dias de atraso no fechamento contábil**; a planilha financeira especifica **sete dias realizados ante dois dias úteis de meta**, ou seja, atraso de cinco dias. Não confundir **ciclo do pedido** com **tempo de fechamento mensal**: são indicadores diferentes.

**Fontes:** `06_Descritivo_Processo_Operacional_SIPOC.docx`, contexto e fluxo AS-IS; `05_Financas_Orcado_vs_Realizado.xlsx`, aba `Gargalos_Operacionais_Custos`, linha 2.

## Desperdícios Lean e evidências

| Desperdício | Evidência do caso | Hipótese de intervenção |
|---|---|---|
| Espera | Aprovação da gerência retém pedidos por 24–48 horas úteis | Regras claras de alçada e fila rastreável, mantendo decisão humana de crédito |
| Processamento excessivo | Assistente consulta três sistemas/planilhas; 40 min por proposta | Pré-triagem assistida do PDF e validações determinísticas |
| Defeitos / retrabalho | Erros em códigos de produto, inscrição e frete CIF/FOB | Campos obrigatórios e validação antes do faturamento |
| Movimentação de informação | E-mails sucessivos entre vendas, financeiro e CD | Protocolo único de pedido e rastreio de status, sem afirmar integração ao ERP |
| Estoques em processo | Pedidos aguardam resposta em caixas de e-mail | Painel de fila com responsável, idade e SLA |

Os nomes dos desperdícios são enquadramento analítico Lean; os fatos associados provêm do dossiê. **Não há medição pré/pós-piloto**.

## Sinais quantitativos de urgência

| KPI | Meta | Realizado | Proveniência |
|---|---:|---:|---|
| Fechamento contábil | 2 dias úteis | 7 dias úteis | XLSX 05, aba Gargalos, linha 2 |
| Homologação de crédito B2B | Até 4 h | 48 h | XLSX 05, aba Gargalos, linha 3 |
| Reentregas e fretes emergenciais | 0,8% do faturamento | 2,8% | XLSX 05, aba Gargalos, linha 4 |
| Divergência de boletos | Menos de 0,5% das NF-e | 6,8% | XLSX 05, aba Gargalos, linha 5 |
| Inadimplência B2B > 90 dias | 1,2% da receita | 3,4% | XLSX 05, aba Gargalos, linha 6 |

As métricas são **baselines do cenário simulado**; não significam que os gargalos tenham sido eliminados.

## Decisão executiva proposta

1. **Primeiro piloto: C02, conciliação financeira e controles de qualidade dos dados.** Base determinística existente, resultados auditáveis e supervisão humana.
2. **Projeto de melhoria operacional: C01, pré-triagem e passagem de bastão dos pedidos B2B.** Criar padrão documental, regras explícitas, mensuração de fila e aprovação humana em alçadas. Implementação futura condicionada.
3. **C03 bloqueado:** sem histórico granular rotulado não é defensável anunciar um modelo preditivo logístico funcional.

## Cuidados na interpretação financeira

- A divergência de receita **DRE R$ 48,5 mi × linhas de produto R$ 47,4 mi** é pendência de reconciliação de **R$ 1,1 mi**; não é perda comprovada.
- Os **R$ 960 mil/ano** de impacto relatado para fretes extras na aba de gargalos **não são automaticamente iguais** ao desvio de despesa total de fretes da DRE (R$ 3,74 mi realizado − R$ 2,38 mi orçado = **R$ 1,36 mi**). As bases têm escopos distintos até conciliação.
- Indicadores e potenciais benefícios de ROI são estimativas, não ganhos realizados.

## Plano de medição proposto

Para uma implantação real, registrar carimbo de tempo por etapa, identificador do pedido, motivo de retenção, responsável, status, categoria de exceção, retrabalho e resultado final. Comparar períodos antes/depois com escopo e mix de pedidos equivalentes. Não usar dados pessoais reais no protótipo do challenge.
