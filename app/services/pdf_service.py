import pypandoc
from pathlib import Path

def markdown_to_pdf(markdown_text: str, output_filename: str) -> Path:
    """
    Convierte un texto Markdown a PDF y devuelve la ruta del archivo generado.
    """
    output_path = Path("generated") / f"{output_filename}.pdf"
    output_path.parent.mkdir(exist_ok=True)
    pypandoc.convert_text(
        markdown_text,
        "pdf",
        format="md",
        outputfile=str(output_path),
        extra_args=['--standalone']
    )
    return output_path
