import globals_scc


def get_ditto_fodested(people, kilde, sogn, herred, amt, stednavn, husstandsfamilienr, lbnr):
    for person in people:
        if person.kilde == kilde and person.sogn == sogn and person.herred == herred and person.amt == amt and person.stednavn == stednavn and person.husstands_familienr == husstandsfamilienr and person.lbnr == lbnr:
            return person.fodested

    return ""


def generate_homes(people, analysed):
    home = []
    this_family = []
    last_husstands_familienr = -1
    for person in people:
        if person.husstands_familienr == last_husstands_familienr:
            person.home_index = len(home)
            this_family.append(person)
        else:
            last_husstands_familienr = person.husstands_familienr
            home.append(this_family)
            this_family = [person]
            person.home_index = len(home)

    for an in analysed:
        for person in people:
            if an.id == person.id:
                an.home_index = person.home_index
                break

    import globals_scc
    globals_scc.home = home
    print(len(home))


def get_home(index):
    return globals_scc.home[index]
