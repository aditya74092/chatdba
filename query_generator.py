import os
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_ollama import OllamaLLM
from langchain.chains import create_sql_query_chain
from dotenv import load_dotenv
from db_client import SafePostgresClient
load_dotenv()

class QueryGenerator:
    def __init__(self, db_uri=None):
        self.client = SafePostgresClient()
        self.db_uri = db_uri or f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@localhost/postgres"
        self.llm = OllamaLLM(model="llama3:8b", temperature=0)
        self.db = SQLDatabase.from_uri(self.db_uri)
        self._is_connected = False
        
    async def setup(self):
        if not self._is_connected:
            await self.client.connect(self.db_uri)
            self._is_connected = True
        
    async def generate_query(self, question):
        if not self._is_connected:
            await self.setup()
            
        chain = create_sql_query_chain(llm=self.llm, db=self.db)
        raw_query = chain.invoke({"question": question})
        print("Generated raw query:", raw_query)  # Debug print
        
        # If the response is a natural language message, return it directly
        if raw_query.strip().startswith(('I ', 'Sorry', 'The')):
            return raw_query
            
        # Extract SQL query from formatted response
        if "SQLQuery:" in raw_query:
            raw_query = raw_query.split("SQLQuery:")[1].strip()
            
        try:
            # For testing, let's try a direct query first
            if question.lower().startswith("show") or question.lower().startswith("select"):
                test_query = "SELECT user_id, name FROM users LIMIT 5"
                print("Testing with direct query:", test_query)
                _, result = await self.client.safe_execute(test_query)
                return result
                
            _, result = await self.client.safe_execute(raw_query)
            return result
        except (PermissionError, Warning) as e:
            return str(e)