def get_ditto_fodested(people, KIPnr, Ibnr):
    fodested = []

    for person in people:
        if person.KIPnr == KIPnr and person.lbnr - 1 == Ibnr - 1:
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


def get_all_names(people):
    all_names = []

    for person in people:
        if person.navn not in all_names:
            all_names.append(person.navn)

    return all_names


def get_home(people, kilde, sogn, herred, amt, stednavn, husstand, ibnr):
    home = []
    for person in people:
        if person.kilde == kilde and person.sogn == sogn and person.herred == herred and person.amt == amt and person.stednavn == stednavn and person.husstands_familienr == husstand:
            if person not in home:
                home.append(person)

    return home

def get_mand_home(home, ibnr):

    mand_ibnr = ibnr - 1

    for person in home:
        if person.lbnr == mand_ibnr:
            return person.navn
