# Validação local da Rota 0 — Etapa 3

Este pacote adiciona **somente arquivos novos** e não altera o motor de auditoria, a priorização anterior ou as planilhas originais.

No VS Code com WSL2, a partir da raiz do repositório:

```bash
python scripts/check_route0_etapa3.py
python -m unittest discover -s tests -v
python scripts/check_route0_etapa2.py
python scripts/check_route0.py
bash scripts/check_project.sh
git status --short
```

Os artefatos de saída são `reports/rota0_etapa3_result.json` e `reports/rota0_etapa3_resumo.md` (gerados e não incluídos neste ZIP). A verificação automatizada **confirma a completude estrutural da proposta**, não que os controles estejam implantados na empresa real ou que a política tenha sido aprovada.

Não comitar, publicar nem conectar dados reais antes de revisar o projeto com o usuário e autorizações aplicáveis. Conferir o novo pipeline GitHub Actions após o push. Se a versão oficial do template da Alura exigir um formato distinto, adaptar o resumo sem modificar o diagnóstico de origem.
