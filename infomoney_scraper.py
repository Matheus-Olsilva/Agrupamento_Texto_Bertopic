import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import json
import re
from datetime import datetime

class InfoMoneyScraper:
    """
    Classe para extrair o conteúdo completo das notícias do InfoMoney
    """
    
    def __init__(self):
        self.base_url = "https://www.infomoney.com.br"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def fetch_page(self, url):
        """
        Faz a requisição HTTP para obter o conteúdo da página
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
            return None
    
    def get_article_links(self, html_content):
        """
        Extrai os links das notícias da página principal
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        # Busca por diferentes seletores CSS para encontrar links de notícias
        selectors = [
            'article a',
            '.post a',
            '.noticia a',
            '.card a',
            '.item a',
            'div[class*="post"] a',
            'div[class*="article"] a',
            'div[class*="news"] a',
            'h1 a', 'h2 a', 'h3 a', 'h4 a'
        ]
        
        found_links = set()
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href')
                if href:
                    # Converte para URL absoluta
                    full_url = urljoin(self.base_url, href)
                    # Verifica se é um link interno do InfoMoney
                    if 'infomoney.com.br' in full_url and full_url not in found_links:
                        found_links.add(full_url)
        
        return list(found_links)
    
    def is_valid_content(self, text):
        """
        Verifica se o texto é conteúdo válido da notícia
        """
        # Lista de padrões que indicam informações desnecessárias
        unwanted_patterns = [
            r'^\d{2}/\d{2}/\d{4}',  # Data no início
            r'^\d{2}h\d{2}',        # Hora no início
            r'Atualizado.*atrás',   # "Atualizado X horas atrás"
            r'Estadão Conteúdo',    # Nome do veículo
            r'^\d{2}/\d{2}/\d{4}.*\d{2}h\d{2}',  # Data e hora juntas
            r'•.*atrás',            # Bullet com tempo
            r'^\s*\d{2}/\d{2}/\d{4}\s*\d{2}h\d{2}.*$',  # Padrão completo de data/hora
            r'^\s*Por\s+',          # "Por Fulano"
            r'^\s*De\s+',           # "De Fulano"
            r'^\s*Fonte:',          # "Fonte:"
            r'^\s*Leia também',     # "Leia também"
            r'^\s*Veja mais',       # "Veja mais"
            r'^\s*Saiba mais',      # "Saiba mais"
            r'^\s*Leia mais',       # "Leia mais"
            r'^\s*Confira',         # "Confira"
            r'^\s*Clique aqui',     # "Clique aqui"
            r'^\s*Assine',          # "Assine"
            r'^\s*Cadastre-se',     # "Cadastre-se"
            r'^\s*Newsletter',      # "Newsletter"
            r'^\s*Publicidade',     # "Publicidade"
            r'^\s*Anúncio',         # "Anúncio"
            r'^\s*Continua após',   # "Continua após publicidade"
            r'^\s*\d+\s*de\s*\d+',  # Paginação "1 de 10"
        ]
        
        # Verifica se o texto contém algum padrão indesejado
        for pattern in unwanted_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        
        # Verifica se é muito curto ou só tem números/símbolos
        if len(text.strip()) < 30:
            return False
        
        # Verifica se é principalmente números e símbolos (provavelmente metadata)
        alphanumeric_count = sum(1 for char in text if char.isalnum())
        if alphanumeric_count < len(text) * 0.7:
            return False
        
        return True
    
    def extract_article_content(self, article_url):
        """
        Extrai o conteúdo completo de uma notícia individual
        """
        html_content = self.fetch_page(article_url)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        article_data = {
            'url': article_url,
            'titulo': '',
            'conteudo': '',
            'data': '',
            'categoria': ''
        }
        
        try:
            # Extrai o título
            title_selectors = [
                'h1',
                '.title',
                '.post-title',
                '.article-title',
                'header h1',
                'header h2'
            ]
            
            for selector in title_selectors:
                title_element = soup.select_one(selector)
                if title_element:
                    article_data['titulo'] = title_element.get_text(strip=True)
                    break
            
            # Extrai o conteúdo do artigo
            content_selectors = [
                '.post-content',
                '.article-content',
                '.content',
                '.entry-content',
                '.post-body',
                '.article-body',
                'div[class*="content"]',
                'div[class*="post"]',
                'div[class*="article"]'
            ]
            
            content_paragraphs = []
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    # Extrai todos os parágrafos do conteúdo
                    paragraphs = content_element.find_all('p')
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if text and len(text) > 20:  # Ignora parágrafos muito curtos
                            # Filtra informações desnecessárias
                            if self.is_valid_content(text):
                                content_paragraphs.append(text)
                    break
            
            # Se não encontrou com seletores específicos, busca todos os parágrafos
            if not content_paragraphs:
                all_paragraphs = soup.find_all('p')
                for p in all_paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 20 and self.is_valid_content(text):
                        content_paragraphs.append(text)
            
            article_data['conteudo'] = '\n\n'.join(content_paragraphs)
            
            # Extrai a data
            date_selectors = [
                'time',
                '.date',
                '.post-date',
                '.article-date',
                'span[class*="date"]',
                'div[class*="date"]'
            ]
            
            for selector in date_selectors:
                date_element = soup.select_one(selector)
                if date_element:
                    date_text = date_element.get('datetime') or date_element.get_text(strip=True)
                    article_data['data'] = date_text
                    break
            
            # Extrai a categoria
            category_selectors = [
                '.category',
                '.post-category',
                '.article-category',
                'span[class*="category"]',
                'div[class*="category"]'
            ]
            
            for selector in category_selectors:
                category_element = soup.select_one(selector)
                if category_element:
                    article_data['categoria'] = category_element.get_text(strip=True)
                    break
                    
        except Exception as e:
            print(f"Erro ao extrair conteúdo de {article_url}: {e}")
        
        return article_data
    
    def scrape_infomoney(self, max_articles=10):
        """
        Executa o scraping completo das notícias do InfoMoney
        """
        print("Iniciando scraping do InfoMoney...")
        
        # Acessa a página principal
        html_content = self.fetch_page(self.base_url)
        if not html_content:
            return None
        
        # Extrai os links das notícias
        print("Extraindo links das notícias...")
        article_links = self.get_article_links(html_content)
        
        if not article_links:
            print("Nenhum link de notícia encontrado.")
            return None
        
        # Limita o número de artigos
        article_links = article_links[:max_articles]
        
        print(f"Encontrados {len(article_links)} links de notícias. Extraindo conteúdo...")
        
        # Extrai o conteúdo de cada artigo
        articles = []
        for i, link in enumerate(article_links, 1):
            print(f"Processando artigo {i}/{len(article_links)}: {link}")
            
            article_data = self.extract_article_content(link)
            if article_data and article_data['conteudo']:
                articles.append(article_data)
            
            # Pausa entre requisições para ser respeitoso
            time.sleep(2)
        
        # Compila os resultados
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_articles': len(articles),
            'articles': articles,
            'fonte': self.base_url
        }
        
        return results
    
    def save_to_json(self, data, filename='infomoney_noticias_completas.json'):
        """
        Salva os dados em formato JSON
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Dados salvos em {filename}")
        except Exception as e:
            print(f"Erro ao salvar arquivo JSON: {e}")
    
    def display_summary(self, data):
        """
        Exibe um resumo dos dados coletados
        """
        if not data:
            print("Nenhum dado foi coletado.")
            return
        
        print("\n" + "="*50)
        print("RESUMO DO SCRAPING - INFOMONEY")
        print("="*50)
        print(f"Data/Hora: {data['timestamp']}")
        print(f"Total de artigos: {data['total_articles']}")
        print(f"Fonte: {data['fonte']}")
        
        print("\nPrimeiros 3 artigos:")
        print("-" * 50)
        for i, article in enumerate(data['articles'][:3]):
            print(f"{i+1}. {article['titulo']}")
            print(f"   URL: {article['url']}")
            print(f"   Data: {article['data']}")
            print(f"   Categoria: {article['categoria']}")
            print(f"   Tamanho do conteúdo: {len(article['conteudo'])} caracteres")
            print(f"   Prévia: {article['conteudo'][:150]}...")
            print()

def main():
    """
    Função principal para executar o scraper
    """
    scraper = InfoMoneyScraper()
    
    # Pergunta quantos artigos processar
    try:
        max_articles = int(input("Quantos artigos deseja processar? (padrão: 10): ") or "10")
    except ValueError:
        max_articles = 10
    
    # Executa o scraping
    data = scraper.scrape_infomoney(max_articles)
    
    if data:
        # Exibe resumo
        scraper.display_summary(data)
        
        # Salva os dados
        scraper.save_to_json(data)
        
        return data
    else:
        print("Falha ao coletar dados do InfoMoney")
        return None

if __name__ == "__main__":
    # Instala as dependências necessárias
    try:
        import requests
        import bs4
    except ImportError:
        print("Instalando dependências necessárias...")
        print("Execute: pip install requests beautifulsoup4")
        exit(1)
    
    # Executa o scraper
    dados = main()