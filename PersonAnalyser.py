from Person import Person
from jellyfish import jaro_distance
import pp


def run(people):
    assert isinstance(people, list)

    # Seperate people into different years
    dic = dict()
    for person in people:
        year_list = dic.get(person.year, [])
        year_list.append(person)

    for this_year, this_year_list in dic.items():
        assert isinstance(this_year, int)
        assert isinstance(this_year_list, list)

        # Iterate over all the person in this year
        for person in this_year_list:
            assert isinstance(person, Person)

            # Compare with all the other years
            for other_year, other_year_list in dic.items():

                # Skip if the year is the same
                if other_year == this_year:
                    continue

                # Sorter civiltilstand
                possible_matches = []

                for other_person in other_year_list:
                    assert isinstance(other_person, Person)
                    if other_year > this_year and other_person.civilstand >= person.civilstand:
                        possible_matches.append(other_person)
                    elif other_year < this_year and other_person.civilstand <= person.civilstand:
                        possible_matches.append(other_person)

                # Tag kun dem hvis alder er brugbar
                temp = []
                for possible_match in possible_matches:
                    assert isinstance(possible_match, Person)
                    if abs(person.fodeaar - possible_match.fodeaar) < 5:
                        temp.append(possible_match)

                possible_matches = temp

                # Sammenlign navne
                for possible_match in possible_matches:
                    assert isinstance(possible_match, Person)
                    proximity = jaro_distance(person.navn, possible_match.navn)
                    if proximity > 0.93:
                        person.matches.get(proximity, []).append(possible_match)
