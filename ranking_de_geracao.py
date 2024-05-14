# -*- coding: utf-8 -*-
"""
Created on Mon May 13 14:55:54 2024

@author: felipe.damasceno
"""
import pandas as pd
import os

diretorio = '\\\\arara1-10-2\\Arquivos\\29 - Superitendencia de Planejamento da Operação\\02-Banco de dados\\Geração SIN\\GERACAO_USINA'
arquivos = os.listdir(diretorio)

# DataFrame vazio para armazenar todos os resultados
resultados_totais = pd.DataFrame()

# Itera sobre todos os arquivos
for arquivo in arquivos:
    # Verifica se o arquivo é um arquivo Excel
    if arquivo.endswith(".xlsx"):
        try:
            # Lê o arquivo Excel
            df = pd.read_excel(os.path.join(diretorio, arquivo))
            
            # Filtrar o DataFrame para hidroelétricas
            df_hidro = df[df['nom_tipousina'] == 'HIDROELÉTRICA']

            # Extrai o mês da coluna 'din_instante' e armazena em uma nova coluna 'mes'
            df_hidro['mes'] = df_hidro['din_instante'].dt.month

            # Extrai o ano da coluna 'din_instante' e armazena em uma nova coluna 'ano'
            df_hidro['ano'] = df_hidro['din_instante'].dt.year
            
            # Calcula a média mensal de geração de energia por usina
            media_mensal_hidro = df_hidro.groupby(['nom_usina', 'ano', 'mes']).mean().reset_index()
            
            # Adiciona os resultados ao DataFrame total
            resultados_totais = pd.concat([resultados_totais, media_mensal_hidro])
            
            print(f"Processamento concluído para o arquivo: {arquivo}")
        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo}: {e}")

# Salva o resultado em um único arquivo Excel
nome_arquivo_saida = "resultados_totais_hidro.xlsx"
resultados_totais.to_excel(os.path.join(diretorio, nome_arquivo_saida), index=False)
print("Todos os resultados das hidroelétricas foram combinados em um único arquivo Excel.")