from csv import CsvParser
import pp
from os import walk
from os.path import join
import PersonAnalyser
from time import time

people = []
jobs = []
job_server = pp.Server()


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
            parser = CsvParser(file)
            job = job_server.submit(get_people_from_file, (parser,))
            jobs.append(job)


# Fetch the current data
get_people_from_directory("/home/rasmus/Documents/gelsted/", job_server, jobs)

# Create lists of data
invalidPeople = []
males = []
females = []

# Wait for all the jobs to finish
for job in jobs:
    v = job()
    for person in v:
        if person.valid:
            if person.kon:
                males.append(person)
            else:
                females.append(person)
        else:
            invalidPeople.append(person)

job_server.print_stats()

# Tell us how many of each type of person we have
print("Invalid people count: %d" % (len(invalidPeople)))
print("Male people count: %d" % (len(males)))
print("Female people count: %d" % (len(females)))

t1 = time()
jobs = []
j = job_server.submit(PersonAnalyser.run, (males,))
jobs.append(j)
j = job_server.submit(PersonAnalyser.run, (females,))
jobs.append(j)

for job in jobs:
    job()
t2 = time()

job_server.print_stats()

print(t2 - t1)
