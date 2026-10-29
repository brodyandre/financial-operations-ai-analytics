# SIPOC — Aprovação de Pedido, Faturamento e Expedição B2B

**Escopo:** da recepção da proposta assinada à transmissão da ordem de expedição. A matriz segue o conteúdo da tabela SIPOC do `06_Descritivo_Processo_Operacional_SIPOC.docx`, com redação condensada.

| Supplier (Fornecedor) | Input (Entrada) | Process (Processo) | Output (Saída) | Customer (Cliente) |
|---|---|---|---|---|
| Consultores de vendas B2B e SDR | Proposta comercial assinada em PDF | 1. Receber e triar proposta | Ordem de venda cadastrada | Assistente financeiro |
| Cliente B2B | CNPJ, IE e endereço | 2. Consultar birô e histórico | Dossiê de crédito | Gerente financeiro |
| Birô de crédito | Score, protestos e pendências | 3. Submeter à alçada | Autorização formal de faturamento | Faturamento / Contabilidade |
| Gerência financeira | Aprovação por e-mail | 4. Emitir NF-e e boletos | DANFE, XML e boletos | Cliente comprador |
| CD e transportadoras | Tabelas de frete e rotas | 5. Transmitir pedido à expedição | Picking list e minuta | CD de Joinville / Transportadora |

## Fronteiras e observações

- **Início:** proposta assinada recebida. **Fim:** ordem transmitida ao CD, antes do transporte físico.
- A entrada de dados incompletos retorna ao comercial, criando retrabalho.
- A política de crédito e os lançamentos contábeis permanecem sob responsabilidade humana.
- Este SIPOC é uma representação do processo existente; não comprova implantação de um novo fluxo.
