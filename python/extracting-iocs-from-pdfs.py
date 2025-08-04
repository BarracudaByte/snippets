from urllib.parse import urlparse

import click
import pypdfium2 as pdfium
import re
import pikepdf

PHONE_REGEX = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
EMAIL_REGEX = r'\S+@\S+\.\S+'

@click.command()
@click.argument('filepath')
def parse_pdf(filepath, password):
    """Script to extract IOCs from a PDF file, for URLs it will also try to extract the FQDN."""
    with open(filepath, "rb") as fh:
        # Extracting text
        pdf = pdfium.PdfDocument(fh)
        version = pdf.get_version()
        num_pages = len(pdf)
        
        # extracting text (this mostly exctracts visible characters)
        text = [page.get_textpage().get_text_bounded() for page in pdf]
        result = {'pages': num_pages, 'version': version, 'text': text, 'urls': [], 'domains': []}

        full_text = '\n'.join(text)
        # extract phone numbers from visible text
        matched_phone_nums = re.findall(PHONE_REGEX, full_text)
        result['phone_numbers'] = matched_phone_nums

        # extracting email from visible text
        matched_emails = re.findall(EMAIL_REGEX, full_text)
        result['email_addresses'] = matched_emails

        # Extracting URLs from the Annots objects
        pdf = pikepdf.Pdf.open(fh)
        for page in pdf.pages:
            for annots in page.get('/Annots', []):
                url = annots.get('/A', {}).get('/URI')
                if url:
                    url = str(url)
                    parsed_url = urlparse(url)
                    # Email address from Annotation
                    if parsed_url.scheme == 'mailto':
                        result['email_addresses'].append(parsed_url.netloc or parsed_url.path)
                        continue
                    # Phone number from Annotation
                    if parsed_url.scheme == 'tel':
                        result['phone_numbers'].append(parsed_url.netloc or parsed_url.path)
                        continue

                    # Otherwise its just a normal URI
                    result['urls'].append(url)
                    result['domains'].append(parsed_url.netloc or parsed_url.path)
    print(result)
        

if __name__ == '__main__':
    parse_pdf()