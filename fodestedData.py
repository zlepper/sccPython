
def get_ditto_fodested(people, KIPnr, Ibnr):

    fodested = []

    for person in people:
        for person.KIPnr in person and person.ibnr in person:

            if person.KIPnr is KIPnr and person.ibnr - 1 is Ibnr - 1:
                fodested.append(person.KIPnr)
                fodested.append(person.ibnr - 1)

    return fodested

def get_all_sogn(people):

    all_sogn = []

    for person in people:
        for person.sogn in person:

            if person.sogn not in all_sogn:
                all_sogn.append(person.sogn)

    return all_sogn



