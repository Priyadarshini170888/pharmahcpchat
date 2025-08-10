
from transformers import pipeline
import config

chat_pipeline = pipeline("text2text-generation", model=config.HUGGINGFACE_MODEL)

def generate_response(question, context):
    prompt = f"Answer the question based on the context:\n\nContext:\n{context}\n\nQuestion: {question}"
    result = chat_pipeline(prompt, max_length=512, truncation=True)
    return result[0]['generated_text']
