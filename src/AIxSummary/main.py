import streamlit as st
from docx import Document
import fitz
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from AIxSummary.crew import AIxSummary



def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_docx(docx_file):
    """Extracts text from a DOCX file."""
    doc = Document(docx_file)
    text = " ".join([para.text for para in doc.paragraphs])
    return text

def process_file(file):
    """Processes the uploaded file using CrewAI."""
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        st.error("Unsupported file type. Please upload a .docx or .pdf file.")
        return None


def main():
    st.title("Summarize your documents with CrewAI")
    st.markdown("""
    Upload a `.docx` or `.pdf` file, summarize it using CrewAI and ask questions.
    """)

    # File upload
    uploaded_file = st.file_uploader("Upload your .docx or .pdf file", type=["docx", "pdf"])

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

    # Default instructions
    default_instructions = (
       "You are an expert document summarizer. Your task is to read the given document and provide a concise and informative summary while retaining the key details."
    )

    # Text area for modifying instructions
    instructions = st.text_area(
        "Edit the instructions for CrewAI (or keep the defaults below):",
        value=default_instructions,
        height=300
    )

    # Run button
    if st.button("Run"):
        if uploaded_file:
            with st.spinner("Processing the file..."):
                # Extract text
                extracted_text = process_file(uploaded_file)
                if extracted_text:
                    # Save the extracted text and instructions as input for CrewAI
                    inputs = {
                        "document": extracted_text,
                        "instructions": instructions
                    }
                    # Run CrewAI
                    AIxSummary().crew().kickoff(inputs=inputs)

                    # Check for the output file
                    report_path = "report.md"
                    if os.path.exists(report_path):
                        # Read the Markdown content
                        with open(report_path, "r", encoding="utf-8") as file:
                            markdown_content = file.read()

                        # Display the Markdown content
                        st.markdown("Summary")
                        st.markdown(markdown_content, unsafe_allow_html=True)
                    else:
                        st.error("Please ensure CrewAI generated the output.")
        else:
            st.error("Please upload a file before running.")


if __name__ == "__main__":
    main()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AIxSummary().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AIxSummary().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AIxSummary().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
