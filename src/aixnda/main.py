import streamlit as st
from docx import Document
import fitz  # PyMuPDF for PDF processing
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from aixnda.crew import Aixnda


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
    st.title("CrewAI NDA Document Analyzer")
    st.markdown("""
    Upload a `.docx` or `.pdf` file, process it using CrewAI, and download the output 
    as a PDF file.
    """)

    # File upload
    uploaded_file = st.file_uploader("Upload your .docx or .pdf file", type=["docx", "pdf"])

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

    # Default instructions
    default_instructions = (
        "When reviewing an NDA, ensure the following elements are clearly defined:\n"
        "1. Confidential Information: Clearly defines what constitutes confidential information.\n"
        "2. Obligations for Protection: Outlines the obligations for protection and permissible use.\n"
        "3. Exclusions: Specifies exclusions for public, independently developed, or received information without restriction.\n"
        "4. Duration of Confidentiality: States the duration of confidentiality.\n"
        "5. Post-Agreement Procedures: Details procedures for returning or destroying information after the agreement ends.\n"
        "6. Permissible Disclosures: Outlines disclosures under legal compulsion with provisions for notification and minimizing disclosure.\n"
        "7. Enforceable Remedies: Includes enforceable remedies for breaches of confidentiality.\n"
        "8. Governing Law and Dispute Resolution: Specifies the governing law and dispute resolution mechanisms.\n"
        "9. Binding on All Parties: Ensures that all related parties, including affiliates and successors, are bound by the terms.\n"
        "10. Non-Solicit or Non-Compete Clauses: Check for any applicable non-solicit or non-compete clauses.\n\n"
        "These steps help protect the integrity of confidential information and safeguard the interests of all parties involved."
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
                        "nda_document": extracted_text,
                        "instructions": instructions
                    }
                    # Run CrewAI
                    Aixnda().crew().kickoff(inputs=inputs)

                    # Check for the output file
                    report_path = "report.md"
                    if os.path.exists(report_path):
                        # Read the Markdown content
                        with open(report_path, "r", encoding="utf-8") as file:
                            markdown_content = file.read()

                        # Display the Markdown content
                        st.markdown("### Generated Report")
                        st.markdown(markdown_content, unsafe_allow_html=True)


                    else:
                        st.error("The output file (report.md) was not found. Please ensure CrewAI generated the output.")
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
        Aixnda().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Aixnda().crew().replay(task_id=sys.argv[1])

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
        Aixnda().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
