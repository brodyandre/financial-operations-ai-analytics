# Taranis Black — AI for Finance & Operations

Challenge ONE G11 / Alura | **Rota 0 obrigatória + Rota 4 Finanças e Operações** | Entrega 08/11/2026

Projeto de consultoria de IA sobre empresa simulada. O objetivo é diagnosticar gargalos financeiros/operacionais, priorizar oportunidades de IA com critérios executivos, propor governança e demonstrar uma solução enxuta apoiada pelo **ChatGPT**. Não há integração com Claude.

## Status — 29/10/2026

- [x] Inventário do material financeiro e do fluxo operacional.
- [x] Extração controlada dos valores de três abas do XLSX para CSV, com SHA-256 da fonte.
- [x] Auditoria inicial de DRE, receitas por produto, despesas e inconsistências.
- [x] Testes automatizados da camada analítica.
- [ ] Rota 0: AI Canvas, priorização e política de IA.
- [ ] Rota 4: SIPOC, Ishikawa, plano de melhoria.
- [ ] Dashboard interativo com ChatGPT + VS Code.
- [ ] Gravação do vídeo demo e relatório executivo final.

## Começando no VS Code / WSL2

Abra esta pasta no WSL2 (`code .`). O script inicial utiliza somente a biblioteca padrão do Python 3.12; não há dependências pagas nem necessidade de credenciais.

```bash
cd ~/Repositorios/taranis-black-ai-for-business
python3 -m venv .venv
source .venv/bin/activate
PYTHONPATH=src python -m taranis_black.audit
python -m unittest discover -s tests -v
```

A execução cria, em `reports/`:

- `audit_result.json`: verificações e achados estruturados.
- `auditoria_financeira_inicial.md`: análise executiva legível, com pendências e fontes.

Se desejar validar a integridade contra o XLSX original:

```bash
PYTHONPATH=src python -m taranis_black.audit --source-xlsx "data/source/05_Financas_Orcado_vs_Realizado.xlsx"
```

**Não edite o XLSX original.** Os arquivos CSV de trabalho estão em `data/derived/`.

## Limites e interpretação

- Dados: cenário **sintético** fornecido pela Alura.
- Desvios de despesas não são economias alcançadas.
- Dados de quatro trimestres não sustentam alegação de precisão preditiva.
- Diferenças entre fontes permanecem abertas até reconciliação documentada.
- Concessões de crédito, lançamentos e decisões financeiras exigem revisão humana.
- O dashboard ainda é uma etapa futura; esta entrega inicial é a **fundação auditável**.

## Organização

- `data/derived/`: cópias CSV dos valores (preservando aba/linha de origem).
- `data/source/`: pasta local para originais, excluída de versionamento.
- `src/taranis_black/audit.py`: cálculos e validações determinísticos.
- `tests/`: testes de regressão.
- `reports/`: JSON + relatório Markdown gerados.
- `docs/`: escopo, requisitos, cronograma e próximos entregáveis.
- `evidence/`: capturas e links para a entrega.

## Submissão

O **Google Docs oficial** é a entrega na Alura. O repositório e o vídeo demo (MP4 ou link não listado) serão evidências complementares, referenciadas no documento. Prazo: 08/11/2026; code freeze proposto: 06/11/2026.
