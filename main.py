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
import fix_attempts
from collections import defaultdict
import getData
import sys
import _io

args = []
# stdin = sys.stdin
# assert isinstance(stdin, _io.TextIOWrapper)
# for line in stdin:
#     line = line.rstrip()
#     print(line)
#     if line != "\n":
#         args.append(line)
# print("Args are: ")
# print(args)

if len(args) == 0:
    args.append("*")
print("AFter")
assert isinstance(args, list)
logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
config = get_config()
t56 = time()

people = []
jobs = []
ppservers = tuple(args)
job_server = pp.Server(restart=True, ppservers=ppservers)
logging.info("Number of pp processes created: " + str(job_server.get_ncpus()))


def get_people_from_file(parser):
    return parser.get_people()


def get_people_from_directory(dir, job_server, jobs):
    for (dirpath, dirnames, filenames) in walk(dir):
        for dirname in dirnames:
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
    for person in p:
        for k in person.matches:
            m = person.matches[k]
            ml = []
            for i in m:
                try:
                    pers = p[i]
                    if pers:
                        ml.append(pers)
                except IndexError:
                    pass
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
while len(jobs) > 0:
    done_jobs = [job for job in jobs if job.finished]
    jobs = [job for job in jobs if not job.finished]
    for job in done_jobs:
        logging.info("Waiting for next job to finish")
        v = job()
        logging.info("Done with job " + str(x))
        x += 1
        for person in v:
            person.id = id
            if person.valid:
                if person.kon:
                    # logging.debug("Appending to males")
                    males.append(person)
                    # logging.debug("Appended to males")
                else:
                    # logging.debug("Appending to females")
                    females.append(person)
                    # logging.debug("Appended to females")
            else:
                # logging.debug("Appending to invalidpeople")
                invalidPeople.append(person)
                # logging.debug("Appended to invalid people")
            id += 1

logging.info("Invalid fix start")
female_names = defaultdict(int)
for name in [person.navn.split()[0] for person in females if not person.navn.isspace]:
    female_names[name] += 1

male_names = defaultdict(int)
for name in [person.navn.split()[0] for person in males if not person.navn.isspace]:
    male_names[name] += 1

# Gør invalide personer valide - Hvis en anden person med samme navn har et køn, så brug den persons køn
if len(invalidPeople) > 0:
    logging.info("Trying to fix invalid people data")
    chunks = PersonAnalyser.chunkify(invalidPeople, job_server.get_ncpus())
    jobs = []
    for chunk in chunks:
        job = job_server.submit(fix_attempts.try_to_fix, (chunk, male_names, female_names))
        jobs.append(job)
    invalidPeople = []
    for job in jobs:
        result = job()
        invalidPeople.extend(result[0])
        males.extend(result[1])
        females.extend(result[2])
    logging.info("Done fixing invalid people data")
    job_server.print_stats()

male_names = []
female_names = []

# Tell us how many of each type of person we have
logging.info("Invalid people count: %d" % (len(invalidPeople)))
logging.info("Male people count: %d" % (len(males)))
logging.info("Female people count: %d" % (len(females)))

people.extend(males)
people.extend(females)

people = sorted(people, key=lambda person: person.id)

t1 = time()


homes = getData.generate_homes(people)

logging.info("MAIN: Waiting for jobs to execute")
people = main_analyser.analyse(people, homes, config, job_server)
logging.info("MAIN: People list was extended with information")


logging.info("MAIN: Sorting people according to ID")
people.extend(invalidPeople)
people = sorted(people, key=lambda person: person.id)
logging.info("MAIN: Done sorting people according to ID")

logging.info("MAIN: Rebuilding matches")
people = rebuild_matches(people)
logging.info("MAIN: Done rebuilding matches")

# Create groups
logging.info("MAIN: Creating groups")
people = create_groups(people, config)
logging.info("MAIN: Done creating groups")

job_server.print_stats()

logging.info("Writing output")
Outputter.output(people, "smallscc.out.csv")
t2 = time()

logging.info("Counting unuseable data")
number_of_not_found = 0
for person in people:
    if person.group == -1:
        number_of_not_found += 1
logging.info("Number of people that could not be matched: " + str(number_of_not_found))

logging.info("Tid for kørsel i alt: " + str(t2 - t1))
print("Tid for kørsel i alt: " + str(t2 - t1))
