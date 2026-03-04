from database import get_session, save_reading
from scraper import ChoreScraper
import time

# Configurações
USER = "Junior"
PASS = "Junior1281"
URLS = {
    "Aviario_1": "https://www.choretronicswebservices.com/...",
    "Aviario_2": "https://www.choretronicswebservices.com/..."
}

def run_scraper( ):
    session = get_session()
    scraper = ChoreScraper(USER, PASS)
    
    try:
        scraper.login()
        for name, url in URLS.items():
            print(f"Coletando dados de {name}...")
            data = scraper.get_aviary_data(url)
            data['aviary_id'] = name
            save_reading(session, data)
            print("Dados salvos com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    run_scraper()
