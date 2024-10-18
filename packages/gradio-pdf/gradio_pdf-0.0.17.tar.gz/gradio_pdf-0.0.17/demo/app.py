
import gradio as gr
from gradio_pdf import PDF
# from pdf2image import convert_from_path
# from transformers import pipeline
from pathlib import Path

dir_ = Path(__file__).parent

# p = pipeline(
#     "document-question-answering",
#     model="impira/layoutlm-document-qa",
# )

def qa(question: str, doc: str) -> str:
   return doc


demo = gr.Interface(
    qa,
    [PDF(label="Document")],
    PDF(),
    examples=[[str((dir_ / "invoice_2.pdf").resolve())],
              [str((dir_ / "sample_invoice.pdf").resolve())]]
)

if __name__ == "__main__":
    demo.launch()
