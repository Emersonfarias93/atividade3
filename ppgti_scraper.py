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