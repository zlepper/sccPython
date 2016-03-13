import Person


def create_groups(people):
    people_source = list(people)
    remove_indices = []
    group = 1
    proximity = 0
    groups = dict()
    while len(people_source) > 0 and proximity < 15:
        for index, person in enumerate(people_source):
            assert isinstance(person, Person.Person)
            if proximity in person.matches:
                matches = person.matches[proximity]
                assert isinstance(matches, list)
                for match in matches:
                    assert isinstance(match, Person.Person)
                    # Check if the possible match already is in a group
                    if match.group != -1:
                        continue
                    # Check that the current matches doesn't already contain data from this year
                    if do_group_have_year(groups.get(person.group, []), match.year):
                        continue
                    # The match is available
                    if person.group == -1:
                        person.group = group
                        group += 1
                    match.group = person.group
                    magaritas = groups.get(person.group, [])
                    if match not in magaritas:
                        magaritas.append(match)
                    if person not in magaritas:
                        magaritas.append(person)
                    groups[person.group] = magaritas
                    if index not in remove_indices:
                        remove_indices.append(index)
        proximity += 1
        remove_indices.sort(reverse=True)
        for index in remove_indices:
            people_source.pop(index)
        remove_indices = []
    return people


def do_group_have_year(group, year):
    for member in group:
        assert isinstance(member, Person.Person)
        if member.year == year:
            return True
    return False
