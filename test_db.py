import asyncio
import os
from dotenv import load_dotenv
from db_client import SafePostgresClient

async def test_db():
    load_dotenv()
    client = SafePostgresClient()
    db_uri = f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@localhost/postgres"
    
    try:
        await client.connect(db_uri)
        # Test if we can list tables
        tables = await client.conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        print("Available tables:", [t['table_name'] for t in tables])
        
        # Get users table schema
        schema = await client.conn.fetch("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users'
        """)
        print("\nUsers table schema:")
        for col in schema:
            print(f"- {col['column_name']}: {col['data_type']}")
        
        # Test the users table specifically
        users = await client.conn.fetch("SELECT * FROM users LIMIT 1")
        print("\nUsers table exists and has data:", bool(users))
        if users:
            print("Sample user data:", dict(users[0]))
        
    except Exception as e:
        print("Error:", str(e))
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_db()) 