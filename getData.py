import Person
import globals_scc


def get_ditto_fodested(people, kilde, sogn, herred, amt, stednavn, husstandsfamilienr, lbnr):
    for person in people:
        if person.kilde == kilde and person.sogn == sogn and person.herred == herred and person.amt == amt and person.stednavn == stednavn and person.husstands_familienr == husstandsfamilienr and person.lbnr == lbnr:
            return person.fodested

    return ""


def person_from_small_copy(person):
    import re
    import ast
    match = re.match("(.*?)\\|(.*?)\\|(.*?)\\|(.*)", person)
    groups = match.groups()
    p = Person.Person(0)
    p.kon = ast.literal_eval(groups[0])
    p.civilstand = int(groups[1])
    if groups[2]:
        p.nregteskab = int(groups[2])
    else:
        p.nregteskab = 0
    p.erhverv = groups[3]
    return p


def generate_homes(people):
    home = []
    this_family = []
    last_husstands_familienr = -1
    for person in people:
        if person.husstands_familienr == last_husstands_familienr:
            person.home_index = len(home)
            this_family.append(person.to_small_copy())
        else:
            last_husstands_familienr = person.husstands_familienr
            home.append(this_family)
            this_family = [person.to_small_copy()]
            person.home_index = len(home)
    return home


def get_home(index):
    try:
        return [person_from_small_copy(p) for p in globals_scc.home[index]]
    except IndexError:
        # import logging
        # logging.debug("IndexError when trying to fetch home")
        return []
