from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import format_document
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from operator import itemgetter
import os
import re


class GeminiPlugin:
    def __init__(self,retr,model="gemini-pro",) -> None:
        llm = GoogleGenerativeAI(model=model, google_api_key=os.environ['GOOGLE_API_KEY'])
        prompt_template = """
        [INST]
        You are SPARQL Developer, Your task is to follow the SOP no matter what.:
        1. Read the Query asked by data analyst in english.
        2. Write a sparql query to retrieve the data from the database as requested by the data analyst.
        3. Use the given query-SPARQL query example to help you.
        4. Use only valid predcate and class names from the ontology like in the example. For example for the class atomic number use ae:number.
        5. output only the sparql query in the response and not anything else.
        6. The output should be a valid SPARQL query.
        7. Do not assume values for anything, all the values are available in the database. For example, do not assume that the atomic number of iron is 26. or the atomic radius of iron is 1.26.

        ### Example:
        {docs}

        ### QUESTION:
        {query}

        """
        RESPONSE_PROMPT = ChatPromptTemplate.from_template(prompt_template)
        memory = ConversationBufferMemory(return_messages=True, output_key="answer", input_key="query")
        loaded_memory = RunnablePassthrough.assign(chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("history"),)
        retrieved_documents = {
            "docs": itemgetter("query") | retr,
            "query": lambda x: x["query"],
            }
        final_inputs = {
            "docs": lambda x: x["docs"],
            "query": itemgetter("query"),
            }
        answer = {
            "answer": final_inputs | RESPONSE_PROMPT | llm,
            "query": itemgetter("query"),
            "docs": final_inputs["docs"]
            }
        
        self.final_chain = loaded_memory | retrieved_documents | answer
        
    def get_answer(self,query):
        return self.final_chain.invoke({"query": query})['answer']