import streamlit as st
import os
import PyPDF2
import textract
import docx
import re

# Function to preprocess and vectorize the documents


# Function to retrieve relevant documents based on the query using word matching
def retrieve_relevant_documents(query, documents):
    relevant_documents = []
    for document_text in documents:
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', document_text)
        relevant_sentences = []
        for sentence in sentences:
            if re.search(r'\b{}\b'.format(query.lower()), sentence.lower()):
                relevant_sentences.append(sentence)
        if relevant_sentences:
            relevant_documents.append('\n'.join(relevant_sentences))
    return relevant_documents

# Function to display relevant documents along with the relevant text
def display_relevant_documents(relevant_documents):
    if relevant_documents:
        st.subheader("Relevant Documents:")
        for index, relevant_document in enumerate(relevant_documents):
            st.write(f"Document {index+1}:")
            st.write(relevant_document)
            st.write("(End of relevant text)")
    else:
        st.write("No relevant information found in the documents.")

# Streamlit web application
def main():
    st.title("AI Document Retrieval System")

    # Sidebar for uploading files
    st.sidebar.title("Upload Documents")
    uploaded_files = st.sidebar.file_uploader("Upload documents", accept_multiple_files=True)

    if uploaded_files:
        # Process uploaded documents
        documents = []
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith('.pdf'):
                # Extract text from PDF using PyPDF2
                text = extract_text_from_pdf(uploaded_file)
                documents.append(text)
            elif uploaded_file.name.endswith('.docx'):
                # Extract text from DOCX using python-docx
                text = extract_text_from_docx(uploaded_file)
                documents.append(text)
            else:
                # Decode text files directly as UTF-8
                documents.append(uploaded_file.getvalue().decode('utf-8'))

        # Main content
        st.header("Enter your query")
        query = st.text_input("")

        if st.button("Search") and query:
            # Preprocess the query to remove common words
            cleaned_query = preprocess_query(query)

            # Retrieve relevant documents based on the cleaned query using word matching
            relevant_documents = retrieve_relevant_documents(cleaned_query, documents)

            # Display relevant documents and text
            display_relevant_documents(relevant_documents)

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file using PyPDF2."""
    pdf_text = ""
    with uploaded_file as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            pdf_text += page.extract_text()
    return pdf_text

def extract_text_from_docx(uploaded_file):
    """Extract text from a DOCX file using python-docx."""
    doc = docx.Document(uploaded_file)
    paragraphs = [p.text for p in doc.paragraphs]
    return '\n'.join(paragraphs)

def preprocess_query(query):
    """Preprocess the query to remove common words."""
    # Add more patterns if needed
    unnecessary_words = ["what", "is", "means", "different", "why", "how"]
    cleaned_query = query.lower()
    for word in unnecessary_words:
        cleaned_query = cleaned_query.replace(word, "")
    return cleaned_query.strip()

if __name__ == "__main__":
    main()
