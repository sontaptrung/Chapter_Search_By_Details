from .defaults import ANSWER_PROMPT, VALIDATE_CONTEXT_PROMPT, SUMMARIZE_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from llm import Llama3Engine
from vector_database import QdrantEngine
class Generator:
    def __init__(self, llm:Llama3Engine, vector_db: QdrantEngine):
        self._llm = llm
        self._vector_db = vector_db
    def run(self, query: str, task="answer"):
        if task == "answer":
            retrieve_contexts = self.run(query=query, task = "validate")
            if retrieve_contexts !=None:
                prompt_template = ChatPromptTemplate(ANSWER_PROMPT)
                output_parser = StrOutputParser()
                chain = prompt_template | self._llm | output_parser
                return chain.invoke({"source_knowledge": retrieve_contexts, "query" : query})
            else :
                return "Xin lỗi tôi không thể trả lời câu hỏi của bạn!"
        elif task == "validate":
            top_10_retrieve = self._vector_db.search(query=query)
            i=0
            for i in range(3):
                top_3 = top_10_retrieve[i*3:i*3+3]
                source_knowledge = "\n".join([f"The excerpt is from chapter: {x.metadata['chapter_title']}\nChapter content: {x.metadata['chunk_content']}\n" for x in top_3])
                prompt_template = ChatPromptTemplate(VALIDATE_CONTEXT_PROMPT)
                chain = prompt_template | self._llm
                completion = chain.invoke({"source_knowledge": source_knowledge, "query" : query})
                response = int(completion.content.strip())
                if response == 1:
                    return source_knowledge
                else:
                    continue
            return None
        elif task == "summarize":
            prompt_template = ChatPromptTemplate(SUMMARIZE_PROMPT)
            
            
    # def decide_top_3_to_answer(self, vector_db: QdrantEngine, query:str) -> str:
    #     top_10_retrieve = vector_db.run(query)
    #     i=0
    #     for i in range(3):
    #         top_3 = top_10_retrieve[i*3:i*3+3]
    #         source_knowledge = "\n".join([f"The excerpt is from chapter: {x.metadata['chapter_title']}\nChapter content: {x.metadata['chunk_content']}\n" for x in top_3])
    #         prompt_template = ChatPromptTemplate(VALIDATE_CONTEXT_PROMPT)
    #         chain = prompt_template | self._llm
    #         completion = chain.invoke(source_knowledge=source_knowledge, query = query)
    #         response = int(completion.content.strip())
    #         if response == 1:
    #             return source_knowledge
    #         else:
    #             continue
    #     return None
    