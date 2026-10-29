# Rota 0 — Etapa 1 | AI Canvas e oportunidades de IA

**Challenge:** ONE G11 — AI for Business | Taranis Black  
**Vertical:** Rota 4 — Finanças e Operações  
**Status:** versão candidata para revisão executiva, 29/10/2026  
**Origem:** Mock Data Kit sintético da Alura; nenhuma implantação ou ganho realizado.

## 1. Síntese executiva

A Taranis Black apresenta perdas de eficiência em aprovação de pedidos, conciliação financeira e logística, associadas a fluxos manuais e sistemas legados. A proposta é combinar **IA generativa para apoiar leitura e triagem documental**, **controles determinísticos para conciliação e qualidade financeira** e, numa fase futura, **IA preditiva para sinalizar risco de atrasos e custos logísticos**. Os casos de uso não substituem aprovações humanas nem lançamentos autorizados no ERP.

A sequência proposta é **primeiro confiabilidade dos dados, depois protótipo de apoio à triagem e, apenas com histórico granular adequado, análise preditiva**. A ordem definitiva será justificada na Rota 0 — Etapa 2 (Matriz Esforço × Impacto), ainda não concluída.

## 2. Diagnóstico de base — fatos verificados

| Identificador | Evidência do material | Interpretação responsável |
|---|---|---|
| E-FIN-01 | Receita bruta anual realizada: DRE R$ 48.500.000; soma das linhas de produto R$ 47.400.000; diferença R$ 1.100.000 | Divergência entre fontes; **não** classificar como prejuízo, fraude ou dinheiro recuperável |
| E-FIN-02 | EBITDA R$ 5.770.000, ante R$ 9.848.000 orçados (-41,41%) | Desvio de resultado, sem causalidade automática atribuível a IA |
| E-FIN-03 | Fretes: R$ 3.740.000 realizados e R$ 2.380.000 orçados; excesso R$ 1.360.000 | Desvio contábil que requer decomposição por causa |
| E-FIN-04 | Reentregas/multas: R$ 725.000 realizados e R$ 210.000 orçados; excesso R$ 515.000 | Desvio; não somar diretamente a estimativas operacionais correlatas |
| E-OP-01 | Homologação de crédito: 48 horas, contra meta de até 4 horas; triagem manual de aproximadamente 40 minutos/pedido | Gargalo do fluxo de pedidos, conforme documentação operacional |
| E-OP-02 | Fluxo entre proposta e expedição ultrapassa 5 dias úteis, contra meta de 24 horas úteis | Base para diagnóstico Lean (Rota 4) |
| E-OP-03 | Conciliação de três planilhas com ERP desconectado; fechamento em 7 dias úteis, meta 2 dias | Motivação para controles de qualidade e reconciliadores |

**Fontes completas:** `05_Financas_Orcado_vs_Realizado.xlsx` (abas `DRE_Trimestral_Orcado_Real`, `Receita_por_Linha_Produto`, `Gargalos_Operacionais_Custos`); `06_Descritivo_Processo_Operacional_SIPOC.docx` (fluxo AS-IS, SIPOC e causas 6M). Conferência programática em `reports/auditoria_financeira_inicial.md` e `reports/audit_result.json`.

## 3. AI Canvas — visão corporativa

| Elemento do Canvas | Definição |
|---|---|
| Objetivo de negócio | Acelerar processamento B2B, reduzir inconsistências financeiras e dar visibilidade aos gargalos sem ampliar proporcionalmente a equipe |
| Patrocinador | CEO; validação operacional por gerência Financeira e Controladoria (papéis propostos, não nomeados no kit) |
| Usuários | Assistentes financeiros, Controladoria, Gerência Financeira, Vendas B2B e Expedição |
| Fontes de dados | Propostas em PDF, dados cadastrais, regras de alçada, planilhas, ERP legado e histórico de pedidos; no MVP somente dados sintéticos autorizados |
| Oportunidades | C01 — triagem assistida; C02 — reconciliação e QA; C03 — alerta de risco logístico (futuro) |
| Critério geral de sucesso | KPIs com linha de base, período, denominador e fonte; comparação antes/depois quando houver piloto válido |
| Riscos transversais | Dado incorreto, vieses, informação confidencial em prompts, inconsistências não explicadas e decisões automáticas sem autorização |
| Governança e supervisão | Segregação de funções, controle de acesso, trilhas de auditoria, revisão humana e retenção adequada; política completa na Rota 0 — Etapa 3 |
| Limite do protótipo | Demonstração local com dados sintéticos e cálculos auditáveis; sem conexão real ao Serasa, a ERP, a serviços bancários ou a clientes |

## 4. AI Canvas por oportunidade

### C01 — Assistente de pré-triagem de propostas e pedidos B2B

- **Problema:** proposta chega por e-mail/PDF, com campos incompletos e digitação manual; triagem média de 40 minutos/pedido e aprovação retida por até 48 horas (E-OP-01; processo AS-IS, passos 1–4).
- **Objetivo:** transformar documentos em um checklist estruturado e facilitar encaminhamento de exceções com justificativas, sem decidir o crédito.
- **IA classificada:** **Generativa**, para interpretar trechos de documentos, estruturar campos e explicar pendências; validações de CNPJ, códigos de produto e regras de alçada são **determinísticas**.
- **Entradas necessárias:** PDF autorizado, cadastro sintético de cliente, catálogo de produtos e regras formalizadas. No kit atual **não existe coleção completa de propostas individuais para medir precisão do extrator**.
- **Saídas esperadas:** rascunho de dados do pedido, campos ausentes, justificativas e indicação de qual pessoa deve conferir.
- **Human-in-the-Loop:** assistente verifica os campos extraídos e gerente financeiro aprova crédito conforme regras vigentes; notas fiscais e expedição só após validação. IA não acessa portal de crédito real nem toma decisão de crédito.
- **KPIs de piloto:** tempo de triagem por pedido (minutos; baseline documental ~40), percentual de campos com correção humana, taxa de devolução por incompletude, tempo até encaminhamento à aprovação. Medir usando amostra de pedidos com cronômetro e dupla conferência.
- **Riscos/mitigações:** extração equivocada → exigir evidência por campo; prompt injection em PDFs → tratar texto como dado não confiável; exposição de informações → dados sintéticos/anonimizados e controle de acesso.
- **Maturidade:** proposta de caso de uso; **não implementado**, sem teste de acurácia.

