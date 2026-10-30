# Experimento DQ-001 — método e limitações

**Objetivo:** demonstrar se a regra `abs(DRE − Produtos) > R$ 0,01` sinaliza divergências introduzidas em um conjunto sintético conhecido.

**Desenho:** 20 casos fixos e rotulados manualmente, com oito situações compatíveis com a tolerância e doze divergências acima da tolerância (positivas e negativas). A base usada é hipotética; o Mock Data Kit e seus CSVs não são alterados. O código não utiliza ML nem ChatGPT para classificar os casos.

**Métricas:** verdadeiro positivo, falso positivo, verdadeiro negativo, falso negativo, precisão e sensibilidade (*recall*) no conjunto de teste.

A regra é simples e os casos foram **projetados para exercitá-la**, portanto um resultado perfeito não demonstra eficácia geral em bases financeiras reais. Não há amostragem probabilística, dados transacionais, falhas de classificação mapeadas ou comparação de tempo manual versus automatizado. Não extrapolar os resultados para economia, ROI, produtividade ou qualidade de um modelo de IA.

**Reprodução:** `python scripts/check_showme.py` grava `reports/showme_experimento_sintetico.json` localmente. O arquivo é evidência reproduzível e não deve ser incluído no commit automaticamente.
