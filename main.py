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
import re
from comparison import damerau_levenshtein_distance

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
config = get_config()
t56 = time()

people = []
jobs = []
job_server = pp.Server(restart=True)


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
for job in jobs:
    v = job()
    logging.info("Done with job " + str(x))
    x += 1
    assert isinstance(v, list)
    for person in v:
        if person.valid:
            if person.kon:
                males.append(person)
            else:
                females.append(person)
        else:
            invalidPeople.append(person)

<<<<<<< HEAD
    # Gør invalide personer valide - Hvis en anden person med samme navn har et køn, så brug den persons køn
    if len(invalidPeople) > 0:
        for person in invalidPeople:

            # Hvis personerne er invalide på grund af manglende alder
            if person.alder_tal is 0:
                if person.fodeaar is not 0 and person.kilde is not None:

                    person.alder_tal = int((re.findall('\d+', person.kilde))[0]) - int(person.fodeaar)

                    if person.alder_tal is not 0:

                        if person.kon is True:
                            males.append(person)

                            if person in invalidPeople:
                                invalidPeople.remove(person)

                        else:
                            females.append(person)

                            if person in invalidPeople:
                                invalidPeople.remove(person)

            # Hvis personerne er invalide på grund af manglende fødeår
            if person.fodeaar is 0:
                if person.alder_tal is not 0 and person.kilde is not None:

                    person.fodeaar = int((re.findall('\d+', person.kilde))[0]) - int(person.alder_tal)

                    if person.fodeaar is not 0:

                        if person.kon is True:
                            males.append(person)

                            if person in invalidPeople:
                                invalidPeople.remove(person)

                        else:
                            females.append(person)

                            if person in invalidPeople:
                                invalidPeople.remove(person)

            # Hvis personerne er invalide på grund af manglende køn
            if person.kon is None:
                mand = []
                kvinde = []

                if person.navn != "":

                    for match in males:
                        proximity = damerau_levenshtein_distance(person.navn, match.navn)

                        if proximity < 5:
                            if match.valid:
                                mand.append(person)

                    for match in females:
                        proximity = damerau_levenshtein_distance(person.navn, match.navn)

                        if proximity < 5:
                            if match.valid:
                                kvinde.append(person)

                    if mand != [] or kvinde != []:
                        if len(mand) < len(kvinde):
                            person.kon = False
                            females.append(person)

                            if person in invalidPeople:
                                invalidPeople.remove(person)

                        else:
                            person.kon = True
                            males.append(person)

                            if person in invalidPeople:
                                invalidPeople.remove(person)
=======
# # Gør invalide personer valide - Hvis en anden person med samme navn har et køn, så brug den persons køn
# if len(invalidPeople) > 0:
#     for person in invalidPeople:
#
#         # Hvis personerne er invalide på grund af manglende alder
#         if person.alder_tal is 0:
#             if person.fodeaar is not 0 and person.kilde is not None:
#
#                 person.alder_tal = int((re.findall('\d+', person.kilde))[0]) - int(person.fodeaar)
#
#                 if person.alder_tal is not 0:
#
#                     if person.kon is True:
#                         males.append(person)
#                         invalidPeople.remove(person)
#
#                     else:
#                         females.append(person)
#                         invalidPeople.remove(person)
#
#         # Hvis personerne er invalide på grund af manglende fødeår
#         if person.fodeaar is 0:
#             if person.alder_tal is not 0 and person.kilde is not None:
#
#                 person.fodeaar = int((re.findall('\d+', person.kilde))[0]) - int(person.alder_tal)
#
#                 if person.fodeaar is not 0:
#
#                     if person.kon is True:
#                         males.append(person)
#                         invalidPeople.remove(person)
#
#                     else:
#                         females.append(person)
#                         invalidPeople.remove(person)
#
#         # Hvis personerne er invalide på grund af manglende køn
#         if person.kon is None:
#             mand = []
#             kvinde = []
#
#             if person.navn != "":
#
#                 for match in males:
#                     proximity = damerau_levenshtein_distance(person.navn, match.navn)
#
#                     if proximity < 5:
#                         if match.valid:
#                             mand.append(person)
#
#                 for match in females:
#                     proximity = damerau_levenshtein_distance(person.navn, match.navn)
#
#                     if proximity < 5:
#                         if match.valid:
#                             kvinde.append(person)
#
#                 if mand != [] or kvinde != []:
#                     if len(mand) < len(kvinde):
#                         person.kon = False
#                         females.append(person)
#                         invalidPeople.remove(person)
#
#                     else:
#                         person.kon = True
#                         males.append(person)
#                         invalidPeople.remove(person)
>>>>>>> refs/remotes/origin/cache


# job_server.print_stats()

# Tell us how many of each type of person we have
logging.info("Invalid people count: %d" % (len(invalidPeople)))
logging.info("Male people count: %d" % (len(males)))
logging.info("Female people count: %d" % (len(females)))

id = 1

people.extend(males)
people.extend(females)
for p in people:
    p.id = id
    id += 1

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

t2 = time()

# Create groups
people = create_groups(people, config)

job_server.print_stats()

logging.info(t2 - t1)
print("Tid for kørsel i alt: " + str(t2 - t1))

t1 = time()
Outputter.output(people, "smallscc.out.csv")
t2 = time()

logging.info(t2 - t56)
