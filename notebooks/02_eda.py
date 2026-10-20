# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.6
#   kernelspec:
#     display_name: .venv (3.13.15)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 02 — Exploratory Data Analysis (EDA) | Telco Customer Churn
#
# **Objetivo:** identificar padrões associados ao churn para apoiar o diagnóstico de negócio e a seleção inicial de variáveis.
#
# **População:** apenas clientes `Stayed` e `Churned` (excluímos `Joined`, conforme o enunciado). Os dados representam **um único snapshot de Q3**, sem histórico temporal nem ano especificado.
#
# **Como usar:** executar as células por ordem (*Restart Kernel → Run All*). Os gráficos mostram associações, **não relações causais**.

# %% [markdown]
# ## 1. Carregar os dados
#
# Reutilizamos o código de `src/data.py` para não repetir os cinco joins. A nova coluna `Churn` representa 1 para `Churned` e 0 para `Stayed`.

# %%
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

ROOT = next(
    p for p in [Path.cwd(), *Path.cwd().parents] if (p / "src" / "data.py").exists()
)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data import load_core_population

df = load_core_population()
df["Churn"] = df["Customer Status"].eq("Churned").astype(int)

print(
    f"Clientes: {len(df):,} | Colunas: {df.shape[1]} | Taxa de churn: {df['Churn'].mean():.2%}"
)
assert df["Customer ID"].is_unique

display(
    df[
        [
            "Customer ID",
            "Customer Status",
            "Tenure in Months",
            "Contract",
            "Monthly Charge",
        ]
    ].head()
)

# %% [markdown]
# ## 2. Distribuição da variável-alvo
#
# Qual é a percentagem de clientes com churn? A *accuracy* de um modelo deve ser interpretada face à proporção de `Stayed`, e não isoladamente.

# %%
status = df["Customer Status"].value_counts().reindex(["Stayed", "Churned"])
display(
    pd.DataFrame(
        {"Clientes": status, "Percentagem (%)": (status / len(df) * 100).round(1)}
    )
)

status.plot.bar(rot=0, title="Clientes por estado (Q3)", ylabel="Número de clientes")
plt.tight_layout()
plt.show()


# %% [markdown]
# ## 3. Taxa de churn por grupo
#
# Esta pequena função será usada para evitar repetir o mesmo `groupby` em todos os gráficos. Mostra a **dimensão do grupo** e a respetiva **taxa observada de churn**.

# %%
def churn_by(group):
    result = df.groupby(group, observed=True)["Churn"].agg(["size", "mean"])
    result.columns = ["Clientes", "Churn (%)"]
    result["Churn (%)"] = (result["Churn (%)"] * 100).round(1)
    return result


# %% [markdown]
# ## 4. Tipo de contrato
#
# Pergunta de negócio: clientes com contratos mensais apresentam maior taxa de churn do que clientes com contratos de um ou dois anos?
#
# **Cuidado:** não podemos concluir que prolongar um contrato causaria uma redução do churn; pode haver seleção prévia de clientes.

