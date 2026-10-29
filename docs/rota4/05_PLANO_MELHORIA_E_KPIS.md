# Plano de melhoria Lean / IA assistida — proposta TO-BE

**Natureza:** roadmap proposto, não implantado. *Quick win* inicial C02 do AI Canvas é conciliação financeira; a melhoria C01 para o fluxo B2B depende de dados e aprovação de negócio.

| Iniciativa | Primeiro passo verificável | KPI / fórmula | Baseline sintético | Meta do caso ou alvo a negociar | Responsável proposto |
|---|---|---|---|---|---|
| C02: reconciliação | Executar auditoria automatizada de consistência e tratar exceções | Divergências abertas por fonte e período | Receita DRE 48,5 mi vs produtos 47,4 mi | Sem diferenças sem justificativa | Controladoria |
| Padronização de proposta | Definir schema e checklist de campos | Taxa de propostas completas = completas/recebidas | Não medida | Definir em piloto | Comercial |
| Filas e alçadas | Registrar pedidos, responsáveis, tempo de espera e decisão humana | Tempo de homologação = fim − início, em horas | 48 h | Até 4 h (meta da fonte) | Financeiro |
| Conciliação de fechamento | Marcar etapas do fechamento e conciliações | Dias úteis até fechamento concluído | 7 dias úteis | 2 dias úteis (meta da fonte) | Controladoria |
| Qualidade do faturamento | Validar itens, preços e frete antes da liberação | Boletos divergentes / NF-e emitidas | 6,8% | Menos de 0,5% (meta da fonte) | Faturamento |
| Logística | Checar CIF/FOB e dados de entrega | Custo de reentregas e fretes expressos / receita | 2,8% | 0,8% (meta da fonte) | Logística |
| Cobrança | Formalizar rotinas e rastreio de títulos vencidos | Inadimplência >90d / receita B2B | 3,4% | 1,2% (meta da fonte) | Financeiro |

## Protocolo de piloto (não executado)

1. Levantar eventos de pedidos sintéticos e estabelecer dicionário de dados; distinguir dados observados de exemplos gerados.
2. Registrar baseline real em eventual implantação, com carimbos e origens verificáveis.
3. Rodar validação determinística antes de sugerir conclusões assistidas por ChatGPT.
4. Exigir revisão humana para crédito, faturamento, acesso e alteração de políticas.
5. Reavaliar após período piloto definido com liderança, sem reivindicar ROI alcançado.

## Riscos e limites

- ERP do cenário é legado, sem API; não prometer integração automática.
- O dashboard da demo poderá mostrar cenários e exceções, não uma integração em produção.
- **R$ 960 mil** (fretes extras relatados na aba de gargalos) não devem ser somados automaticamente ao **desvio de R$ 1,36 milhão** em fretes da DRE, sob risco de dupla contagem.
- Usar apenas dados sintéticos, com política de tratamento e revisão da Rota 0.
