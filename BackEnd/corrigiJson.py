import json

# Lista dos campos de matrícula
campos_matricula = [
    'QT_MAT_BAS', 'QT_MAT_EJA', 'QT_MAT_ESP',
    'QT_MAT_FUND', 'QT_MAT_INF', 'QT_MAT_MED', 'QT_MAT_PROF'
]

# Carrega o JSON
with open('instituicoes2024.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Substitui None por 0 nos campos definidos
for registro in dados:
    for campo in campos_matricula:
        if campo not in registro or registro[campo] is None:
            registro[campo] = 0

# Salva o JSON corrigido
with open('instituicoes2024_corrigido.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print('Arquivo corrigido salvo como instituicoes_corrigido.json')