# %%
contract = churn_by("Contract").sort_values("Churn (%)", ascending=False)
display(contract)
contract["Churn (%)"].plot.bar(
    rot=0, title="Churn por tipo de contrato", ylabel="Churn (%)"
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 5. Antiguidade do cliente (*Tenure*)
#
# Agrupamos os meses de antiguidade em intervalos interpretáveis para identificar fases da relação com maior churn observado.
#
# **Nota temporal:** a antiguidade foi registada no fim do trimestre; a sua utilização preditiva exigirá validação do momento de medição.

# %%
tenure_band = pd.cut(
    df["Tenure in Months"],
    bins=[0, 6, 12, 24, 48, 72],
    labels=["1–6", "7–12", "13–24", "25–48", "49–72"],
)
tenure = churn_by(tenure_band)
display(tenure)
tenure["Churn (%)"].plot.bar(
    rot=0, title="Churn por antiguidade", xlabel="Meses", ylabel="Churn (%)"
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 6. Mensalidade (*Monthly Charge*)
#
# Dividimos os clientes em cinco grupos com dimensão semelhante (*quintis*) para verificar a associação entre o valor mensal e o churn.
#
# Os intervalos são calculados a partir dos dados, em vez de escolhidos arbitrariamente.

# %%
charge_band = pd.qcut(df["Monthly Charge"], q=5, duplicates="drop")
charges = churn_by(charge_band)
display(charges)
charges["Churn (%)"].plot.bar(
    rot=25,
    title="Churn por quintil de mensalidade",
    xlabel="Monthly Charge (USD)",
    ylabel="Churn (%)",
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 7. Tipo de internet e método de pagamento
#
# Comparamos duas características comerciais. O valor literal `None` em `Internet Type` significa que o cliente **não tem serviço de internet**; não é um dado em falta.

# %%
internet = churn_by("Internet Type").sort_values("Churn (%)", ascending=False)
display(internet)
internet["Churn (%)"].plot.bar(
    rot=0, title="Churn por tipo de internet", ylabel="Churn (%)"
)
plt.tight_layout()
plt.show()

# %%
payment = churn_by("Payment Method").sort_values("Churn (%)", ascending=False)
display(payment)
payment["Churn (%)"].plot.bar(
    rot=0, title="Churn por método de pagamento", ylabel="Churn (%)"
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 8. Perfil etário
#
# Analisamos faixas etárias em vez de cada idade individual, para evitar grupos excessivamente pequenos. As faixas são descritivas, não uma definição de cliente-alvo.

# %%
age_band = pd.cut(
    df["Age"],
    bins=[0, 29, 44, 59, 74, 120],
    labels=["<30", "30–44", "45–59", "60–74", "75+"],
)
ages = churn_by(age_band)
display(ages)
ages["Churn (%)"].plot.bar(rot=0, title="Churn por faixa etária", ylabel="Churn (%)")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 9. Cruzamento de variáveis
#
# Uma associação pode mudar quando segmentamos por outra característica. Vamos cruzar `Contract` com `Internet Type` e **verificar também o número de clientes** em cada combinação.

# %%
rates = pd.pivot_table(
    df, values="Churn", index="Contract", columns="Internet Type", aggfunc="mean"
)
counts = pd.crosstab(df["Contract"], df["Internet Type"])
print("Taxa de churn (%)")
display((rates * 100).round(1))
print("Número de clientes por grupo")
display(counts)

# %% [markdown]
# ## 10. Motivos declarados de abandono (apenas análise de negócio)
#
# `Churn Category` e `Churn Reason` são preenchidos **depois do abandono**. Podemos descrevê-los para compreender motivos declarados, **mas nunca utilizá-los como preditores de churn**.

# %%
reasons = df.loc[df["Churn"] == 1, "Churn Category"].value_counts()
display(reasons.rename("Clientes com churn").to_frame())

# %% [markdown]
# ## 11. Data Profilling

# %%
# %pip install ydata-profiling
# %pip install "setuptools<81"

# %%
from pathlib import Path
from ydata_profiling import ProfileReport

# Localizar a pasta principal do projeto
root = next(
    p for p in [Path.cwd(), *Path.cwd().parents] if (p / "src" / "data.py").exists()
)

# Gerar o relatório
profile = ProfileReport(
    df, title="Telco Customer Churn - Data Profiling", explorative=True
)

output = root / "reports/generated/telco_profile.html"
output.parent.mkdir(parents=True, exist_ok=True)

profile.to_file(output)

# %% [markdown]
# ## 11. Conclusões a registar pelo grupo
#
# Depois de examinar os outputs, preencher com **valores observados** (taxa e número de clientes, sempre que possível):
#
# 1. **Segmentos com maior churn:** quais são? Quantos clientes incluem?
# 2. **Antiguidade e mensalidade:** existe uma tendência clara ou diferenças entre intervalos?
# 3. **Segmentação cruzada:** a relação entre contrato e churn mantém-se quando consideramos o tipo de internet?
# 4. **Hipóteses para modelação:** que variáveis parecem informativas e estarão disponíveis **antes** da decisão?
# 5. **Limitações:** snapshot único; variáveis possivelmente medidas depois do evento; associações não implicam causalidade.
#
# **Próxima fase:** auditoria temporal e preparação de dados com split estratificado. O `Satisfaction Score`, `Churn Score`, `Churn Category`, `Churn Reason`, `Customer Status` e as variantes diretas do target não devem entrar como preditores. Uma boa ordenação do risco de churn não demonstra o impacto de uma intervenção de retenção.
