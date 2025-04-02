import asyncio
from query_generator import QueryGenerator

async def test():
    generator = QueryGenerator()
    await generator.setup()
    # Test destructive query
   # print(await generator.generate_query("Delete all users"))
    # Test large scan
    print(await generator.generate_query("Show all users records"))

if __name__ == "__main__":
    asyncio.run(test())
