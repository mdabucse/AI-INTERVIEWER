from sentence_transformers import SentenceTransformer
import pinecone
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from groq import Groq

client = Groq(
    api_key="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",
)

model = SentenceTransformer('all-MiniLM-L6-v2')
index_name = "interviewer"
pc = pinecone.Pinecone(api_key="ad424572-ce07-4c33-ba4b-23d7e86f71f0")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

def make_chunks(text):
    return text_splitter.split_text(text)

def get_context(ques,tot2):
    index = pc.Index(index_name)
    ques_emb = model.encode(ques)
    DB_response = index.query(
        vector=ques_emb.tolist(),
        top_k=3,
        include_values=True
    )

    if DB_response is None or 'matches' not in DB_response:
        return ""

    cont = ""
    for i in range(len(DB_response['matches'])):
        try:
            chunk_index = int(DB_response['matches'][i]['id'][3:]) - 1
            # cont += tot2[chunk_index]
            print(tot2[chunk_index])
        except (IndexError, ValueError) as e:
            print(f"Error accessing chunk: {e}")
            print(f"Chunk ID: {DB_response['matches'][i]['id']}, Chunk Index: {chunk_index}")
    return cont

def extract_pdf(path):
    reader = PdfReader(path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text

uploaded_files = r'Mohamed_Abubakkar_S_22AD051.pdf'
read_pdf = extract_pdf(uploaded_files)
tot_chunks = make_chunks(read_pdf)
# print(tot_chunks[0])

tot_embeddings = model.encode(tot_chunks)
tot_vectors = [{"id": f"vec{i+1}", "values": vec.tolist()} for i, vec in enumerate(tot_embeddings)]
print(type(tot_vectors))

try:
    pc.describe_index(index_name)
    print("Index already exists. Skipping creation.")
except pinecone.core.client.exceptions.NotFoundException:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=pinecone.ServerlessSpec(cloud='aws', region='us-east-1')
    )
    print("Index created successfully.")

index = pc.Index(index_name)
index.upsert(tot_vectors)
print("Documents processed and indexed successfully!")
query = input("Enter your query:")
context = get_context(query,tot_chunks)
print(context)  
if context:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Context: {context}, Analyse and understand the above context completely and answer the below query, Query: {query}",
            }
        ],
        model="llama3-8b-8192",
    )
    response_text = chat_completion.choices[0].message.content
    print("Answer:")
    print(response_text)