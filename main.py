import logging
from config_loader import Main

if __name__ == "__main__":
    # Konfiguracja logowania
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('GA_Logger')

    logger.info("Rozpoczynanie eksperymentów algorytmu genetycznego")
    logger.info("Wczytywanie konfiguracji z pliku configs.json")

    # Uruchomienie eksperymentów
    results = Main.run('configs.json')

    logger.info("Eksperymenty zakończone")