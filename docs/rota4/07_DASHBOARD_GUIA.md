# Rota 4 — Dashboard demonstrativo | Financial Operations Intelligence

**Data de referência:** 29/10/2026 · **Prazo do challenge:** 08/11/2026 · **Natureza:** demonstração local offline com dados sintéticos. 

## Objetivo e limites

A interface Streamlit apresenta DRE (orçado e realizado), inconsistências interabas, gargalos operacionais e uma simulação de capacidade hipotética. Ela **não é um ERP, não faz integração, não toma decisões de crédito, não faz previsão com aprendizado de máquina e não gera economia automaticamente**.

- **C02 — piloto prioritário:** conciliação e qualidade financeira com cálculos determinísticos; ChatGPT apoia interpretação de forma externa e consultiva.
- **C01 — segundo piloto condicionado:** simulador de triagem de propostas B2B, com premissas ilustrativas e nenhuma implantação.
- **C03 — bloqueado:** ausência de histórico rotulado de pedidos e eventos logísticos.

## Pré-requisitos

- VS Code, WSL2 (Ubuntu), Python 3.12 e `.venv` do projeto.
- Projeto em `~/Repositorios/taranis-black-ai-for-business`, branch `main`.
- Nenhuma chave de API, conta cloud ou licença paga é necessária.

## Instalar apenas dependências do dashboard

```bash
cd ~/Repositorios/taranis-black-ai-for-business
source .venv/bin/activate
python -m pip install -r requirements-dashboard.txt
```

Se `.venv` ainda não existir, criar com `python3 -m venv .venv` e ativar.

## Verificar o núcleo auditável (sem bibliotecas de visualização)

```bash
python scripts/check_dashboard.py
python -m unittest discover -s tests -v
bash scripts/check_project.sh
```

## Executar a aplicação

```bash
python -m streamlit run dashboard/app.py --server.address 127.0.0.1
```

Abrir **http://localhost:8501** no navegador do Windows. Encerrar com `Ctrl+C` no terminal. A aplicação só lê CSVs locais e configurações do projeto; não altera o Mock Data Kit nem realiza requisições a serviços de IA.

## Roteiro de inspeção manual antes de gravar vídeo

1. **Visão executiva:** receita realizada de R$ 48,50 mi, EBITDA de R$ 5,77 mi; variar período para T3 e conferir os KPIs (os gráficos permanecem com T1–T4).
2. **Análise financeira:** comparar orçado/realizado, inspecionar fretes (R$ 1,36 mi de desvio desfavorável), PDD (R$ 670 mil) e reentregas (R$ 515 mil).
3. **Qualidade de dados:** mostrar DQ-001, diferença anual realizada DRE vs produtos de R$ 1,10 mi; explicar que não é perda de receita.
4. **Operações:** mostrar gargalos operacionais, metas de SLA e priorização C02 → C01 condicionado → C03 bloqueado.
5. **Cenários & ChatGPT:** ajustar de 100 para 200 pedidos/mês e comprovar que o ROI é rotulado como hipotético. Apresentar o briefing pronto para copiar ao ChatGPT.

**Antes de marcar a fase como concluída, conferir a interface visualmente no navegador** (CSS, gráficos, tabelas e navegação), pois os testes automatizados verificam cálculos e integridade, não renderização web.

## Proveniência e controles

- DRE: `data/derived/dre_trimestral.csv`, aba `DRE_Trimestral_Orcado_Real`, fonte `05_Financas_Orcado_vs_Realizado.xlsx`.
- Produtos: `data/derived/receita_por_linha.csv`, aba `Receita_por_Linha_Produto`.
- Operações: `data/derived/gargalos_operacionais.csv`, aba `Gargalos_Operacionais_Custos`.
- Hash da origem, extração e qualidade: `data/derived/source_manifest.json`, `src/taranis_black/audit.py`.
- Priorização e cenário C01: `configs/prioritization_2026.json` e `src/taranis_black/prioritization.py`.
- Política e revisão humana: `docs/rota0/10_POLITICA_USO_IA_LGPD.md`.
- Esta implementação **não** recalcula os efeitos de gargalos sobre a DRE, pois pode ocorrer sobreposição e dupla contagem.

## Evidências a capturar

- Screenshot 01: dashboard executivo com receita/EBITDA.
- Screenshot 02: despesas desfavoráveis.
- Screenshot 03: exceção DQ-001 e status de reconciliação.
- Screenshot 04: cenários C01 com premissas visíveis.
- Vídeo MP4 de 3 a 5 minutos: problema → controles → demonstração → recomendações, sem alegar ganhos realizados.

## Problemas comuns

- `No module named streamlit`: ativar `.venv` e executar `python -m pip install -r requirements-dashboard.txt`.
- `No module named taranis_black`: executar o comando **a partir da raiz** do projeto (o app configura `sys.path` para `src/`).
- Porta 8501 ocupada: `python -m streamlit run dashboard/app.py --server.port 8502`.
- Erro de dados: executar `bash scripts/check_project.sh` antes de alterar qualquer arquivo.
