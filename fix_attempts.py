def try_to_fix(invalid_chunk, males, females):
    from comparison import damerau_levenshtein_distance
    import re
    k = []
    m = []
    for person in invalid_chunk:

        # Hvis personerne er invalide på grund af manglende alder
        if person.alder_tal is 0:
            if person.fodeaar is not 0 and person.kilde is not None:

                person.alder_tal = int((re.findall('\d+', person.kilde))[0]) - int(person.fodeaar)

                if person.alder_tal is not 0:

                    if person.kon is True:
                        m.append(person)

                        if person in invalid_chunk:
                            invalid_chunk.remove(person)

                    else:
                        k.append(person)

                        if person in invalid_chunk:
                            invalid_chunk.remove(person)

        # Hvis personerne er invalide på grund af manglende fødeår
        if person.fodeaar is 0:
            if person.alder_tal is not 0 and person.kilde is not None:

                person.fodeaar = int((re.findall('\d+', person.kilde))[0]) - int(person.alder_tal)

                if person.fodeaar is not 0:

                    if person.kon is True:
                        m.append(person)

                        if person in invalid_chunk:
                            invalid_chunk.remove(person)

                    else:
                        k.append(person)

                        if person in invalid_chunk:
                            invalid_chunk.remove(person)

        # Hvis personerne er invalide på grund af manglende køn
        if person.kon is None:
            mand = []
            kvinde = []

            if person.navn != "":

                for match in males:
                    proximity = damerau_levenshtein_distance(person.navn, match.navn)

                    if proximity < 5:
                        if match.valid:
                            mand.append(person)

                for match in females:
                    proximity = damerau_levenshtein_distance(person.navn, match.navn)

                    if proximity < 5:
                        if match.valid:
                            kvinde.append(person)

                if mand != [] or kvinde != []:
                    if len(mand) < len(kvinde):
                        person.kon = False
                        k.append(person)

                        if person in invalid_chunk:
                            invalid_chunk.remove(person)

                    else:
                        person.kon = True
                        m.append(person)

                        if person in invalid_chunk:
                            invalid_chunk.remove(person)
    return invalid_chunk, m, k
