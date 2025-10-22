import pypandoc
from pathlib import Path

def markdown_to_pdf(markdown_text: str, output_filename: str) -> Path:
    """
    Convierte un texto Markdown a PDF y devuelve la ruta del archivo generado.
    """
    output_path = Path("generated") / f"{output_filename}.pdf"
    output_path.parent.mkdir(exist_ok=True)

    extra_args = [
    "--standalone",
    "-V", "geometry:margin=1.5cm",
    "-V", "fontsize=11pt",
    "-V", "mainfont=Arial",
    "--wrap=preserve",             # Mantiene los saltos de línea
    "--shift-heading-level-by=0"   # Opcional, mantiene los niveles de encabezado
    ]

    pypandoc.convert_text(
        markdown_text,
        "pdf",
        format="md",
        outputfile=str(output_path),
        extra_args= extra_args
    )
    return output_path
