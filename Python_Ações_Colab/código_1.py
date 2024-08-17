!pip install pandas
!pip plotly.express

import pandas as pd
import plotly.express as px

df_principal = pd.read_excel("/content/Tabela de ações.xlsx", sheet_name="Principal")
df_principal



df_total_acoes = pd.read_excel("/content/Tabela de ações.xlsx", sheet_name="Total_de_acoes")
df_total_acoes



df_ticker = pd.read_excel("/content/Tabela de ações.xlsx", sheet_name="Ticker")
df_ticker

df_chatgpt = pd.read_excel("/content/Tabela de ações.xlsx", sheet_name="Utilitários")
df_chatgpt

df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()
df_principal

df_principal = df_principal.rename(columns={'Último (R$)':'Valor_final','Var. Dia (%)':'Valor_Dia_pct'}).copy()
df_principal

df_principal['Var_pct'] = df_principal['Valor_Dia_pct'] / 100
df_principal['valor_inicial'] = df_principal['Valor_final'] / (df_principal ['Var_pct'] + 1)
df_principal

df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left')
df_principal

df_principal = df_principal.drop(columns=['Código'])
df_principal

df_principal['variacao_rs'] = (df_principal['Valor_final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica']
df_principal

pd.options.display.float_format= '{:.2f}'.format

df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)
df_principal

df_principal = df_principal.rename(columns={'Qtde. Teórica':'Qtde_teorica'}).copy()
df_principal

df_principal['Resultado'] = df_principal['variacao_rs'].apply(lambda x: 'Subiu' if x > 0 else('Desceu' if x < 0 else 'Estavel'))
df_principal

df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal

df_principal = df_principal.drop(columns=['Ticker'])
df_principal

df_principal = df_principal.merge(df_chatgpt, left_on='Nome', right_on='Nome da empresa', how='left')
df_principal = df_principal.drop(columns='Nome')
df_principal

df_principal['Cat_Idade'] = df_principal['Idade (anos)'].apply(lambda x: 'Maior de 100 anos' if x > 100 else('Menor de 50 anos' if x < 50 else 'Entre 100 e 50 anos'))
df_principal

maior = df_principal['variacao_rs'].max()
menor = df_principal['variacao_rs'].min()
media = df_principal['variacao_rs'].mean()
media_subiu = df_principal[df_principal['Resultado']=='Subiu']["variacao_rs"].mean()
media_desceu = df_principal[df_principal['Resultado']=='Desceu']["variacao_rs"].mean()
print(f"Maior\tR$ {maior:,.2f}")
print(f"Menor\tR$ {menor:,.2f}")
print(f"Media\tR$ {media:,.2f}")
print(f"Média de quem subiu\tR$ {media_subiu:,.2f}")
print(f"Média de quem desceu\tR$ {media_desceu:,.2f}")

df_principal[df_principal['Resultado'] == 'Subiu']

df_analise_segmento = df_principal_subiu.groupby('Segmento')['variacao_rs'].sum().reset_index()
df_analise_segmento

df_analise_saldo = df_principal.groupby('Resultado')['variacao_rs'].sum().reset_index()
df_analise_saldo

fig = px.bar(df_analise_saldo, x='variacao_rs', y='Resultado', text='variacao_rs', title='Variação em Reais por Resultado')
fig.update_traces(texttemplate='%{text:.2f}')
fig.show()