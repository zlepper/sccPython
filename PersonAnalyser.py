import Person


def run(people):
    assert isinstance(people, list)

    # Seperate people into different years
    dic = dict()
    for person in people:
        year_list = dic.get(person.year, [])
        year_list.append(person)
        dic[person.year] = year_list

    for this_year in dic:
        assert isinstance(this_year, int)
        this_year_list = dic[this_year]
        assert isinstance(this_year_list, list)
        print(this_year)

        # Iterate over all the person in this year
        for person in this_year_list:

            # Compare with all the other years
            for other_year in dic:

                # Skip if the year is the same
                if other_year == this_year:
                    continue

                other_year_list = dic[other_year]

                # Sorter civiltilstand
                possible_matches = []

                for other_person in other_year_list:
                    if other_year > this_year and other_person.civilstand >= person.civilstand:
                        possible_matches.append(other_person)
                    elif other_year < this_year and other_person.civilstand <= person.civilstand:
                        possible_matches.append(other_person)

                # Tag kun dem hvis alder er brugbar
                temp = []
                for possible_match in possible_matches:
                    if abs(person.fodeaar - possible_match.fodeaar) < 5:
                        temp.append(possible_match)

                possible_matches = temp

                for possible_match in possible_matches:
                    assert isinstance(possible_match, Person.Person)
                    prox = person.get_proximity(possible_match, people)
                    if prox < 3:
                        lis = person.matches.get(prox, [])
                        assert isinstance(lis, list)
                        lis.append(possible_match.id)
                        person.matches[prox] = lis
    return people

