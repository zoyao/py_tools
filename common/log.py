import logging

logging.basicConfig(filename='./logs/info.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',
                    level=logging.INFO)
