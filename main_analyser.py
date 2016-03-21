
def analyse(people, all_people, config):
    from PersonAnalyser import run, chunkify
    import pp
    import math
    job_server = pp.Server(restart=True)
    chunks = chunkify(people, math.floor(job_server.get_ncpus() / 2))
    jobs = []
    for chunk in chunks:
        from comparison import damerau_levenshtein_distance
        job = job_server.submit(run, (chunk, all_people, config), (damerau_levenshtein_distance,),
                                ("collections", "Person", "getData"))
        jobs.append(job)
    results = []
    for job in jobs:
        re = job()
        results.extend(re)
    job_server.print_stats()
    return results
