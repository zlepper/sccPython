from csv import CsvParser
import pp
from os import walk
from os.path import join
import PersonAnalyser
from time import time
from output import Outputter
from comparison import damerau_levenshtein_distance
import collections
import Person


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
            print(file)
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


# TODO Modify this to point to the local files on your machine
# Fetch the current data
get_people_from_directory(".\\toy", job_server, jobs)

# Create lists of data
invalidPeople = []
males = []
females = []

# Wait for all the jobs to finish
x = 1
for job in jobs:
    v = job()
    print("Done with job " + str(x))
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

# job_server.print_stats()

# Tell us how many of each type of person we have
print("Invalid people count: %d" % (len(invalidPeople)))
print("Male people count: %d" % (len(males)))
print("Female people count: %d" % (len(females)))

id = 1

people.extend(males)
people.extend(females)
for p in people:
    p.id = id
    id += 1


t1 = time()
jobs = []
j = job_server.submit(PersonAnalyser.run, (males,), (damerau_levenshtein_distance,), ("collections", "Person"))
jobs.append(j)
j = job_server.submit(PersonAnalyser.run, (females,), (damerau_levenshtein_distance,), ("collections", "Person"))
jobs.append(j)

people = []

for job in jobs:
    pe = job()
    # print(len(pe))
    people.extend(pe)

people = rebuild_matches(people)

t2 = time()

#job_server.print_stats()

#print(t2 - t1)

t1 = time()
Outputter.output(people, "smallscc.out.csv")
t2 = time()

#print(t2 - t1)