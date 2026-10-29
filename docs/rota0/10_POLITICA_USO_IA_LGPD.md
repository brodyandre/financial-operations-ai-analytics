# Rota 0 — Etapa 3 | Política Corporativa de Uso Responsável de IA

**Empresa:** Taranis Black (cenário simulado da Alura ONE G11)\
**Versão:** 0.1 — proposta consultiva para aprovação executiva (29/10/2026)\
**Status:** RASCUNHO. Não é política vigente e não comprova conformidade jurídica ou implantação.\
**Abrangência proposta:** colaboradores, prestadores e fornecedores que atuem em nome da empresa.\
**Aplicabilidade do challenge:** exclusivamente dados sintéticos do Mock Data Kit e análises locais; não há acesso ao ERP real ou clientes reais.

## 1. Propósito e princípios

Orientar a adoção de IA como **apoio**, e não substituição de responsabilidade profissional. Princípios: finalidade específica, necessidade e minimização, transparência, segurança, prevenção, não discriminação, qualidade, prestação de contas e revisão humana proporcional ao impacto. Antes de utilizar dados pessoais, Privacidade/Jurídico define **hipótese legal, finalidade, necessidade e agentes de tratamento** caso a caso; não presumir consentimento como base legal universal.

## 2. Uso permitido — sujeito à homologação

- Analisar demonstrativos e registros **sintéticos ou adequadamente autorizados**, com fórmulas reproduzíveis e fontes identificadas.
- Propor correções de cadastro, elaborar **rascunhos** de documentos e resumir divergências para validação por pessoa habilitada.
- Auxiliar pré-triagem de pedidos (C01) com checklist; não autorizar crédito, emissão fiscal ou expedição.
- Produzir painéis de DRE e alertas de qualidade (C02), mantendo divergências abertas até validação da Controladoria.
- Realizar pesquisas e testes de IA (C03) somente depois de aprovação de dados, metodologia, monitoramento e riscos; **C03 permanece bloqueado** no projeto atual.

## 3. Uso proibido

1. Tomar **decisões de crédito autônomas**; executar cobranças, pagamentos, alterações contábeis, emissão fiscal ou liberação de pedidos sem autoridade humana.
2. Inserir informações pessoais, dados sensíveis, documentos confidenciais, segredos comerciais ou credenciais em contas e serviços de IA não homologados.
3. Criar perfis discriminatórios, inferir atributos sensíveis sem fundamento legítimo, manipular pessoas ou ocultar uso significativo de IA.
4. Declarar resultados simulados como ganho financeiro realizado, ou anunciar modelos preditivos não treinados como se estivessem em produção.
5. Remover trilhas de auditoria, alterar dados de origem para forçar conciliação ou reutilizar dados para finalidade incompatível sem avaliação.

## 4. Governança de dados e LGPD

**Antes de iniciar uso com dados pessoais reais:** (a) inventário de dados e responsáveis, (b) finalidade e hipótese legal pertinentes, (c) minimização e classificação dos dados, (d) definição de acessos e retenção, (e) avaliação contratual do provedor e eventual transferência internacional, (f) avaliação de impacto/riscos e RIPD quando cabível, (g) canal para direitos dos titulares e (h) autorização formal. **Anonimização efetiva** é diferente de pseudonimização: reidentificação possível mantém riscos e pode manter a aplicabilidade da LGPD. Nenhum desses passos é considerado cumprido pela mera execução do notebook/script local.

**Dados financeiros vs. pessoais:** demonstrativos agregados podem não conter dados pessoais; faturas, cadastro B2B e informações de contato podem identificar pessoas naturais e exigem avaliação específica. A base do challenge é sintética e não autoriza inferir políticas reais da Taranis Black.

## 5. Controles técnicos e de operação

- `G-01` Inventário de origem, propósito e minimização.
- `G-02` Definição documentada de finalidade/hipótese legal.
- `G-03` Segregação de funções e proibição de ações autônomas materiais.
- `G-04` Revisão humana, contestação e botão/processo de interrupção.
- `G-05` Proveniência e integridade de cálculos (hash e testes).
- `G-06` Controle de acesso mínimo, segredos protegidos, plataformas homologadas.
- `G-07` Validação de qualidade, erros e vieses quando aplicável.
- `G-08` Retenção, descarte, segurança dos registros e trilha de auditoria.
- `G-09` Resposta a incidentes e avaliação de necessidade de notificação.
- `G-10` Due diligence de fornecedores e transferências internacionais.
- `G-11` Procedimentos para direitos dos titulares.
- `G-12` Comitê de governança, monitoramento e controle de mudanças.

A especificação estruturada dos controles e sua responsabilidade está em `configs/governance_controls_2026.json`.

## 6. Gestão de incidentes

1. Interromper a operação afetada, impedir agravamento e preservar evidências e logs relevantes.
2. Acionar imediatamente TI/Segurança e Privacidade/Encarregado, que apoiam o controlador na análise do evento, tipo de dado e risco/dano relevante aos titulares.
3. Decidir, documentar e executar as comunicações legalmente exigidas. **Quando o incidente com dados pessoais puder acarretar risco ou dano relevante, o controlador deve observar o prazo de três dias úteis para comunicação à ANPD e aos titulares, ressalvadas disposições específicas e particularidades legais.** A contagem e as exceções devem ser avaliadas por Jurídico/Privacidade a partir do conhecimento pertinente do evento. Um aviso interno deve ocorrer imediatamente; ele não substitui comunicação legal.
4. Corrigir a causa, realizar teste de retorno, revisar controles e registrar aprendizado. Registros de incidentes com dados pessoais devem ser mantidos pelo prazo normativo aplicável (o RCIS prevê pelo menos cinco anos).

**Referência oficial:** Resolução CD/ANPD nº 15/2024 e orientações da ANPD: https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis e https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-aprova-o-regulamento-de-comunicacao-de-incidente-de-seguranca

## 7. Supervisão e alçadas por caso

| Caso | Operação permitida no MVP | Aprovação humana obrigatória | Gate de produção |
|---|---|---|---|
| C01 — Pré-triagem | Rascunho e checklist de proposta sintética | Assistente de Vendas e gestor de Crédito | PDF real, privacidade e taxa de erro validados |
| C02 — Conciliação | Cálculos determinísticos, DRE, alertas de divergência | Controller confirma conciliação e apresentação | Regras contábeis, ERP e autorizações homologados |
| C03 — Preditivo logístico | Apenas desenho do caso | Logística e Engenharia de Dados | **Bloqueado:** histórico rotulado, testes temporais e aprovação |

## 8. Prestação de contas e revisão da política

O comitê proposto deve receber registros de riscos, auditoria dos indicadores, decisões de aceite e incidentes. A revisão é trimestral ou extraordinária em mudança material de finalidade/modelo/fornecedor. Sem assinatura de patrocinador e avaliação jurídica, este documento permanece uma proposta.

## 9. Referências normativas e limitações

- LGPD (Lei nº 13.709/2018): princípios, bases legais, direitos, segurança e prestação de contas. Ver texto oficial: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- ANPD, página de normas vigentes: https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/
- Resolução CD/ANPD nº 15/2024 (comunicação de incidentes): https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis
- Documento educacional e modelo de governança **não constituem parecer jurídico**. Políticas internas reais e nomes de responsáveis não foram disponibilizados.
