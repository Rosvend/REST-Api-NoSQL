import asyncio
from app.db.mongo import client

async def ping():
    try:
        await client.admin.command("ping")
        print(":) connected to MongoDB successfully!")
    except Exception as e:
        print("damn failed to connect:", e)

asyncio.run(ping())