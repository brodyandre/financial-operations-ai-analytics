# Rota 0 — Etapa 2 | Matriz Esforço × Impacto

**Projeto:** Challenge ONE G11 — Taranis Black | Rota 0 obrigatória + Rota 4.  
**Versão:** candidata para revisão executiva, 29/10/2026.  
**Situação:** proposta metodológica, não representa aprovação de gestores fictícios nem resultados já alcançados.

## 1. Decisão executiva recomendada

1. **C02 — Conciliação financeira e qualidade de dados: implementar primeiro no MVP**. Já existem planilhas derivadas, rotina de auditoria e verificações automatizadas; oferece uma entrega viável no prazo com riscos controlados. **É um controle determinístico, não um modelo de ML**. O ChatGPT auxilia na interpretação e produção do relatório; o Python calcula e valida.
2. **C01 — Assistente generativo de pré-triagem B2B: piloto seguinte, condicional**. Requer amostras sintéticas de documentos, teste de acurácia por campo, regras de alçada e revisão humana. É a oportunidade prioritária para posterior automação com IA generativa, não uma funcionalidade pronta.
3. **C03 — Modelo preditivo logístico: não incluir no MVP**. Sem eventos históricos por pedido e rótulos, não é possível justificar treinamento, acurácia ou previsão em produção.

Essa ordem é **sequenciamento de implantação**, não a declaração de que C02 possui um modelo de IA treinado. A seleção estratégica das três oportunidades permanece a da Etapa 1.

## 2. Metodologia — notas qualitativas e pesos explícitos

Os três casos recebem notas ordinais de **1 a 5** por critério. Para impacto, nota maior significa maior efeito potencial. Para esforço, nota maior significa maior dificuldade **dentro do MVP demonstrativo offline**, não em implantação real.

- **Impacto:** relevância financeira (40%), contribuição para prazo/SLA (35%), abrangência interfuncional (25%).
- **Esforço:** preparação e disponibilidade de dados (35%), integração necessária ao MVP (35%), governança e adoção (30%).
- Fórmula por eixo: `score = Σ(nota_do_critério × peso_do_critério)`.
- Quadrante de referência: **alto impacto se nota ≥ 4,0; baixo esforço se nota ≤ 3,0**.
- Um **gate de dados** pode bloquear implementação independentemente da pontuação. A direção executiva deverá homologar pesos, notas e critérios antes de orçamento real.

Essas notas são **avaliações consultivas documentadas**, não fatos do kit nem medições financeiras. As notas compostas auxiliam discussão e não devem ser tratadas como grandezas de ROI.

## 3. Matriz para decisão

| Caso | Relevância financeira | SLA | Abrangência | Impacto ponderado | Dados | Integração | Governança | Esforço ponderado | Quadrante |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| C01 | 4 | 5 | 4 | **4,35** | 3 | 4 | 3 | **3,35** | Alto impacto / maior esforço |
| C02 | 5 | 4 | 4 | **4,40** | 2 | 2 | 2 | **2,00** | Alto impacto / baixo esforço (no MVP) |
| C03 | 4 | 4 | 3 | **3,75** | 5 | 5 | 4 | **4,70** | Bloqueado por dados insuficientes |

*Scores e racional armazenados em `configs/prioritization_2026.json`, calculados por `src/taranis_black/prioritization.py`.*

### Justificativas por caso

- **C02:** fechamento atual 7 dias úteis, meta de 2; divergência DRE/produtos R$ 1,1 milhão em reconciliação. Números justificam interesse, **não significam** R$ 1,1 milhão recuperáveis. No MVP, dados e testes disponíveis diminuem esforço; integração com ERP real não foi considerada.
- **C01:** triagem manual de 40 minutos por pedido, homologação atual de 48h versus meta até 4h. Há potencial relevante de melhoria, mas não sabemos volume mensal nem taxa de erro do extrator, e redução do tempo de triagem não garante redução equivalente do SLA de aprovação.
- **C03:** fretes, reentregas e atrasos afetam o negócio, mas quatro trimestres de agregados não bastam para previsão por pedido. O modelo permanece conceitual.

## 4. Ordem cronológica e dependências

| Horizonte | Ação | Pré-requisito / evidência de aceite | Responsável proposto |
|---|---|---|---|
| Challenge (até 08/11/2026) | C02: relatórios de auditoria + dashboard com KPIs e cenários | 48 verificações preservadas; divergências visíveis; nenhuma correção silenciosa | Analista de dados + validação da Controladoria |
| Piloto posterior, após autorização | C01: coletar PDFs sintéticos, avaliar extração e prototipar checklist | Regras de negócio assinadas, acurácia por campo, base de teste, logs de revisão | Vendas, Financeiro e TI |
| Evolução posterior, sem data comprometida | C03: inventariar dados/eventos e testar viabilidade de ML | Série de eventos rotulada por pedido; avaliação de drift e vazamento | Logística + Dados |

## 5. Evidências observadas, metas e limites

| KPI | Baseline sintético informado | Meta/limite | Como verificar no piloto |
|---|---|---|---|
| Fechamento contábil | 7 dias úteis | 2 dias úteis (meta do kit) | Logs com início/fim em ciclos comparáveis; **não medido no app** |
| Triagem de proposta | 40 minutos/pedido | 30 min/pedido (hipótese de piloto: -25%) | Cronometrar amostra representativa antes/depois; **não realizado** |
| Homologação de crédito | 48 horas | até 4 horas (meta do kit) | Timestamp de recebimento/aprovação; não confundir com triagem |
| Divergência DRE/produtos | R$ 1,1 milhão | Investigar e documentar diferença | Reconciliação por competência, escopo e conta; não impor zero sem explicação |
| Reentregas e fretes emergenciais | 2,8% do faturamento | 0,8% do faturamento (meta do kit) | Série por período e denominador reconciliado; sem atribuir causalidade automática à IA |

## 6. Uso no relatório executivo

Proposta de texto breve para a seção de priorização da Rota 0:

> Com base no Mock Data Kit, a Taranis Black apresenta gargalos financeiros e operacionais que justificam três oportunidades: triagem generativa de propostas, conciliação de dados e previsão de risco logístico. Pela matriz qualitativa Esforço × Impacto, priorizamos o piloto de conciliação (impacto 4,40/5; esforço 2,00/5 no contexto offline) por disponibilidade imediata dos dados e auditabilidade. A triagem generativa será a segunda frente, sujeita à validação de documentos e alçadas; a iniciativa preditiva ficará condicionada à obtenção de histórico granular. Os escores são estimativas consultivas e não representam ROI realizado.

## 7. Riscos e mitigação

- **Risco de dados:** conciliações cruzadas abertas não podem ser apagadas nem editadas manualmente para bater totais. Mitigar com manifesto, testes e revisão da Controladoria.
- **Risco de escopo:** notas do MVP não devem ser usadas para estimar custo de implantação real, sobretudo ERP e integrações.
- **Risco de IA:** classificar regras determinísticas como controles; a IA generativa é aplicada à análise e ao caso C01 proposto.
- **Risco de benefício:** não somar estimativas operacionais com contas contábeis potencialmente sobrepostas e não declarar economias antes de piloto real.

**Fontes:** `05_Financas_Orcado_vs_Realizado.xlsx`, abas DRE, receita e gargalos; `06_Descritivo_Processo_Operacional_SIPOC.docx`, passos AS-IS; auditoria e AI Canvas da Fase 1/Etapa 1.
