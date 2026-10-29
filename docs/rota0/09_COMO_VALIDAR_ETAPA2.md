# Instalação incremental — Rota 0 Etapa 2

Este ZIP acrescenta **somente arquivos novos**; não substitui a Etapa 1, scripts de auditoria, arquivos originais nem CSVs derivados.

1. Baixe `taranis-black-fase-03-rota0-etapa2.zip` em Downloads.
2. No terminal do VS Code/WSL2, na raiz do repositório, execute:

```bash
cd ~/Repositorios/taranis-black-ai-for-business
unzip -n /mnt/c/Users/USER/Downloads/taranis-black-fase-03-rota0-etapa2.zip -d .
python scripts/check_route0_etapa2.py
python -m unittest discover -s tests -v
python scripts/check_route0.py
bash scripts/check_project.sh
```

> Ajuste o caminho de Downloads se o nome do usuário do Windows ou nome baixado forem diferentes. Não use `unzip -o`.

## Critérios de aceite

- [ ] Três casos vinculados à Etapa 1 e pontuações dentro da escala 1–5.
- [ ] Pesos somam 100% em cada eixo; notas e razões rastreáveis.
- [ ] C02 aparece no quadrante de alto impacto e baixo esforço **no MVP**, não automaticamente em produção.
- [ ] C03 permanece bloqueado por dados insuficientes.
- [ ] ROI apenas como cenários hipotéticos e condicionais; C02 não recebe ROI inventado.
- [ ] KPIs separam baselines, metas do kit, hipóteses e N/D.
- [ ] Revisão humana e gestão de mudanças contempladas.
- [ ] Testes da Fase 1 e da Etapa 1 continuam aprovados.

## Próximo passo

Rota 0 — Etapa 3: política corporativa de IA responsável, LGPD, viés, responsabilidades e auditoria; depois Rota 4 SIPOC e Ishikawa. A entrega final será no Google Docs oficial, com link do vídeo demonstrativo.
