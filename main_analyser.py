
def analyse(people, all_people, config):
    import logging
    logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info("Analyse started")
    from PersonAnalyser import run, chunkify
    import pp
    import math
    job_server = pp.Server(restart=True)
    chunks = chunkify(people, math.floor(job_server.get_ncpus() / 2) - 1)
    logging.info("Number of chunks: " + str(len(chunks)))
    jobs = []
    for chunk in chunks:
        from comparison import damerau_levenshtein_distance
        job = job_server.submit(run, (chunk, all_people, config), (damerau_levenshtein_distance,),
                                ("collections", "Person", "getData"))
        jobs.append(job)
    logging.info("Jobs started")
    results = []
    people = None
    all_people = None
    for job in jobs:
        re = job()
        results.extend(re)
    logging.info("Jobs done")
    job_server.print_stats()
    return results
