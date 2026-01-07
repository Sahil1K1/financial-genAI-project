from src.utils.logger import get_logger
import json
from pathlib import Path

logging = get_logger('Test file')

print(logging)

my_logger = get_logger(__name__)
print(my_logger)
my_logger.info('this is just for info')
my_logger.warning('this is warning message')
my_logger.debug('this is for debugging but the message won"t be shown')

file_path = Path(__file__).parent / 'data/outputs/llm_output.json'
print(file_path)
with open(file_path, 'r') as file:
    data = json.load(file)
    print(data['raw_response'])

