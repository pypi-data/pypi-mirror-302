from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from rich.console import Console

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
