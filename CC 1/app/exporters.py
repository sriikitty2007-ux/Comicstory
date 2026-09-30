from datetime import datetime

from fpdf import FPDF

from .config import get_settings


def _safe_pdf_text(value: str) -> str:
    """
    Built-in Helvetica fonts in FPDF are Latin-1.
    Replace unsupported characters so PDF generation doesn't fail.
    """

    return (
        value
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def save_pdf(
    layout: list[dict],
    comic_id: str,
) -> str:

    settings = get_settings()

    filename = (
        f"comic_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
        f"{comic_id[:8]}.pdf"
    )

    output_path = (
        settings.exports_dir / filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        pdf.cell(
            0,
            12,
            _safe_pdf_text(
                f"Panel {panel['panel_number']}: "
                f"{panel['title']}"
            ),
            ln=True,
        )

        image_file = (
            settings.static_dir
            / panel["image_path"]
            .removeprefix("/static/")
        )

        if image_file.exists():

            pdf.image(
                str(image_file),
                x=15,
                y=30,
                w=180,
                h=100,
            )

        pdf.set_y(138)

        pdf.set_font(
            "Helvetica",
            "I",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            _safe_pdf_text(
                panel["scene_description"]
            ),
        )

        pdf.ln(3)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            _safe_pdf_text(
                "Caption: "
                + panel["caption"]
            ),
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            _safe_pdf_text(
                "Narration: "
                + panel["narration"]
            ),
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            0,
            7,
            _safe_pdf_text(
                "Dialogue: "
                + panel["dialogue"]
            ),
        )

    pdf.output(
        str(output_path)
    )

    return f"/static/exports/{filename}"