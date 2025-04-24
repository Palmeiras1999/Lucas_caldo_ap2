import requests
import pandas as pd

# TOKEN
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTE1ODMyLCJpYXQiOjE3NDUzMjM4MzIsImp0aSI6IjY3ZTRjOGIzYTM0NzQ5ZmM5N2UyMDYwNjI4ZWIyYzY2IiwidXNlcl9pZCI6Mjh9.wzkQiBk-U8aTs__Ra4jRUzAlxrI9LOZt4LrGYrxKUS8"
headers = {'Authorization': f'JWT {token}'}

# --- Consulta API para PRIO3 2024
params_2024 = {'ticker': 'PRIO3', 'ano_tri': '20244T'}
r_2024 = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params_2024, headers=headers)
df_24 = pd.DataFrame(r_2024.json()['dados'][0]['balanco'])

# --- Consulta API para PRIO3 2023
params_2023 = {'ticker': 'PRIO3', 'ano_tri': '20234T'}
r_2023 = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params_2023, headers=headers)
df_23 = pd.DataFrame(r_2023.json()['dados'][0]['balanco'])

# --- Função para buscar valores contábeis
def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False, na=False)
    return sum(df[filtro_conta & filtro_descricao]['valor'].values)

# Valores principais
estoque_24 = valor_contabil(df_24, '^1.0*', 'estoque|óleo|consumível')
estoque_23 = valor_contabil(df_23, '^1.0*', 'estoque|óleo|consumível')
estoque_medio = (estoque_24 + estoque_23) / 2

intagivel = valor_contabil(df_24, '^1.*', 'Intang')
imobilizado = valor_contabil(df_24, '^1.*', 'Imobilizad')
investimentos = valor_contabil(df_24, '^1.*', 'Invest')
pl = valor_contabil(df_24, '^2.*', 'patrim.nio')
ipl = (intagivel + imobilizado + investimentos) / pl if pl else None

# Liquidez
ativo_circulante = valor_contabil(df_24, '^1.01', '')
ativo_nao_circulante = valor_contabil(df_24, '^1.1', '')
passivo_circulante = valor_contabil(df_24, '^2.01', '')
passivo_nao_circulante = valor_contabil(df_24, '^2.02', '')
disponibilidades = valor_contabil(df_24, '^1.01', 'Caixa|Bancos')
estoques = valor_contabil(df_24, '^1.01', 'estoque|óleo|consumível')
contas_receber = valor_contabil(df_24, '^1.01', 'Clientes|Duplicatas|receber')

# Liquidez
ccl = ativo_circulante - passivo_circulante
lc = ativo_circulante / passivo_circulante if passivo_circulante else None
ls = (ativo_circulante - estoques) / passivo_circulante if passivo_circulante else None
li = disponibilidades / passivo_circulante if passivo_circulante else None
lg = (ativo_circulante + ativo_nao_circulante) / (passivo_circulante + passivo_nao_circulante)

# Endividamento
divida_total = passivo_circulante + passivo_nao_circulante
endividamento_geral = divida_total / (ativo_circulante + ativo_nao_circulante)
solvencia = (ativo_circulante + ativo_nao_circulante) / (passivo_circulante + passivo_nao_circulante)
relacao_ct_cp = passivo_nao_circulante / passivo_circulante if passivo_circulante else None
composicao_endividamento = passivo_circulante / divida_total if divida_total else None

# Valores reais informados
cmv = 2876000  # R$ mil
receitas = 11380000  # R$ mil

# Indicadores operacionais
pme = 360 * (estoque_medio / cmv) if cmv else None
ge = cmv / estoque_medio if estoque_medio else None
pmr = 360 * contas_receber / receitas if receitas else None
fornecedores = valor_contabil(df_24, '^2.01', 'Fornecedores')
pmpf = 360 * fornecedores / cmv if cmv else None

# Ciclos
co = pme + pmr if pme and pmr else None
cf = co - pmpf if co and pmpf else None
ce = 360 / ge if ge else None

# Capital de Giro
ncg = ativo_circulante - fornecedores - contas_receber - estoques
st = ccl - ncg
cg = ativo_circulante - passivo_circulante

# Print dos principais indicadores
print(f"Estoque Médio: R$ {estoque_medio:,.0f}")
print(f"Índice de Imobilização do PL: {ipl:.4f}")
print(f"Liquidez Corrente: {lc:.2f}")
print(f"Liquidez Seca: {ls:.2f}")
print(f"Liquidez Imediata: {li:.2f}")
print(f"Liquidez Geral: {lg:.2f}")
print(f"Endividamento Geral: {endividamento_geral:.2f}")
print(f"Solvência: {solvencia:.2f}")
print(f"Composição do Endividamento: {composicao_endividamento:.2f}")
print(f"PME (dias): {pme:.1f}")
print(f"PMR (dias): {pmr:.1f}")
print(f"PMPF (dias): {pmpf:.1f}")
print(f"Ciclo Operacional (CO): {co:.1f}")
print(f"Ciclo Financeiro (CF): {cf:.1f}")
print(f"Ciclo Econômico (CE): {ce:.1f}")
print(f"NCG: R$ {ncg:,.0f}")
print(f"Saldo de Tesouraria: R$ {st:,.0f}")
print(f"Capital de Giro: R$ {cg:,.0f}")




 