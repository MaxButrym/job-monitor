from config import KEYWORDS, LOCATIONS


def filter_jobs(jobs):

    filtered = []

    for job in jobs:

        title = job.get("title", "").lower()
        location = job.get("location", "").lower()

        keyword_match = any(keyword in title for keyword in KEYWORDS)
        location_match = any(loc in location for loc in LOCATIONS)

        if keyword_match and location_match:
            filtered.append(job)

    return filtered