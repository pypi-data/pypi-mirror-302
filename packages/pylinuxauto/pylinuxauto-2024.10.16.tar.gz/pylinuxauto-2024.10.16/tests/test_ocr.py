from pylinuxauto.ocr import OCR

from pylinuxauto.config import config
from funnylog2 import logger

logger("DEBUG")

config.OCR_SERVER_IP = "10.8.13.100"

a = OCR().find_element_by_ocr("中国").result
print(a)