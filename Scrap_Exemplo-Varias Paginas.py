import requests
from bs4 import BeautifulSoup
import time

def scrape_all_books():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []
    page = 1
    
    while True:
        url = base_url.format(page)
        print(f"Scraping p�gina {page}: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code == 404:
                print("Fim das p�ginas!")
                break
                
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            books = soup.find_all('article', class_='product_pod')
            
            if not books:
                break
                
            for book in books:
                title = book.h3.a['title']
                price = book.find('p', class_='price_color').text
                availability = book.find('p', class_='instock availability').text.strip()
                rating = book.p['class'][1]
                
                all_books.append({
                    'T�tulo': title,
                    'Pre�o': price,
                    'Disponibilidade': availability,
                    'Avalia��o': rating,
                    'P�gina': page
                })
            
            page += 1
            time.sleep(1)  # Respeitar o servidor
            
        except Exception as e:
            print(f"Erro na p�gina {page}: {e}")
            break
    
    print(f"\nTotal de livros coletados: {len(all_books)}")
    return all_books



# Para usar:
# todos_livros = scrape_all_books()


#Extrair tamb�m a categoria de cada livro
#Converter o pre�o para n�mero (remover o s�mbolo �)
#Filtrar apenas livros com 4+ estrelas
#Salvar em JSON em vez de CSV

