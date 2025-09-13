from PIL import Image

import pytesseract
import re

URL_REGEX = r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?'

img = Image.open('test/sms_phish.png')

extracted_text = pytesseract.image_to_string(img)

print("Extracted Text:", repr(extracted_text.replace('/\n', '/').replace('.\n', '.').replace('\n', ' ')))

print("Found URLs:", re.findall(URL_REGEX, extracted_text))
print("Found URLs:", re.findall(URL_REGEX, extracted_text.replace('\n', '')))