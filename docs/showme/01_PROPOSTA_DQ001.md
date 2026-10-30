# Show Me Project Ready — DQ-001

**Challenge:** Taranis Black, Alura ONE G11 · **Rota 4** · **Prazo:** 08/11/2026.

## Proposta de valor

Demonstrar um fluxo completo de decisão **assistida**, não autônoma:

1. Os dados sintéticos são lidos pelo motor Python já auditado.
2. A diferença entre DRE e total por produto é detectada e apresentada.
3. A tela **Investigação DQ-001** mostra valores, fontes e hipóteses ainda não confirmadas.
4. Um briefing é copiado **manualmente** para o ChatGPT. A resposta exige conferência humana.
5. Uma área responsável é sugerida para a investigação; o encaminhamento pode ser exportado como JSON demonstrativo.
6. A exceção continua pendente até que documentação autorize sua conciliação.

## Evidências do Mock Data Kit

| Visão anual | DRE | Produtos | Diferença |
|---|---:|---:|---:|
| Realizada | R$ 48.500.000 | R$ 47.400.000 | **R$ 1.100.000** |
| Orçada | R$ 48.600.000 | R$ 48.000.000 | **R$ 600.000** |

**Fonte:** arquivo 05, abas `DRE_Trimestral_Orcado_Real` e `Receita_por_Linha_Produto`, conforme manifesto SHA-256 em `data/derived/source_manifest.json`.

O valor **não representa perda, fraude, recuperação de receita ou economia realizada**. A causa é desconhecida. Os dados são sintéticos e não estão ligados a ERP ou sistemas reais.

## Controle de decisão

- O experimento não tenta reconciliar automaticamente a diferença.
- O ChatGPT não atua dentro do Streamlit e não realiza consultas a sistemas.
- O registro exportável é apenas um encaminhamento demonstrativo, e não uma aprovação contábil.
- Nenhuma informação de clientes deve ser inserida no campo de nota ou no prompt.
- A política de governança permanece **proposta**, não implantada na empresa simulada.

## Aceite técnico

- O fluxo anterior do Streamlit e os testes originais continuam funcionando.
- `scripts/enable_showme.py` executa patch idempotente e cria backup em `/tmp`.
- `scripts/check_showme.py` valida os valores, a rastreabilidade, o controle humano e o experimento.
- A revisão visual de todas as abas ainda é necessária no navegador.
