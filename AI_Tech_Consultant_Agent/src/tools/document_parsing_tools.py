"""
Tools for parsing and extracting text from various document formats.
"""
import os
from typing import List
from markitdown import MarkItDown

# Initialize the converter once, as per the correct usage.
md_converter = MarkItDown(enable_plugins=False)

def parse_documents(file_paths: List[str]) -> str:
    """
    Parses a list of documents (PDF, DOCX, etc.) from the given file paths
    and converts their content into a single Markdown string. Each document's
    content is separated by a clear marker.

    Args:
        file_paths: A list of local paths to the documents to be parsed.

    Returns:
        The concatenated content of the documents as a Markdown string.
    """
    if not file_paths:
        return "Error: A list of file paths must be provided."

    all_markdown_content = []
    for i, file_path in enumerate(file_paths):
        print(f"Parsing document {i+1}/{len(file_paths)} at path: {file_path}")
        try:
            # Use the single converter instance and access the .text_content attribute.
            markdown_content = md_converter.convert(file_path).text_content
            print("markdown_content: ", markdown_content)
            header = f"\n--- START OF DOCUMENT: {os.path.basename(file_path)} ---\n"
            footer = f"\n--- END OF DOCUMENT: {os.path.basename(file_path)} ---\n"
            all_markdown_content.append(header + str(markdown_content) + footer)
        except Exception as e:
            error_message = f"Error parsing document {file_path}: {e}"
            print(error_message)
            all_markdown_content.append(f"\n--- ERROR PARSING DOCUMENT: {os.path.basename(file_path)} ---\n{error_message}\n--- END OF ERROR ---\n")

    return "\n".join(all_markdown_content)
