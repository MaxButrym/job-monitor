import asyncio

from fastapi import FastAPI
from api.job import router as job_router

from database.db import engine
from database import models
from parser.job_parser import parse_jobs
from services.job_filter import filter_jobs
from services.job_service import save_jobs

app = FastAPI()

app.include_router(job_router)

async def main():
    models.Base.metadata.create_all(bind=engine)

    jobs = parse_jobs()
    print("Jobs parsed:", len(jobs))

    filtered_jobs = filter_jobs(jobs)
    print("Jobs after filter:", len(filtered_jobs))

    print("Calling save_jobs...")
    await save_jobs(filtered_jobs)

    print("Finished")


if __name__ == "__main__":
    asyncio.run(main())