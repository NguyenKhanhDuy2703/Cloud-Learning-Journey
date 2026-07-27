import boto3
import json
import os
import streamlit as st
import numpy as np
from typing import List, Dict, Tuple
import re
import PyPDF2
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import io
from dotenv import load_dotenv

class BedrockClient:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get AWS credentials from environment variables
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_session_token = os.getenv('AWS_SESSION_TOKEN')  # Optional, for temporary credentials
        aws_region = os.getenv('AWS_REGION', 'us-east-1')  # Default to us-east-1 if not specified
        
        # Create session with credentials from .env
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=aws_region
        )
        
        self.bedrock = session.client('bedrock-runtime', region_name=aws_region)
        self.bedrock_agent = session.client('bedrock-agent', region_name=aws_region)
        self.bedrock_agent_runtime = session.client('bedrock-agent-runtime', region_name=aws_region)
    
    def invoke_nova_pro(self, prompt, system_prompt="", max_tokens=1000, temperature=0.7, top_p=0.9):
        """Invoke Nova Pro for text-to-text generation"""
        try:
            body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p
                }
            }
            
            if system_prompt:
                body["system"] = [{"text": system_prompt}]
            
            response = self.bedrock.invoke_model(
                modelId="amazon.nova-pro-v1:0",
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['output']['message']['content'][0]['text']
            
        except Exception as e:
            st.error(f"Error invoking Nova Pro: {str(e)}")
            return None
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for a list of texts using Titan Embeddings"""
        try:
            # TODO: Excercise 2 Students specify the embedding model
            embedding_model = "amazon.titan-embed-text-v1"  # TODO: What Titan embedding model should be used?
            
            embeddings = []
            for text in texts:
                body = {
                    "inputText": text
                }
                
                response = self.bedrock.invoke_model(
                    modelId=embedding_model,
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                embeddings.append(response_body['embedding'])
            
            return embeddings
            
        except Exception as e:
            st.error(f"Error getting embeddings: {str(e)}")
            return []
    
    def list_knowledge_bases(self) -> List[Tuple[str, str]]:
        """List all Knowledge Bases in user's account"""
        try:
            response = self.bedrock_agent.list_knowledge_bases()
            knowledge_bases = []
            
            for kb in response.get('knowledgeBaseSummaries', []):
                kb_id = kb['knowledgeBaseId']
                kb_name = kb['name']
                knowledge_bases.append((kb_id, kb_name))
            
            return knowledge_bases
            
        except Exception as e:
            st.error(f"Error listing Knowledge Bases: {str(e)}")
            return []
    
    def query_knowledge_base(self, kb_id: str, query: str, max_tokens: int = 1500) -> Dict:
        """Query a Knowledge Base and return response with citations"""
        try:
            response = self.bedrock_agent_runtime.retrieve_and_generate(
                input={
                    'text': query
                },
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': kb_id,
                        'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0'
                    }
                }
            )
            
            # Extract response and citations
            output = response.get('output', {})
            text_response = output.get('text', '')
            citations = response.get('citations', [])
            
            # Return the raw response without any filtering
            return {
                'response': text_response,
                'citations': citations,
                'session_id': response.get('sessionId', ''),
                'model_used': 'nova-pro-v1:0',
                'raw_response': response  # Include full raw response for debugging
            }
            
        except Exception as e:
            st.error(f"Error querying Knowledge Base: {str(e)}")
            return {
                'response': f'Error querying Knowledge Base: {str(e)}',
                'citations': [],
                'session_id': '',
                'model_used': 'error',
                'raw_response': None
            }

class DocumentProcessor:
    """Handle different document types and web scraping"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """Extract text from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    @staticmethod
    def scrape_web_content(url: str) -> Tuple[str, str]:
        """Scrape content from a web URL
        
        Returns:
            Tuple of (title, content)
        """
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            
            # Set headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Make request with timeout
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Web Page"
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Extract main content
            # Try to find main content areas first
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article'))
            
            if main_content:
                content = main_content.get_text()
            else:
                content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            content = ' '.join(chunk for chunk in chunks if chunk)
            
            return title_text, content
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching URL: {str(e)}")
            return "", ""
        except Exception as e:
            st.error(f"Error processing web content: {str(e)}")
            return "", ""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

