from langchain_core.prompts import ChatPromptTemplate
from config.logger import logger

class PromptBuilder:

    def __init__(self) -> None:
        
        self.logger = logger
        self.template = ChatPromptTemplate.from_messages([

            ("system", """
                You are a helpful assistant that answers questions 
                based on the provided document context only.
                
                Rules:
                - Answer only from the context provided
                - If answer not in context → say "I don't know based on the document"
                - Be concise and specific
            """),
            ("human", """
                    Context from document:
                    {context}
                    
                    Question: {question}
                    
                    Answer:
            """)

        ])

    def get_prompt(self):
        return self.template