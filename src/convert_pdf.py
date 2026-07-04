from playwright.sync_api import sync_playwright
import os

HTML_DIR = "outputs_html"
PDF_DIR = "outputs_pdf"

os.makedirs(PDF_DIR, exist_ok=True)

html_files = sorted([
    f for f in os.listdir(HTML_DIR)
    if f.endswith(".html")
])

PRINT_FIX_CSS = """
@page {
    size: A4;
    margin: 20mm 0 18mm 0 !important;
}

@media print {
    .footer {
        display: none !important;
    }

    body {
        background: white !important;
    }

    .page {
        width: auto !important;
        min-height: auto !important;
        margin: 0 !important;
        padding: 0 18mm !important;
        page-break-after: always;
    }

    .note-card {
        break-inside: avoid;
        page-break-inside: avoid;
    }

    .learning-plan-section {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
    }

    .plan-table-wrapper {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
    }

    .plan-table {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
    }

    .plan-table tr {
        break-inside: avoid;
        page-break-inside: avoid;
    }

    thead {
        display: table-header-group;
    }
}
"""

FOOTER_TEMPLATE = """
<div style="
    width:100%;
    padding:0 18mm;
    font-size:8px;
    color:#6b7280;
    font-family:Arial, sans-serif;
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
">
    <div>
        Page <span class="pageNumber"></span>
    </div>

    <div style="text-align:right; line-height:1.4;">
        <strong>Portfolio Project by Anandya Devan Alfarizky</strong><br>
        anandyadevan@gmail.com • linkedin.com/in/anandyadevan
    </div>
</div>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for html_file in html_files:
        html_path = os.path.abspath(os.path.join(HTML_DIR, html_file))
        pdf_path = os.path.join(PDF_DIR, html_file.replace(".html", ".pdf"))

        page.goto(f"file:///{html_path}", wait_until="networkidle")

        # Inject CSS khusus PDF
        page.add_style_tag(content=PRINT_FIX_CSS)

        page.emulate_media(media="print")

        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template="<div></div>",
            footer_template=FOOTER_TEMPLATE,
            margin={
                "top": "0mm",
                "right": "0mm",
                "bottom": "0mm",
                "left": "0mm"
            }
        )

        print(f"Created: {pdf_path}")

    browser.close()