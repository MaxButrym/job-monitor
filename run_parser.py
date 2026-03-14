from parser.job_parser import parse_jobs
from services.job_service import save_jobs


def main():

    print("🚀 Запуск парсера...")

    jobs = parse_jobs()

    save_jobs(jobs)


if __name__ == "__main__":
    main()