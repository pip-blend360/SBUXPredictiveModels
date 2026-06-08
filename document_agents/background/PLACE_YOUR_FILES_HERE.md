# Background Materials Folder

Place your source documents and reference materials in this folder.

## Supported File Types

- PDF documents (`.pdf`)
- Markdown files (`.md`)
- Text files (`.txt`)
- Word documents (`.docx`)
- PowerPoint presentations (`.pptx`)
- Data files (`.csv`, `.json`, etc.)
- Any other reference materials

## Usage

The Writer Agent will read materials from this folder to understand context and requirements for the document you want to create.

**Example workflow:**
1. Place your source materials here (e.g., `original_spec.pdf`)
2. Add a requirements file (e.g., `rewrite_requirements.md`)
3. Run the orchestrator with a prompt referencing these files
4. The Writer Agent will use this context to create your document

## Example Structure

```
background/
├── original_document.pdf       # Document to rewrite/expand
├── requirements.md             # Your specific requirements
├── reference_material.pdf      # Additional context
├── data_dictionary.csv         # Supporting data
└── README.md                   # Instructions (this file)
```

## Tips

- **Use clear, descriptive filenames** - helps the Writer Agent understand what each file contains
- **Include all relevant context** - the more background you provide, the better the output quality
- **Add a requirements file** - specify exactly what you want in the final document
- **Reference files in your prompt** - e.g., "Rewrite original_document.pdf using the requirements in requirements.md"

## Example Requirements File

See `example_requirements.md` for a template you can copy and customize.
