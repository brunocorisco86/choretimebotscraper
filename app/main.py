import schedule
import time
import logging
from config import CHORE_USER, CHORE_PASS, DB_PATH, PG_URI
from database import init_db, AviaryReading
from scraper import ChoreScraper
from sync import transfer_data
from log_cleaner import clean_old_logs

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
sqlite_uri = f"sqlite:///{DB_PATH}"
SessionFactory = init_db(sqlite_uri)

def job_scrape():
    scraper = ChoreScraper(CHORE_USER, CHORE_PASS)
    if scraper.login():
        # Exemplo para os aviários 1282 e 1283
        urls = [
            ("1282", "https://www.choretronicswebservices.com/connect/00b6f4c3-d40f-1a6f-5f74-b779a048f4f5/2/CurrentConditions" ),
            ("1283", "https://www.choretronicswebservices.com/connect/00b6f4c3-d40f-1a6f-5f74-b779a048f4f5/3/CurrentConditions" )
        ]
        for num, url in urls:
            data = scraper.scrape_aviary(url)
            if data:
                session = SessionFactory()
                session.add(AviaryReading(aviary_id=num, **data))
                session.commit()
                session.close()
                logging.info(f"Dados do aviário {num} salvos.")
    scraper.close()

schedule.every(10).minutes.do(job_scrape)
schedule.every(4).hours.do(transfer_data)
schedule.every().sunday.at("00:00").do(clean_old_logs)

if __name__ == "__main__":
    logging.info("Serviço ChoreTime Iniciado...")
    job_scrape() # Executa uma vez ao iniciar
    while True:
        schedule.run_pending()
        time.sleep(1)
