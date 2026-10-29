# Rota 0 — Etapa 2 | Contrato de indicadores (KPIs)

**Regra geral:** todo KPI deve registrar unidade, base, fórmula, janela temporal, fonte, proprietário, meta e qualidade. Metas do kit não são resultados alcançados. Os valores do kit não são dados reais de cliente.

| ID | KPI | Unidade / fórmula | Baseline no kit | Meta e natureza | Fonte | Responsável proposto |
|---|---|---|---|---|---|---|
| K-01 | Tempo de fechamento mensal | Dias úteis entre início e fechamento confirmado | 7 dias úteis | 2 dias úteis, **meta oficial do kit** | `05...xlsx`, aba `Gargalos_Operacionais_Custos`, linha 2 | Controladoria |
| K-02 | Tempo de homologação de crédito | Horas entre entrada completa e decisão humana | 48h | Até 4h, **meta oficial do kit** | `05...xlsx`, aba gargalos, linha 3 | Gerência Financeira |
| K-03 | Tempo de triagem de proposta | Minutos cronometrados por pedido | 40 min, **informado no descritivo** | 30 min, **hipótese de piloto** | `06...docx`, passo 2; cronômetro no piloto | Assistente / Operações |
| K-04 | Taxa de reentregas e fretes emergenciais | Valor de gastos classificados ÷ faturamento do período × 100 | 2,8% | 0,8%, **meta oficial do kit** | `05...xlsx`, aba gargalos, linha 4 | Logística + Controladoria |
| K-05 | Divergência de boletos | Quantidade de NFs com divergência ÷ total de NFs emitidas ×100 | 6,8% | Abaixo de 0,5%, **meta do kit** | `05...xlsx`, aba gargalos, linha 5 | Faturamento |
| K-06 | Inadimplência B2B 90+ | Valor vencido há mais de 90 dias ÷ receita de base comparável × 100 | 3,4% | 1,2%, **meta do kit** | `05...xlsx`, aba gargalos, linha 6 | Crédito e Cobrança |
| K-07 | Diferença entre receita DRE e receita de produtos | Total anual da DRE - soma da visão por produto | R$ 1.100.000 diferença | **Investigar e justificar**, não supor recuperação | `05...xlsx` abas DRE e Receita; relatório de auditoria | Controller |
| K-08 | Desvio de EBITDA | (realizado - orçado) ÷ abs(orçado) ×100 | -41,41% | Monitorar por trimestre; sem meta inventada | `05...xlsx` DRE linha 21 | Controladoria |
| K-09 | Cobertura da reconciliação (futuro) | Itens conciliados com evidência ÷ itens elegíveis ×100 | **N/D** (não há itens transacionais para compor) | Definir com o responsável no piloto | Futura base granular e logs do reconciliador | Controladoria |
| K-10 | Acurácia de extração de proposta (futuro) | Campos validados corretamente ÷ campos anotados em amostra ×100 | **N/D** | Limite mínimo a ser aprovado antes de uso | PDFs de teste autorizados + gabarito humano | Vendas + TI |

## Regras de qualidade

- O campo de receita na DRE **não** pode ser substituído pela receita por produto sem homologação.
- K-04 usa a **definição do indicador operacional do kit**; não recalcular a partir de despesas contábeis sem alinhar numerador/denominador.
- K-06 também possui uma métrica de provisionamento contábil que não deve ser confundida com uma taxa de carteira vencida.
- K-07 não mede necessariamente perda, fraude, erro material ou dinheiro recuperável.
- Comparações reais antes/depois exigem mesmas populações, datas, cortes, controle de sazonalidade e qualidade mínima da amostra.
- O dashboard pode exibir baselines e metas do kit; para K-09 e K-10 deve mostrar **N/D**, não inventar valores.
