# Instalação incremental — Show Me Project Ready

Requisitos: repositório local `~/Repositorios/taranis-black-ai-for-business` com dashboard já funcionando, Python no `.venv`. **Não sobrescrever `dashboard/app.py`, `dashboard/theme.css` nem os arquivos anteriores.**

1. Extrair ZIP com `unzip -n` na raiz do projeto.
2. Executar `python scripts/enable_showme.py` — altera apenas o menu e a rota em `dashboard/app.py`, com backup para `/tmp`.
3. Executar `python scripts/check_showme.py`.
4. Executar `python -m unittest discover -s tests -v` e `bash scripts/check_project.sh`.
5. Reabrir ou atualizar Streamlit e conferir a seção **Investigação DQ-001** nas quatro abas.
6. Fazer `git status --short` e `git diff --check`. **Não commitar ainda:** revisar visualmente primeiro.

Se o instalador acusar estrutura inesperada, **não tentar substituições manuais automáticas**. Informe a saída do erro; o patch terá sido interrompido e o aplicativo anterior será preservado.

Arquivos incrementais: `src/taranis_black/{investigation.py, investigation_ui.py, dq_experiment.py}`, `scripts/{enable_showme.py, check_showme.py}`, `tests/test_showme.py` e `docs/showme/*`.

A execução dos testes cria apenas um relatório local em `reports/`.
