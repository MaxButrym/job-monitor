def filter_jobs(jobs):

    filtered = []

    for job in jobs:

        title = job["title"].lower()
        location = job["location"].lower()

        if "python" in title:

            filtered.append(job)

        elif "remote" in location:

            filtered.append(job)

    return filtered