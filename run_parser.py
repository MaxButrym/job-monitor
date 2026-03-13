from parser.job_parser import parse_jobs
from services.job_service import save_jobs


def main():

    jobs = parse_jobs()

    print(f"Найдено вакансий: {len(jobs)}")

    save_jobs(jobs)

    print("Вакансии сохранены в базу")


if __name__ == "__main__":
    main()