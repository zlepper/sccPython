from os import walk
from os.path import join
from time import time

import pp

import Person
import main_analyser
from config import get_config
from csv import CsvParser
from group import create_groups
from output import Outputter
import logging
import PersonAnalyser
import re
from comparison import damerau_levenshtein_distance
import fix_attempts

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
config = get_config()
t56 = time()

people = []
jobs = []
job_server = pp.Server(restart=True)
logging.info("Number of pp processes created: " + str(job_server.get_ncpus()))

def get_people_from_file(parser):
    # assert isinstance(parser, CsvParser)
    return parser.get_people()


def get_people_from_directory(dir, job_server, jobs):
    for (dirpath, dirnames, filenames) in walk(dir):
        # assert isinstance(dirnames, list)
        # assert isinstance(filenames, list)
        # assert isinstance(dirpath, str)
        for dirname in dirnames:
            # assert isinstance(dirname, str)
            d = join(dirpath, dirname)
            job = job_server.submit(get_people_from_directory, (d, job_server, jobs))
            jobs.append(job)

        for filename in filenames:
            file = join(dirpath, filename)
            logging.info(file)
            parser = CsvParser(file)
            job = job_server.submit(get_people_from_file, (parser,))
            jobs.append(job)


def rebuild_matches(p):
    assert isinstance(p, list)
    for person in p:
        assert isinstance(person, Person.Person)
        for k in person.matches:
            m = person.matches[k]
            ml = []
            assert isinstance(m, list)
            for i in m:
                pers = None
                for per in p:
                    assert isinstance(per, Person.Person)
                    if i == per.id:
                        pers = per
                if pers is not None:
                    ml.append(pers)
            person.matches[k] = ml
    return p


# Fetch the current data
get_people_from_directory(join(".", "toy"), job_server, jobs)

# Create lists of data
invalidPeople = []
males = []
females = []

# Wait for all the jobs to finish
x = 1
id = 0
for job in jobs:
    v = job()
    logging.info("Done with job " + str(x))
    x += 1
    assert isinstance(v, list)
    for person in v:
        person.id = id
        if person.valid:
            if person.kon:
                males.append(person)
            else:
                females.append(person)
        else:
            invalidPeople.append(person)
        id += 1


# Gør invalide personer valide - Hvis en anden person med samme navn har et køn, så brug den persons køn
if len(invalidPeople) > 0:
    logging.info("Trying to fix invalid people data")
    chunks = PersonAnalyser.chunkify(invalidPeople, job_server.get_ncpus())
    jobs = []
    for chunk in chunks:
        job = job_server.submit(fix_attempts.try_to_fix, (chunk, males, females))
        jobs.append(job)
    invalidPeople = []
    for job in jobs:
        result = job()
        invalidPeople.extend(result[0])
        males.extend(result[1])
        females.extend(result[2])
    logging.info("Done fixing invalid people data")
    job_server.print_stats()

# Tell us how many of each type of person we have
logging.info("Invalid people count: %d" % (len(invalidPeople)))
logging.info("Male people count: %d" % (len(males)))
logging.info("Female people count: %d" % (len(females)))

id = 1

people.extend(males)
people.extend(females)

people = sorted(people, key=lambda person: person.id)

t1 = time()

jobs = []
j = job_server.submit(main_analyser.analyse, (males, people, config))
jobs.append(j)
j = job_server.submit(main_analyser.analyse, (females, people, config))
jobs.append(j)

people = []

for job in jobs:
    pe = job()
    people.extend(pe)

people = rebuild_matches(people)

# Create groups
people = create_groups(people, config)

job_server.print_stats()


Outputter.output(people, "smallscc.out.csv")
t2 = time()

number_of_not_found = 0
for person in people:
    assert isinstance(person, Person.Person)
    if person.group == -1:
        number_of_not_found += 1
logging.info("Number of people that could not be matches: " + str(number_of_not_found))

logging.info("Tid for kørsel i alt: " + str(t2 - t1))
print("Tid for kørsel i alt: " + str(t2 - t1))