### C02 — Conciliação financeira e detecção de divergências

- **Problema:** três planilhas não sincronizadas com ERP, fechamento de 7 dias versus meta de 2; dados do mock apresentam diferença de R$ 1,1 milhão entre DRE e consolidação por produtos (E-OP-03; E-FIN-01).
- **Objetivo:** consolidar demonstrativos reproduzíveis, sinalizar variações e produzir evidências que ajudem a Controladoria a investigar divergências.
- **IA classificada:** **Tradicional/não generativa como evolução proposta** para classificação estatística de anomalias quando houver amostra suficiente. **No MVP atual, o motor é exclusivamente analítica determinística/regras e não deve ser anunciado como modelo de IA treinado.** O ChatGPT presta apoio à análise textual, sem substituir os cálculos.
- **Entradas:** DRE trimestral, receita por produto e indicadores de gargalos, com proveniência e versão.
- **Saídas esperadas:** relatórios, discrepâncias DQ-001 a DQ-004, painel orçado versus realizado e parecer preliminar sujeito à revisão.
- **Human-in-the-Loop:** Controller valida mapeamento contábil, base de comparação, classificação das divergências e conclusões; sem ajuste contábil automático.
- **KPIs:** tempo de preparação/fechamento (baseline 7 dias úteis), percentagem de itens conciliados, número de divergências abertas/fechadas com evidência, taxa de falso alerta. O dashboard pode mostrar a linha de base, **não uma economia alcançada**.
- **Riscos/mitigações:** mistura de escopos ou dupla contagem → contrato de indicadores e bloqueio de agregação indevida; alterações manuais → manifesto/hash, arquivos derivados e testes automatizados.
- **Maturidade:** **fundação técnica implementada e validada**: 48 verificações internas e 6 testes de base; reconciliação cruzada ainda pendente.

### C03 — Alerta preditivo de risco de atraso e custo logístico

- **Problema:** fretes/reentregas acima das metas, expedições atrasadas e custo logístico acima do orçamento (E-FIN-03; E-FIN-04; E-OP-02).
- **Objetivo:** no futuro, estimar risco de atraso/reentrega *antes* do embarque, permitindo priorização preventiva pela equipe logística.
- **IA classificada:** **Preditiva**, com modelo estatístico/ML supervisionado **somente após aquisição de histórico granular rotulado**.
- **Entradas adicionais exigidas:** pedidos históricos por evento, datas de aprovação/coleta/entrega, transportadora, rota, modalidade CIF/FOB, SKU, custos e rótulo de atraso/reentrega. **O Mock Data Kit, por si só, não sustenta treinamento e validação do modelo**.
- **Saídas esperadas:** risco por pedido, principais fatores correlacionados, alerta e recomendação de checagem humana.
- **Human-in-the-Loop:** analista de logística decide priorização e transportadora; não bloquear embarques ou alterar frete automaticamente.
- **KPIs futuros:** recall de atrasos, precisão dos alertas, diferença de custo por pedido e reentrega por 100 pedidos. Definir split temporal e métricas antes de treinar, com avaliação contra baseline sem ML.
- **Riscos/mitigações:** viés e vazamento temporal → avaliação por período e revisão amostral; dados insuficientes → **não apresentar previsões como confiáveis**.
- **Maturidade:** **hipótese de médio prazo**, não incluída na versão funcional de novembro.

## 5. Encaminhamento para próxima etapa

A Rota 0 — Etapa 1 cumpre: três oportunidades, classificação de tecnologia e papéis de revisão humana. Para a **Rota 0 — Etapa 2**, construir a Matriz Esforço × Impacto com critérios explícitos (benefício, viabilidade de dados, integração, riscos e adoção), custos declarados e metas diferenciadas de observações reais. **Nenhuma nota da matriz foi atribuída ainda.**

## 6. Limitações e premissas

1. Os números são do contexto sintético do challenge, não de implantação real.
2. Os dados de quatro trimestres não permitem afirmar desempenho de uma predição de logística.
3. O desvio de R$ 1,1 milhão é reconciliação pendente, sem causa estabelecida.
4. Não somar R$ 1,36 milhão de excesso de frete, R$ 515 mil de reentregas e estimativas operacionais sem examinar sobreposições.
5. O protótipo financeiro é determinístico; o ChatGPT atua como apoio na preparação dos artefatos e na interpretação, não como fonte contábil de verdade.
6. As políticas internas reais, regras de alçada, volumes de pedidos transacionados e custos de implementação não constam integralmente no kit; exigem validação antes de ROI.

## 7. Aceite desta etapa

- [x] Três oportunidades distintas e com vínculo ao contexto do negócio.
- [x] Tipos generativa, tradicional e preditiva explicitados sem fingir implantação de ML.
- [x] Papel de validação humana descrito em cada oportunidade.
- [x] Indicadores, fontes e riscos associados a cada oportunidade.
- [ ] Revisão do conteúdo no template integral do Google Docs oficial (imagem disponível apenas da capa).
- [ ] Avaliação e aprovação da Matriz Esforço × Impacto (Rota 0 — Etapa 2).
