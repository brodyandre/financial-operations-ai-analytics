# Fonte operacional — resumo rastreável para a próxima fase

**Origem:** `06_Descritivo_Processo_Operacional_SIPOC.docx`, seções de fluxo atual, SIPOC e Ishikawa.

## Processo atual (AS-IS)

1. Vendedor envia PDF assinado por e-mail sem validação prévia de CNPJ, estoque ou limite de crédito.
2. Assistente abre manualmente ERP, birô de crédito e planilha; consulta consome cerca de 40 min/pedido.
3. Assistente solicita aprovação individual ao gerente financeiro por e-mail, inclusive pedidos pequenos.
4. Gerente pode levar de 24 a 48 horas úteis para responder; pedidos ficam parados.
5. Assistente digita faturamento no ERP e envia autorização de expedição por e-mail ao CD de Joinville; erros e divergências CIF/FOB provocam retrabalho.

**Meta relatada no dossiê:** até 24 horas úteis da proposta assinada à expedição. **Cenário observado:** mais de 5 dias úteis.

## Mapeamento SIPOC (já presente na fonte; refinaremos visualmente depois)

| Fornecedor (S) | Entrada (I) | Processo (P) | Saída (O) | Cliente (C) |
|---|---|---|---|---|
| Vendas/SDR | Proposta PDF assinada | Recebimento/triagem | Pedido cadastrado | Financeiro |
| Cliente B2B | Dados cadastrais | Consulta de crédito | Dossiê de crédito | Gerente financeiro |
| Birô de crédito | Score/pendências | Submissão à alçada | Aprovação de faturamento | Faturamento |
| Gerência financeira | Autorização | Emissão NF-e/boletos | NF-e, XML e boletos | Cliente |
| CD e transportadoras | Tabelas de frete | Transmissão à expedição | Picking list e minuta | CD/transportadora |

**Eixos para Ishikawa:** Método (POP/limites), Máquina (ERP sem API/planilhas), Mão de Obra (sobrecarga), Material (propostas incompletas), Medição (ausência de SLAs), Meio Ambiente (comunicação entre unidades).

*Este arquivo é um resumo de trabalho, não substitui o diagrama Lean obrigatório nem comprova que a IA implementou melhorias.*
