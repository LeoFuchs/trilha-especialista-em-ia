# -*- coding: utf-8 -*-
"""
Desafio Final:

1. Carregar um arquivo .txt, onde cada linha será um elemento de uma lista do Python
2. Mandá-la ao modelo que você está rodando localmente para extrair, em formato JSON, onde cada item terá "usuario", "resenha original", "resenha_pt", "avaliacao" (Positiva, Negativa, Neutra)
3. Transformar a resposta do modelo em uma lista de dicionários Python
4. Criar uma função que, dada uma lista de dicionários, percorre a lista e faz 2 coisas:
 a) conta a quantidade de avaliações positivas, negativas e neutras
 b) une cada item dessa lista em uma variável do tipo string com algum separador.
Ao final, retorna ambas as coisas.

"""

from openai import OpenAI
import json

# Etapa 1
with open("resenhas.txt", "r", encoding="utf-8") as file:
    linhas = [line.strip() for line in file.readlines()]

# Etapa 2
def recebe_linha_e_retorna_json(linha):
    client_openai = OpenAI(
        base_url="http://127.0.0.1:1234/v1",
        api_key="lm-studio"
    )

    response = client_openai.chat.completions.create(
        model="google/gemma-3-1b",
        messages=[{
        "role": "user", 
        "content": f"""Analise a seguinte resenha presente nesta lista e retorne para cada elemento apenas um JSON com os campos 'usuario', 'resenha original', 'resenha_pt', 'avaliacao' (Positiva, Negativa, Neutra).

        Exemplo de entrada: [53409593$Safoan Riyad$J'aimais bien ChatGPT. Mais la derniÃ¨re mise Ã jour a tout gÃ¢chÃ©. Elle a tout oubliÃ©.']
        Exemplo de saída: {{"usuario": 53409593, "resenha original": "J'aimais bien ChatGPT. Mais la derniÃ¨re mise Ã jour a tout gÃ¢chÃ©. Elle a tout oubliÃ©.", "resenha_pt": "Eu gostava do ChatGPT. Mas a última atualização estragou tudo. Esqueceu de tudo.", "avaliacao": "Negativa"}}

        Agora analise essa lista: {linha}. """
        }],
        temperature=0.0
    )

    return response.choices[0].message.content

# Etapa 3
lista_de_resenhas = []

for resenha in linhas:
    resenha_json = recebe_linha_e_retorna_json(resenha).replace("```json", "").replace("```", "")
    resenha_dict = json.loads(resenha_json)
    lista_de_resenhas.append(resenha_dict)

# Etapa 4
def analisar_resenhas(lista_de_resenhas):
    """
    Analisa uma lista de dicionários de resenhas para contar as avaliações
    e unir os dados em uma única string separada por um delimitador.

    Args:
        lista_de_resenhas (list): Lista de dicionários, onde cada dicionário
                                  contém a chave 'avaliacao' (Positiva, Negativa, Neutra).

    Returns:
        tuple: Uma tupla contendo:
               1. Um dicionário com a contagem de avaliações (Positiva, Negativa, Neutra).
               2. Uma string contendo todos os dados das resenhas concatenados.
    """
    # 1. Inicializa o contador de avaliações
    contagem_avaliacoes = {
        "Positiva": 0,
        "Negativa": 0,
        "Neutra": 0
    }

    # 2. Inicializa a lista para armazenar as strings de cada resenha
    strings_resenhas = []
    
    # Define o separador que será usado para unir os dados de cada resenha.
    # Usaremos uma linha de traços para facilitar a visualização.
    SEPARADOR_ITEM = "\n---\n" 

    for resenha in lista_de_resenhas:
        # a) Conta as avaliações
        avaliacao = resenha.get("avaliacao")
        if avaliacao in contagem_avaliacoes:
            contagem_avaliacoes[avaliacao] += 1
        
        # b) Une os dados do dicionário em uma string e adiciona à lista
        string_resenha = (
            f"USUÁRIO: {resenha.get('usuario')}\n"
            f"AVALIAÇÃO: {avaliacao}\n"
            f"RESENHA ORIGINAL: {resenha.get('resenha original')}\n"
            f"RESENHA PT: {resenha.get('resenha_pt')}"
        )
        strings_resenhas.append(string_resenha)

    # b) Concatena todas as strings das resenhas em uma única variável,
    # usando o separador definido.
    string_final = SEPARADOR_ITEM.join(strings_resenhas)

    return contagem_avaliacoes, string_final

contagem, dados_concatenados = analisar_resenhas(lista_de_resenhas)

# Imprime os resultados
print("--- RESULTADO DA ANÁLISE ---")
print("\na) CONTAGEM DE AVALIAÇÕES:")
for tipo, cont in contagem.items():
    print(f"  {tipo}: {cont}")

print("\n------------------------------")
print("b) DADOS CONCATENADOS (String Única):")
print("------------------------------")
print(dados_concatenados)