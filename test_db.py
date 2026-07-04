import asyncio
# pyrefly: ignore [missing-import]
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user="postgres",
        password="password",
        database="mydb",
        host="localhost",
        port=5432,
    )
    print("Connected!")
    await conn.close()

asyncio.run(main())