def get_ditto_fodested(people, KIPnr, Ibnr):
    fodested = []

    for person in people:
        for person.KIPnr in person and person.ibnr in person:

            if person.KIPnr is KIPnr and person.ibnr - 1 is Ibnr - 1:
                fodested.append(person.husstands_familienr)
                fodested.append(person.fodested)

    return fodested


def get_all_sogn(people):
    all_sogn = []

    for person in people:
        for person.sogn in person:

            if person.sogn not in all_sogn:
                all_sogn.append(person.sogn)

    return all_sogn


def get_home(people, kilde, sogn, herred, amt, stednavn, husstand):
    home = []

    for person in people:
        if person.kilde is kilde and person.sogn is sogn and person.herred is herred and person.amt is amt and person.stednavn is stednavn and person.husstands_familienr is husstand:
            home.append(person)

    return home
