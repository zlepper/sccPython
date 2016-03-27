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
    return invalid_chunk, m, k
