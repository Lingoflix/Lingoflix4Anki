import logging, os

# Set up basic logging
logger = logging.getLogger('flask_app')
logger.setLevel(logging.DEBUG)

# Log to a file
current_dir = os.path.dirname(os.path.abspath(__file__))
logfile = os.path.join(current_dir, 'lingoflix4anki.log')
file_handler = logging.FileHandler(logfile, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

