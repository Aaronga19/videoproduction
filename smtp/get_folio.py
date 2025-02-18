import PyPDF2
import re

def get_folio_value(filepath):
    """
    Extracts the value (number or text) next to "Folio" in a PDF.

    Args:
        filepath: Path to the PDF file.

    Returns:
        The folio value (string) if found, otherwise None.
    """
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            info = reader.metadata
            print(info)
            for page in reader.pages:
                text = page.extract_text()
                # Improved regex to handle various folio formats
                match = re.search(r"Folio:\s*[:N°#]?\s*([A-Za-z0-9-]+)", text, re.IGNORECASE) # Case-insensitive
                if match:
                    return match.group(1).strip()  # Return the captured value, strip whitespace

            return None  # Folio not found on any page

    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"
    

folio = get_folio_value("contract/meta/contract.pdf")
print(folio)