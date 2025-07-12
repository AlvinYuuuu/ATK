"""
Tools for parsing and extracting text from various document formats.
"""
from markitdown import MarkItDown

def parse_document(file_path: str) -> str:
    """
    Parses a document (PDF, DOCX, etc.) from the given file path
    and converts its content to Markdown.

    Args:
        file_path: The local path to the document to be parsed.

    Returns:
        The content of the document as a Markdown string.
    """
    if not file_path:
        return "Error: A file path must be provided."

    print(f"Parsing document at path: {file_path}")
    try:
        # The markitdown library automatically handles different file types
        # based on the file extension and content.
        markdown_content = MarkItDown(file_path)
        print("Successfully converted document to Markdown.")
        return markdown_content
    except Exception as e:
        print(f"Error parsing document {file_path}: {e}")
        # Return a descriptive error message to the agent.
        return f"Error: Could not parse the document. Details: {str(e)}"
