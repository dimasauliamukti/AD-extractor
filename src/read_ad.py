
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import os
from cleaning_text import text_cleaning,merge_paragraph,tag
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import os
from cleaning_text import text_cleaning, merge_paragraph, tag


def read_pdf(base_dir, file):
    file = os.path.join(base_dir, file)
    pdf = PyPDFLoader(file)
    pages = pdf.load()

    reconstructed_lines = []

    for page in pages:
        texts = text_cleaning(page.page_content)
        lines = texts.split("\n")
        if not lines:
            continue
        prev_line = lines[0]
        for next_line in lines[1:]:
            merged_line = merge_paragraph(prev_line, next_line)
            if merged_line != prev_line:
                prev_line = merged_line
                continue

            tag_result = tag(prev_line)
            if tag_result:
                tag_name, score = tag_result
                metadata = page.metadata.copy()
                metadata["tag"] = tag_name
                metadata["score"] = score

                reconstructed_lines.append(
                    Document(page_content=prev_line, metadata=metadata)
                )

            prev_line = next_line

        tag_result = tag(prev_line)
        if tag_result:
            tag_name, score = tag_result
            metadata = page.metadata.copy()
            metadata["tag"] = tag_name
            metadata["score"] = score
            reconstructed_lines.append(
                Document(page_content=prev_line, metadata=metadata))

    final_dict = {}
    for doc in reconstructed_lines:
        tag_name = doc.metadata.get("tag")
        if not tag_name:
            continue

        final_dict.setdefault(tag_name, "")
        final_dict[tag_name] += " " + doc.page_content

    return final_dict