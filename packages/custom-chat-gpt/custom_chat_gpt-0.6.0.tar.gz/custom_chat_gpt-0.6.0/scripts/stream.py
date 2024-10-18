from typing import Iterator, List

from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from rich.console import Console

prompt = ChatPromptTemplate.from_template(
    "Write a comma-separated list of 5 animals similar to: {animal}"
)
model = ChatOpenAI(temperature=0.0)

str_chain = prompt | model | StrOutputParser()

console = Console()

console.size.width 
console.width = min(80, console.width)


for chunk in str_chain.stream({"animal": "bear"}):
    console.print(chunk, end="", style="green")