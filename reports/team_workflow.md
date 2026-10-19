# Trabalho de equipa — GitHub e VS Code

**Fonte:** Class 3 `class_week03.py`, `README.md` da lab e recomendações específicas para o Telco.

## Acordos iniciais

- GitHub **privado**; acrescentar colegas e ambos os professores como colaboradores (indicação da aula).
- Só a branch `main` contém o trabalho revisto, e cada tarefa é feita numa branch `feature/...`.
- Usar a mesma versão principal de Python (3.13) e instalar `requirements.txt`.
- Nunca colocar `.env`, datasets, credenciais ou `models/*.joblib` no Git sem decisão explícita.
- `data/raw` fica intacto; `data/processed`, `reports/generated` e `models` são gerados pelos scripts.
- Editar notebooks como `.py` via Jupytext; `.ipynb` é produzido apenas localmente.

## Rotina antes e depois de trabalhar

```bash
git switch main
git pull origin main
git switch -c feature/data-quality
# trabalhar e testar
python -m unittest discover
git status
git add src/data.py tests/test_data.py reports/data_audit.md
git commit -m "Validate Telco joins and preserve raw categories"
git push -u origin feature/data-quality
```

Abrir Pull Request no GitHub; pedir revisão a um colega; resolver comentários; integrar na main.

## Convenção de tarefas proposta (não é requisito do guia)

| Área | Branch ilustrativa | Output |
|---|---|---|
| Business understanding | `feature/business-context` | `reports/business_brief.md` |
| Data audit & EDA | `feature/eda` | `notebooks/01_data_audit.py`, relatórios |
| Modeling | `feature/modeling` | `src/features.py`, modelos e avaliação |
| Retention strategy | `feature/retention` | Métricas top-k, análise de custos e cenários |

Todos devem rever decisões de modelação, leakage e a interpretação dos resultados; dividir por ficheiros não implica que cada pessoa fique alheada das restantes partes.
