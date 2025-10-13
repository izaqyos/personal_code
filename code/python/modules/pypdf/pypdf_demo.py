#!/opt/homebrew/bin/python3
from pypdf import PdfReader

reader = PdfReader("Afeka_Challenge_Answers.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[1]
text = page.extract_text()
print(f"The text in page 1 is: {text}")
