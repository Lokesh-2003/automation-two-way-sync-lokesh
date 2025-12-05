import time
from sync.engine import SyncEngine
from utils.logger import logger

def main():
    engine = SyncEngine()
    
    logger.info("Automation Service Started. Press Ctrl+C to stop.")
    
    while True:
        try:
            engine.sync()
            logger.info("Sleeping for 60 seconds...")
            time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Stopping service...")
            break
        except Exception as e:
            logger.error(f"Critical Error in Main Loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()