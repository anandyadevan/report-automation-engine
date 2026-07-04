# Notebooks

These notebooks document the complete workflow used to build the reporting prototype.

Each notebook represents a distinct stage in the reporting architecture.

| Notebook | Purpose |
|----------|---------|
| **01_dataset_enrichment.ipynb** | Enrich the original dataset with additional subject-level scores used throughout the prototype. |
| **02_knowledge_library_builder.ipynb** | Build the base knowledge library containing report labels, interpretations, recommendations, and learning plans. |
| **03_llm_library_enhancement.ipynb** | Enhance the knowledge library with multiple writing styles using an LLM while preserving the original meaning. |
| **04_html_report_generation.ipynb** | Generate HTML reports by combining structured data, business rules, and the enhanced knowledge library. |
| **05_pdf_generation.ipynb** | Render HTML reports into print-ready PDF documents using Playwright. |

---

## Workflow

```text
Student Dataset
        ↓
Dataset Enrichment
        ↓
Knowledge Library
        ↓
LLM Enhancement
        ↓
HTML Report Generation
        ↓
PDF Rendering
```

These notebooks are intended to be executed sequentially.
