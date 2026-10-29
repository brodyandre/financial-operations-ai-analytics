# Rota 0 — Etapa 3 | Comitê de Governança, Auditoria e Responsabilidades

**Comitê proposto, não constituído na empresa simulada.** Os membros são papéis genéricos e dependem de designação e aceite da liderança.

## Estrutura e cadência sugeridas

- Patrocinador executivo (CEO ou delegado): direção estratégica e recursos.
- Controladoria e gerência Financeira: homologação de indicadores e alçadas.
- TI/Segurança: acessos, arquitetura, incidentes e fornecedor.
- Privacidade/Encarregado + Jurídico: bases legais, tratamento, direitos e notificações.
- Área usuária (Vendas, Logística): validação da operacionalização.
- **Cadência:** quinzenal durante piloto, mensal após estabilização, extraordinária em incidente.

## RACI proposto

**R** executa; **A** responde/aprova; **C** consultado; **I** informado. Cada decisão deverá ter um **A** definido pela empresa na implantação real.

| Atividade | Executivo | Controladoria | TI/Segurança | Privacidade/Jurídico | Área usuária |
|---|---|---|---|---|---|
| Política de IA e expansão | A | C | C | R | I |
| Finalidade e hipótese legal | I | C | C | A/R | C |
| Homologação do KPI e conciliação C02 | I | A/R | C | C | I |
| Alçada de crédito C01 | I | A | C | C | R |
| Testes e controles técnicos | I | C | A/R | C | C |
| Resposta técnica a incidentes | I | I | A/R | C | C |
| Decisão legal de comunicar incidente (controlador) | A | I | C | R | I |
| Preparação de dados para C03 | I | C | C | C | A/R |

**Nota de papéis:** as atribuições acima não substituem a definição formal de quem age em nome do controlador; a decisão de notificação depende do regime legal e de autoridades internas competentes.

## Trilha de auditoria mínima

Registrar para cada decisão de uso: ID, caso, finalidade, fonte e versão, responsável, data/hora, evidência, exceção, status de risco, aceitação/recusa e justificativa. Não registrar dados pessoais desnecessários em logs; proteger e reter pelo período definido pelas áreas competentes.

## Fluxo de mudanças e exceções

1. Solicitante registra finalidade, mudança de dado/modelo/fornecedor e ganho esperado.
2. Controladoria ou área usuária verifica benefício, integração e teste de regressão.
3. TI/Segurança e Privacidade/Jurídico examinam exposição e riscos legais.
4. Comitê aprova/rejeita com responsável e prazo; alterações de alto risco não passam tacitamente.
5. Monitorar métricas, incidentes e plano de reversão. O **C03** fica impedido de seguir sem o gate de histórico rotulado.

## Evidências para a Alura

- Política proposta: `docs/rota0/10_POLITICA_USO_IA_LGPD.md`.
- Matriz e mitigação de vieses: `docs/rota0/11_RISCOS_CONTROLES_VIES.md`.
- Registro controlado: `configs/governance_controls_2026.json`.
- Validação automatizada: `python scripts/check_route0_etapa3.py` e `python -m unittest discover -s tests -v`.
- A saída programática lista controles e riscos definidos **em proposta**; não é evidência de implementação real.
