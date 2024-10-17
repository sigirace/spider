import hashlib
import os
from langchain_core.documents import Document
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter


def generate_key(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def extract_pdf(file_path) -> tuple[list[str], float, float]:
    pages = []
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text = page.get_text()
            pages.append(text)
    create_time = os.path.getctime(file_path)
    modification_time = os.path.getmtime(file_path)

    return pages, create_time, modification_time


def split_docs(file_path: str, chunk_size: int, chunk_overlap: int) -> list[Document]:
    try:
        file_name = os.path.basename(file_path)

        pages, create_time, modification_time = extract_pdf(file_path=file_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        if len(pages) <= 0:
            raise ValueError("페이지가 없습니다.")

        docs = []
        previous_overlap = ""

        for page_number, page_text in enumerate(pages, start=1):
            page_text_with_overlap = previous_overlap + page_text
            chunks = splitter.split_text(page_text_with_overlap)

            if chunks:
                previous_overlap = chunks[-1][-50:]

            for chunk in chunks:
                hash_key = generate_key(chunk)
                docs.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "doc_name": file_name,
                            "page_number": page_number,
                            "creation_time": create_time,
                            "modification_time": modification_time,
                            "key": f"{file_name}_{page_number}_{hash_key}",
                        },
                    )
                )
        return docs
    except Exception as e:
        raise Exception(f"split document failed: {e}")
