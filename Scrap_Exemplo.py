import requests
from bs4 import BeautifulSoup
import csv

def scrape_books():
    # URL do site de exemplo
    url = "http://books.toscrape.com/"
    
    try:
        # Fazer requisicao da pagina
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisicao foi bem-sucedida
        
        # Parse do conteudo HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar todos os livros na pagina
        books = soup.find_all('article', class_='product_pod')
        
        print(f"Encontrados {len(books)} livros na pagina inicial\n")
        
        # Lista para armazenar os dados
        books_data = []
        
        # Extrair informacoes de cada livro
        for book in books:
            # Titulo
            title = book.h3.a['title']
            
            # Preco
            price = book.find('p', class_='price_color').text
            
            # Disponibilidade
            availability = book.find('p', class_='instock availability').text.strip()
            
            # Classificacao (estrelas)
            rating = book.p['class'][1]  # Ex: 'Three', 'Four', etc.
            
            # Adicionar a lista
            books_data.append({
                'Titulo': title,
                'Preco': price,
                'Disponibilidade': availability,
                'Avaliacao': rating
            })
            
            # Exibir no console
            print(f"Titulo: {title}")
            print(f"Preco: {price}")
            print(f"Disponibilidade: {availability}")
            print(f"Avaliacao: {rating} estrelas")
            print("-" * 50)
        
        # Salvar em CSV
        save_to_csv(books_data)
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisicao: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def save_to_csv(books_data):
    """Salva os dados em um arquivo CSV"""
    with open('livros.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=books_data[0].keys())
        writer.writeheader()
        writer.writerows(books_data)
    
    print("\nDados salvos em 'livros.csv'")

# Executar a funcao
if __name__ == "__main__":
    scrape_books()