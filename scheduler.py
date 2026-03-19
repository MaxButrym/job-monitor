import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from main import main


async def run_job():
    print("🚀 Запуск парсера...")
    await main()


async def start_scheduler():
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(run_job, "interval", minutes=1)  # тест
    
    scheduler.start()
    print("✅ Scheduler запущен")
    await run_job()
    # держим приложение живым
    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(start_scheduler())