class SimpleRAG:
    """Simple in-memory RAG implementation for Study Buddy"""
    
    def __init__(self, bedrock_client: BedrockClient):
        self.bedrock_client = bedrock_client
        self.documents = []  # List of document chunks
        self.embeddings = []  # List of embeddings
        self.document_metadata = []  # List of metadata (filename, chunk_id, source_type)
        self.doc_processor = DocumentProcessor()
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """Add documents to the RAG system
        
        Args:
            documents: List of dicts with 'content', 'filename', 'chunk_id', and 'source_type'
        """
        if not documents:
            return
        
        # Extract text content for embedding
        texts = [doc['content'] for doc in documents]
        
        # Get embeddings
        with st.spinner("Creating embeddings for documents..."):
            new_embeddings = self.bedrock_client.get_embeddings(texts)
        
        if new_embeddings:
            # Add to storage
            self.documents.extend(documents)
            self.embeddings.extend(new_embeddings)
            self.document_metadata.extend([
                {
                    'filename': doc['filename'], 
                    'chunk_id': doc['chunk_id'],
                    'source_type': doc.get('source_type', 'file')
                } 
                for doc in documents
            ])
            
            st.success(f"Added {len(documents)} document chunks to knowledge base")
    
    def add_files(self, uploaded_files):
        """Process and add uploaded files to the RAG system"""
        if not uploaded_files:
            return
        
        documents = []
        for file in uploaded_files:
            try:
                # Determine file type and extract content
                if file.type == "application/pdf":
                    content = self.doc_processor.extract_text_from_pdf(file)
                    source_type = "pdf"
                elif file.type in ["text/plain", "text/markdown"]:
                    content = file.read().decode('utf-8')
                    source_type = "text"
                else:
                    st.warning(f"Unsupported file type: {file.type}")
                    continue
                
                if content.strip():
                    # Chunk the document
                    chunks = self.chunk_text(content)
                    
                    for i, chunk in enumerate(chunks):
                        documents.append({
                            'content': chunk,
                            'filename': file.name,
                            'chunk_id': i,
                            'source_type': source_type
                        })
                else:
                    st.warning(f"No text content found in {file.name}")
                    
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
        
        if documents:
            self.add_documents(documents)
    
    def add_web_content(self, urls: List[str]):
        """Scrape and add web content to the RAG system"""
        if not urls:
            return
        
        documents = []
        for url in urls:
            try:
                if not self.doc_processor.is_valid_url(url):
                    st.warning(f"Invalid URL: {url}")
                    continue
                
                with st.spinner(f"Scraping content from {url}..."):
                    title, content = self.doc_processor.scrape_web_content(url)
                
                if content.strip():
                    # Chunk the content
                    chunks = self.chunk_text(content)
                    
                    for i, chunk in enumerate(chunks):
                        documents.append({
                            'content': chunk,
                            'filename': title or url,
                            'chunk_id': i,
                            'source_type': 'web'
                        })
                else:
                    st.warning(f"No content extracted from {url}")
                    
            except Exception as e:
                st.error(f"Error processing {url}: {str(e)}")
        
        if documents:
            self.add_documents(documents)
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings near the chunk boundary
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            vec1_np = np.array(vec1)
            vec2_np = np.array(vec2)
            
            dot_product = np.dot(vec1_np, vec2_np)
            norm1 = np.linalg.norm(vec1_np)
            norm2 = np.linalg.norm(vec2_np)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except:
            return 0.0
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve most relevant document chunks for a query"""
        if not self.documents or not self.embeddings:
            return []
        
        # Get query embedding
        query_embeddings = self.bedrock_client.get_embeddings([query])
        if not query_embeddings:
            return []
        
        query_embedding = query_embeddings[0]
        
        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self.cosine_similarity(query_embedding, doc_embedding)
            similarities.append({
                'index': i,
                'similarity': similarity,
                'content': self.documents[i]['content'],
                'metadata': self.document_metadata[i]
            })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]
    
    def clear_documents(self):
        """Clear all stored documents"""
        self.documents = []
        self.embeddings = []
        self.document_metadata = []
