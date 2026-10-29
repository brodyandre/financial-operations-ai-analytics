# Rota 4 Etapa 1 — Verificação, evidências e vídeo

## Aceite técnico

```bash
python scripts/check_rota4_etapa1.py
python -m unittest discover -s tests -v
bash scripts/check_project.sh
```

A primeira rotina valida consistência dos cinco passos do AS-IS, 5 linhas SIPOC, seis grupos 6M, cinco baselines de gargalos, bloqueios de segurança e presença de artefatos. Os testes são **estruturais**; não demonstram ganho operacional.

## Evidências recomendadas

| Evidência | Como capturar | Uso no relatório/vídeo |
|---|---|---|
| EV-R4-01 | Print do fluxo AS-IS Mermaid renderizado no GitHub/VS Code | Gargalos e espera |
| EV-R4-02 | Print da matriz SIPOC | Visão ponta a ponta |
| EV-R4-03 | Print do Ishikawa Mermaid renderizado | Causas em 6M |
| EV-R4-04 | Saída do `check_rota4_etapa1.py` | Consistência técnica |
| EV-R4-05 | Relatório `reports/rota4_etapa1_resumo.md` | Baselines e recomendações |

## Script para o vídeo (trecho de aproximadamente 55 segundos)

> O processo atual possui cinco passagens manuais: envio da proposta por e-mail, consulta de crédito, solicitação de aprovação, espera de até 48 horas e faturamento com transmissão manual ao centro de distribuição. O SIPOC identifica os responsáveis e as entradas e saídas; o Ishikawa organiza evidências nos seis fatores do problema. A proposta é padronizar dados, criar rastreabilidade e apoiar a triagem com IA, sempre preservando a revisão humana. A redução de tempo ainda não foi comprovada; estamos apresentando um desenho de melhoria, não uma implantação.

**Cuidado com a entrega:** a capa do template oficial é conhecida, mas o template completo ainda não foi fornecido. Antes da submissão, copiar os resultados para os campos exigidos no Google Docs e confirmar regras da etapa opcional e do link do vídeo.
