# Instalação incremental — Fase 2 / Rota 0 Etapa 1

Pacote **incremental**: contém somente novos arquivos. Não sobrescreve scripts existentes, relatórios gerados, banco de dados ou dados derivados.

No diretório raiz `~/Repositorios/taranis-black-ai-for-business`, descompactar o ZIP e conferir:

```bash
python -m unittest discover -s tests -v
python scripts/check_route0.py
bash scripts/check_project.sh
```

## Critérios para revisão humana

1. Confirmar que três casos estão vinculados a dores distintas e mensuráveis.
2. Conferir as ressalvas de C02 (regras determinísticas não são um modelo de IA treinado) e C03 (sem treinamento preditivo por insuficiência de dados).
3. Aprovar a redação do papel de cada agente humano (assistente, gerente financeiro, Controller e logística).
4. Conferir fonte, baseline e natureza de cada afirmação antes de migrar ao Google Docs.
5. Aguardar o template integral para adequar redação aos campos exatos da Alura.

Próximo pacote planejado: Rota 0 Etapa 2 — matriz Esforço x Impacto, KPIs, ROI com hipóteses e gestão de mudança.
