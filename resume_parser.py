import re
import io
from PyPDF2 import PdfReader

def parse_resume(file):
    text = extract_text_from_pdf(file)
    
    # Very basic info extraction
    name = re.findall(r'Name[:\-]?\s*([A-Za-z ]+)', text)
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d -]{8,}\d', text)
    skills = re.findall(r'Skills[:\-]?\s*(.*)', text, re.IGNORECASE)
    
    return {
        "name": name[0] if name else "",
        "email": email[0] if email else "",
        "phone": phone[0] if phone else "",
        "skills": skills[0].split(",") if skills else [],
        "raw_text": text
    }

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
