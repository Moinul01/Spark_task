import os
from pathlib import Path
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

class RAGPipeline:
    def __init__(self, knowledge_base_path: Optional[str] = None):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        self.vector_store = None
        self.knowledge_base_path = knowledge_base_path or "knowledge_base"
        
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize or load vector store"""
        vector_store_path = Path(self.knowledge_base_path) / "faiss_index"
        
        if vector_store_path.exists():
            try:
                self.vector_store = FAISS.load_local(
                    str(vector_store_path), 
                    self.embeddings
                )
                print(f"Loaded existing vector store with {self.vector_store.index.ntotal} documents")
            except Exception as e:
                print(f"Error loading vector store: {e}. Creating new one...")
                self._create_empty_vector_store()
        else:
            self._create_empty_vector_store()
    
    def _create_empty_vector_store(self):
        """Create empty vector store"""
        # Create with a dummy document
        dummy_doc = Document(
            page_content="This is a placeholder document.",
            metadata={"source": "system", "title": "Placeholder"}
        )
        self.vector_store = FAISS.from_documents([dummy_doc], self.embeddings)
        self._save_vector_store()
        print("Created new vector store")
    
    def _save_vector_store(self):
        """Save vector store to disk"""
        vector_store_path = Path(self.knowledge_base_path) / "faiss_index"
        vector_store_path.parent.mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(str(vector_store_path))
        print(f"Saved vector store to {vector_store_path}")
    
    def add_documents(self, documents: List[Document]):
        """Add documents to knowledge base"""
        if not documents:
            return
        
        chunks = self.text_splitter.split_documents(documents)
        if self.vector_store.index.ntotal == 1 and "Placeholder" in self.vector_store.docstore._dict:
            # Replace the placeholder
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vector_store.add_documents(chunks)
        
        self._save_vector_store()
        print(f"Added {len(chunks)} chunks to knowledge base")
    
    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """Retrieve relevant documents for a query"""
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            
            # Filter out placeholder if it's the only result
            if len(docs) == 1 and "Placeholder" in str(docs[0].metadata.get('title', '')):
                return []
            
            return docs
        except Exception as e:
            print(f"Error in retrieval: {e}")
            return []
    
    def update_knowledge_base(self, documents: List[dict]):
        """Update knowledge base with new documents"""
        docs = []
        from datetime import datetime
        
        for doc in documents:
            docs.append(Document(
                page_content=doc.get("content", ""),
                metadata={
                    "source": doc.get("source", "unknown"),
                    "title": doc.get("title", "Untitled"),
                    "added_at": doc.get("added_at", datetime.now().isoformat()),
                    "type": doc.get("type", "article")
                }
            ))
        
        self.add_documents(docs)
    
    def get_stats(self):
        """Get statistics about the knowledge base"""
        if not self.vector_store:
            return {"total_documents": 0}
        
        return {
            "total_documents": self.vector_store.index.ntotal,
            "dimension": self.vector_store.index.d if hasattr(self.vector_store.index, 'd') else None,
        }