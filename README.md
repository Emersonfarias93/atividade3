
INSTITUTO FEDERAL DA PARAÍBA - IFPB

Unidade Acadêmica de Informação e Comunicação

Mestrado Profissional em Tecnologia da Informação

Disciplina: Banco de Dados2

Professor: Diego Pessoa

Grupo: Emerson de Farias Santos

APIs, Crawlers, Scrapers e LGDP

1. Responda as questões seguintes (3,0):
  1. Qual é a diferença entre APIs, Scrapers e Crawlers e em que situações cada um é usado?

    APIs são interfaces projetadas para permitir que diferentes sistemas de software se comuniquem de maneira controlada e estruturada.

    Scrapers são ferramentas ou scripts projetados para extrair dados específicos de websites, geralmente focando em páginas específicas.
    
    Crawlers, também conhecidos como web spiders, são programas que navegam sistematicamente pela web, seguindo links e indexando conteúdo.

  2. Quais são três exemplos de PII (Personally Identifiable Information) e quais técnicas podem ser aplicadas para anonimizá-los de acordo com a LGPD (Lei Geral de Proteção de Dados)?

    Exemplos de PII:
    CPF (Cadastro de Pessoas Físicas)
    Endereço residencial
    Número de telefone celular
    Técnicas de Anonimização:
    Mascaramento:
    
    CPF: 123.456.789-00 → XXX.XXX.789-00
    Telefone: (83) 98765-4321 → (83) 9XXXX-4321
    Pseudonimização:
    
    Substituir o nome real por um identificador único gerado aleatoriamente.
    Ex.: "João Silva" → "Usuario_A7X9B2"
    Generalização:
    
    Endereço: Rua das Flores, 123, Bairro Centro, João Pessoa - PB → Bairro Centro, João Pessoa - PB
    Criptografia:
    
    Utilizar algoritmos de criptografia para proteger dados sensíveis.
    Armazenar apenas o hash do CPF, por exemplo.
    Agregação:
    
    Em vez de armazenar idades individuais, agrupar em faixas etárias.
    Ex.: 25 anos → Faixa etária 20-30 anos
    Estas técnicas visam proteger a privacidade dos indivíduos, tornando mais difícil ou impossível a identificação direta a partir dos dados armazenados, em conformidade com a LGPD.

2. Crie um script para consumir dados da API do IBGE para listar os nomes das cidades de um estado específico (2,0)

````python

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
````

3. Crie um Scraper para ler os dados dos docentes da página do PPGTI (https://www.ifpb.edu.br/ppgti/programa/corpo-docente) - construa um dataframe que liste o nome, linha de pesquisa, url do lattes e e-mail de cada professor (5,0).

````python
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página do corpo docente do PPGTI
url = "https://www.ifpb.edu.br/ppgti/programa/corpo-docente"

# Fazendo a requisição GET
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parsing do HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrando todos os divs com a classe 'tile-content'
    docentes = soup.find_all('div', class_='tile-content')
    
    # Listas para armazenar os dados
    nomes = []
    linhas_pesquisa = []
    urls_lattes = []
    emails = []
    
    # Iterando sobre cada docente
    for docente in docentes:
        # Extraindo o nome
        nome = docente.find('h2', class_='tileHeadline').text.strip()
        nomes.append(nome)
        
        # Extraindo a linha de pesquisa
        linha = docente.find('p', class_='tileBody').text.strip()
        linhas_pesquisa.append(linha)
        
        # Extraindo a URL do Lattes
        lattes_link = docente.find('a', text='Currículo Lattes')
        urls_lattes.append(lattes_link['href'] if lattes_link else 'N/A')
        
        # Extraindo o e-mail
        email = docente.find('a', href=lambda href: href and href.startswith('mailto:'))
        emails.append(email.text if email else 'N/A')
    
    # Criando o DataFrame
    df = pd.DataFrame({
        'Nome': nomes,
        'Linha de Pesquisa': linhas_pesquisa,
        'URL Lattes': urls_lattes,
        'E-mail': emails
    })
    
    # Exibindo o DataFrame
    print(df)
    
    # Opcional: Salvar o DataFrame em um arquivo CSV
    # df.to_csv('docentes_ppgti.csv', index=False)
    
else:
    print(f"Erro ao acessar a página: {response.status_code}")
    
