from PersonAnalyser import run, chunkify
import pp
import logging
import Person
import globals_scc
import math


def rewire(updated):
    for person in updated:
        original_person = globals_scc.people_as_dict[person.id]
        assert isinstance(original_person, Person.Person)
        for proximity, matches in person.matches.items():
            original_matches = original_person.matches.get(proximity, [])
            original_matches.extend(matches)
            original_person.matches[proximity] = list(set(original_matches))


def analyse(people, homes, config):
    globals_scc.people_as_dict = {person.id: person for person in people}
    logging.basicConfig(filename='log.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("Analyse started")
    job_server = pp.Server(restart=True)
    max_job_count = job_server.get_ncpus() - 1
    multiplier = math.ceil(len(people) / 1000)
    print("Job multiplier is " + str(multiplier))
    chunks = chunkify(people, max_job_count * multiplier)
    logging.info("Number of chunks: " + str(len(chunks)))
    jobs = []
    from comparison import damerau_levenshtein_distance
    for chunk in chunks:
        for chunk2 in chunks:
            job = job_server.submit(run, (chunk, chunk2, homes, config), (damerau_levenshtein_distance,),
                                    ("collections", "Person", "getData", "globals_scc"))
            assert isinstance(job, pp._Task)
            jobs.append(job)
            while len(jobs) >= max_job_count:
                done_jobs = [job for job in jobs if job.finished]
                jobs = [job for job in jobs if not job.finished]
                if len(done_jobs) > 0:
                    print("Done jobs: " + str(len(done_jobs)))
                for job in done_jobs:
                    rewire(job())


    logging.info("Jobs started")
    # Handle the rest of the jobs
    for job in jobs:
        re = job()
        rewire(re)
    logging.info("Jobs done")
    job_server.print_stats()
    return people
