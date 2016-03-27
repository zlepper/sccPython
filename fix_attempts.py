def try_to_fix(invalid_chunk, males, females):
    k = []
    m = []
    for person in invalid_chunk:
        # Hvis personerne er invalide på grund af manglende køn
        if person.kon is None:
            male_count = males.get(person.navn, 0)
            famale_count = females.get(person.navn, 0)
            if male_count > 0 or famale_count > 0:
                if male_count > famale_count:
                    person.kon = True
                    m.append(person)
                else:
                    person.kon = False
                    k.append(person)
                invalid_chunk.remove(person)
            # mand = []
            # kvinde = []
            #
            # if person.navn != "":
            #
            #     for match in males:
            #         proximity = damerau_levenshtein_distance(person.navn, match.navn)
            #
            #         if proximity < 5:
            #             if match.valid:
            #                 mand.append(person)
            #
            #     for match in females:
            #         proximity = damerau_levenshtein_distance(person.navn, match.navn)
            #
            #         if proximity < 5:
            #             if match.valid:
            #                 kvinde.append(person)
            #
            #     if mand != [] or kvinde != []:
            #         if len(mand) < len(kvinde):
            #             person.kon = False
            #             k.append(person)
            #
            #             if person in invalid_chunk:
            #                 invalid_chunk.remove(person)
            #
            #         else:
            #             person.kon = True
            #             m.append(person)
            #
            #             if person in invalid_chunk:
            #                 invalid_chunk.remove(person)
    return invalid_chunk, m, k
