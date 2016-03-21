import Person
import math


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def run(people, all_people, config):
    import logging
    logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    assert isinstance(people, list)
    max_age_difference = config["max_age_difference"]
    max_proximity = config["max_proximity"]
    # Seperate people into different years
    # dic = dict()
    # for person in people:
    #     year_list = dic.get(person.year, [])
    #     year_list.append(person)
    #     dic[person.year] = year_list
    #
    # for this_year in dic:
    #     assert isinstance(this_year, int)
    #     this_year_list = dic[this_year]
    #     assert isinstance(this_year_list, list)
    #     print(this_year)
    #
    #     # Iterate over all the person in this year
    #     for person in this_year_list:
    #
    #         # Compare with all the other years
    #         for other_year in dic:
    #
    #             # Skip if the year is the same
    #             if other_year == this_year:
    #                 continue
    #
    #             other_year_list = dic[other_year]
    #
    #             # Sorter civiltilstand
    #             possible_matches = []
    #
    #             for other_person in other_year_list:
    #                 if other_year > this_year and other_person.civilstand >= person.civilstand:
    #                     possible_matches.append(other_person)
    #                 elif other_year < this_year and other_person.civilstand <= person.civilstand:
    #                     possible_matches.append(other_person)
    #
    #             # Tag kun dem hvis alder er brugbar
    #             temp = []
    #             for possible_match in possible_matches:
    #                 if abs(person.fodeaar - possible_match.fodeaar) < max_age_difference:
    #                     temp.append(possible_match)
    #
    #             possible_matches = temp
    #
    #             for possible_match in possible_matches:
    #                 assert isinstance(possible_match, Person.Person)
    #                 prox = person.get_proximity(possible_match, people, all_people)
    #                 if prox < max_proximity:
    #                     lis = person.matches.get(prox, [])
    #                     assert isinstance(lis, list)
    #                     lis.append(possible_match.id)
    #                     person.matches[prox] = lis
    # Iterate the current chunk
    n = 1
    for person in people:
        if n % 10 == 0:
            logging.debug("Person number " + str(n))
        n += 1
        # assert isinstance(person, Person.Person)
        # Compare with all other datapoints
        for possible_match in all_people:
            # assert isinstance(possible_match, Person.Person)
            # Make sure both data points are of the same gender
            if person.kon == possible_match.kon:
                # Make sure the datapoints isn't from the same year
                if person.year != possible_match.year:
                    # Make sure the data points are within the max age difference of each other
                    if abs(person.fodeaar - possible_match.fodeaar) < max_age_difference:
                        # Make sure civilstand is only moving on, not moving backwards
                        if (person.year > possible_match.year and person.civilstand >= possible_match.civilstand) or (
                                person.year < possible_match.year and person.civilstand <= possible_match.civilstand):
                            prox = person.get_proximity(possible_match, people)
                            if prox <= max_proximity:
                                lis = person.matches.get(prox, [])
                                lis.append(possible_match.id)
                                person.matches[prox] = lis
    return people


