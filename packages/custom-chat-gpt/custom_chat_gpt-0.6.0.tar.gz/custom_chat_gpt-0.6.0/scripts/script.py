from operator import itemgetter

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rich.console import Console
from rich.live import Live

prompt = ChatPromptTemplate.from_template(
    "Given a string, write a regex that removes the last 3 characters from the string.\n\n{topic}"
)
model = ChatOpenAI(model="gpt-4-turbo-preview")
output_parser = StrOutputParser()

chain = prompt | model | output_parser


console = Console()

res = ""
for chunk in chain.stream({"topic": "ice cream"}):
    res += chunk
    print(chunk, end="", flush=True)


with Live(console=console, refresh_per_second=4) as live:
    chain.invoke({"topic": "ice cream"})


model = ChatOpenAI()
events = []

for event in model.astream_events("hello", version="v1"):
    events.append(event)


vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

retrieval_chain.invoke("where did harrison work?")


console = Console()

# video_url = "https://www.youtube.com/watch?v=NYSWn1ipbgg" "https://www.youtube.com/watch?v=L_Guz73e6fw"
url = "https://www.youtube.com/watch?v=ftmdDlwMwwQ"
language = "en"
db = create_db_from_youtube_video_url(url, language, console)

llm = ChatOpenAI(temperature=0.1)


template = """
You are a helpful assistant that that can answer questions about youtube videos 
based on the video's transcript.

Answer the following question: {question}
By searching the following video transcript: {context}

Only use the factual information from the transcript to answer the question.

If you feel like you don't have enough information to answer the question, say "I don't know".

Your answers should be verbose and detailed.
"""
prompt = ChatPromptTemplate.from_template(template)

# chain = LLMChain(llm=llm, prompt=prompt)

chain = (
    {
        "context": itemgetter("question") | db.as_retriever(),
        "question": itemgetter("question"),
    }
    | prompt
    | llm
    | StrOutputParser()
)

console.print("[blue][b]Assistant :[/b][/blue]")

for chunk in chain.stream({"question": "what is the video about?"}):
    console.print(chunk, end="", style="green")
