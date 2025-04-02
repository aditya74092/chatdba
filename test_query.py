import asyncio
from query_generator import QueryGenerator

async def main():
    generator = QueryGenerator()
    await generator.setup()
    try:
        query_result = await generator.generate_query("Count all users")
        print("Generated SQL:", query_result)
    finally:
        await generator.client.close()

if __name__ == "__main__":
    asyncio.run(main())