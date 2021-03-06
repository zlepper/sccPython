import getData


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def run(people, all_people, config):
    import logging
    logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    assert isinstance(people, list)
    max_age_difference = config["max_age_difference"]
    max_proximity = config["max_proximity"]
    # Iterate the current chunk
    getData.generate_homes(all_people, people)
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
                            prox = person.get_proximity(possible_match, people, config)
                            if prox <= max_proximity:
                                lis = person.matches.get(prox, [])
                                lis.append(possible_match.id)
                                person.matches[prox] = lis
    return people


