import requests
import json

def listar_cidades_por_estado(codigo_estado):
    # URL da API do IBGE para municípios
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{codigo_estado}/municipios"
    
    # Fazendo a requisição GET
    response = requests.get(url)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        municipios = json.loads(response.text)
        
        # Listando os nomes dos municípios
        print(f"Municípios do estado {codigo_estado}:")
        for municipio in municipios:
            print(municipio['nome'])
    else:
        print(f"Erro ao acessar a API: {response.status_code}")

# Exemplo de uso: listar cidades da Paraíba (código 25)
listar_cidades_por_estado(25)