from config.logger import logger
from config.settings import settings
from langchain_ollama import OllamaLLM
from retrieval.retriever import retriver_builder
from generation.prompt import PromptBuilder


class RAGChain:

    def __init__(self) -> None:
        self.prompt = PromptBuilder().get_prompt()
        self.llm = OllamaLLM(
            model = settings.OLLAMA_MODEL,base_url=settings.OLLAMA_URL
        )
        self.retriver = retriver_builder().get_retriver()
        self.logger = logger
    
    def format_docs(self,docs):
        return "\n\n".join([f"Page {doc.metadata.get('page','?')}: {doc.page_content}" for doc in docs])


    def invoke(self, question):

        # retrived the chunks from the chroma db

        docs = self.retriver.invoke(question)
        self.logger.info(docs)

        # format the context keep in a stream line as a string
        context = self.format_docs(docs)
        # self.logger.info(context)

        # build the prompt
        prompt_value = self.prompt.invoke({
            "context" : context,
            "question": question
        })

        self.logger.info(f"Invoking LLM witht he {prompt_value}")
        
        # generate the answer
        answer = self.llm.invoke(prompt_value)

        self.logger.info(f"LLM Generated answer is : {answer}")

        # build the source list:
        sources =  [
            {
                "page" : doc.metadata.get("page","?"),
                "type" : doc.metadata.get("type","?"),
                "source": doc.metadata.get("source","?")
            }
            for doc in docs
        ]
        
        self.logger.info(f"sources generated are : {sources}")

        
        self.logger.info(f"Query answered — {len(docs)} chunks retrieved")

        return {"answer" : answer, "sources" : sources}