#AI Processing Module 
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI  # Updated import
from langchain_community.vectorstores import FAISS  # Updated import
from langchain_openai import OpenAI
from database import IncidentDB
from datetime import datetime
class AIProcessor:
    def __init__(self):
        self.llm = OpenAI(
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")  # Load from .env
        )
class AIProcessor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.db = IncidentDB()
        self.index = None
        self._initialize_vector_index()
    
    def _initialize_vector_index(self):
        incidents = self.db.collection.find({})
        error_texts = [inc["error_message"] for inc in incidents]
        
        if error_texts:
            embeddings = self.model.encode(error_texts)
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings)
        else:
            self.index = None
    
    def find_similar_errors(self, error_message, k=3):
        if not self.index:
            return []
        
        query_embedding = self.model.encode([error_message])
        distances, indices = self.index.search(query_embedding, k)
        
        incidents = list(self.db.collection.find({}))
        return [incidents[i] for i in indices[0]]
    
    def generate_solution(self, error_message):
        similar_errors = self.find_similar_errors(error_message)
        
        if not similar_errors:
            similar_errors = self.db.search_errors(error_message)
        
        context = "\n\n".join([
            f"Error: {err['error_message']}\nSolution: {', '.join(err['solution_steps'])}" 
            for err in similar_errors
        ])
        
        from langchain_core.prompts import PromptTemplate  # Updated import
        
        template = """As a senior DevOps engineer, analyze this error:
        
        Past Similar Incidents:
        {context}
        
        Current Error:
        {error_message}
        
        Provide:
        1. Root cause analysis
        2. Step-by-step resolution
        3. Verification steps
        4. Prevention recommendations"""
        
        prompt = PromptTemplate(
            input_variables=["context", "error_message"],
            template=template
        )
        
        llm = OpenAI(temperature=0.3)
        return llm(prompt.format(context=context, error_message=error_message))