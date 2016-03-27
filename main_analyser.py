
def analyse(people, homes, config):
    import logging
    logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("Analyse started")
    from PersonAnalyser import run, chunkify
    import pp
    import math
    job_server = pp.Server(restart=True)
    max_job_count = job_server.get_ncpus() - 1
    chunks = chunkify(people, max_job_count)
    logging.info("Number of chunks: " + str(len(chunks)))
    jobs = []
    results = []
    from comparison import damerau_levenshtein_distance
    for chunk in chunks:
        for chunk2 in chunks:
            job = job_server.submit(run, (chunk, chunk2, homes, config), (damerau_levenshtein_distance,),
                                    ("collections", "Person", "getData", "globals_scc"))
            jobs.append(job)
            if len(jobs) >= max_job_count:
                job = jobs.pop(0)
                re = job()
                results.extend(re)

    logging.info("Jobs started")
    # Handle the rest of the jobs
    for job in jobs:
        re = job()
        results.extend(re)
    logging.info("Jobs done")
    job_server.print_stats()
    return results
