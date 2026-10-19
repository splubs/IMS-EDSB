# %% [markdown]
# # 01 — Data Audit: Telco Customer Churn
# A versão .py é o ficheiro principal para GitHub. Gere o .ipynb localmente usando Jupytext.

# %% [markdown]
# # 01 — Data Audit: Telco Customer Churn
#
# **Objetivo:** confirmar granularidade, exclusões, codificações e potenciais fugas de informação. Este notebook é exploratório; não constitui validação de um modelo preditivo.

# %%
from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "src" / "data.py").exists())
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from src.data import load_tables, validate_tables, load_customers, load_core_population
print("Root:", ROOT)

# %% [markdown]
# ## 1. Ficheiros de origem e testes de consistência
# O ficheiro Population é unido por **Zip Code**; as outras quatro tabelas são unidas por **Customer ID**.

# %%
tables=load_tables()
validate_tables(tables)
pd.DataFrame({"rows":{k:len(v) for k,v in tables.items()},"columns":{k:len(v.columns) for k,v in tables.items()}})

# %%
full=load_customers()
core=load_core_population()
print("Após join:", full.shape, "| sem Joined:",core.shape)
print("Churn rate core:", round(core["Customer Status"].eq("Churned").mean()*100,2),"%")
full["Customer Status"].value_counts()

# %% [markdown]
# ## 2. Distinguir categorias reais de valores em falta
# O texto `None` em `Offer` e `Internet Type` é uma categoria válida; nunca converter automaticamente em NaN.

# %%
display(tables["services"]["Offer"].value_counts())
display(tables["services"]["Internet Type"].value_counts())
print("Campos de churn pós-evento vazios:", (core["Churn Category"]=="").sum())

# %% [markdown]
# ## 3. Taxa observada de churn por tipo de contrato
# Associação descritiva, não evidência causal sobre mudar contratos.

# %%
rates=(core.assign(Churn=core["Customer Status"].eq("Churned").astype(int)).groupby("Contract")["Churn"].agg(["count","mean"]).sort_values("mean",ascending=False))
display(rates)
ax=(rates["mean"]*100).plot.bar(rot=0,figsize=(8,4),ylabel="Churn (%)",title="Churn por tipo de contrato (Q3; associação observada)")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 4. Risco de data leakage: Satisfaction Score
# A distribuição desta variável pode ter sido observada depois do churn. Por enquanto **não** a incluir no modelo.

# %%
display(pd.crosstab(core["Satisfaction Score"],core["Customer Status"]))
print("Outcomes duplicados?", (core["Churn Value"] == core["Customer Status"].eq("Churned").astype(int)).all())

# %% [markdown]
# ## 5. Próximos passos
# 1. Determinar o instante de decisão: informação disponível **antes** do abandono.
# 2. Completar o inventário e a auditoria temporal de variáveis.
# 3. Definir modelo baseline com split treino/validação/teste estratificado.
# 4. Só depois comparar modelos e desenhar o critério de priorização de retenção.
#
# **Limitação:** não existem vários períodos históricos para testar comportamento futuro; não inferir desempenho prospectivo nem impacto causal.
