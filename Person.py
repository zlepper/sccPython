from comparison import damerau_levenshtein_distance
import getData


class Person:
    def __init__(self, year):
        assert isinstance(year, int)
        self.year = year
        self.KIPnr = str()
        self.kilde = str()
        self.sogn = str()
        self.herred = str()
        self.amt = str()
        self.lbnr = int()
        self.kildehenvisning = str()
        self.stednavn = str()
        self.husstands_familienr = int()
        self.matr_nr_adresse = None
        self.navn = str()
        self.kon = bool()
        self.alder_tal = int()
        self.fodeaar = int()
        self.civilstand = int()
        self.civilstand_source = str()
        self.fodested = str()
        self.valid = True
        self.matches = dict()
        self.erhverv = str()
        self.nregteskab = int()
        self.id = -1
        self.group = -1
        self.home_index = -1
        pass

    def __str__(self):
        return "Person(" + self.navn + ")"

    def __repr__(self):
        return self.__str__()

    def to_csv(self):
        s = ""
        s += str(self.id) + "|"
        s += str(self.group) + "|"
        s += str(self.year) + "|"
        s += str(self.KIPnr) + "|"
        s += str(self.kilde) + "|"
        s += str(self.sogn) + "|"
        s += str(self.herred) + "|"
        s += str(self.amt) + "|"
        s += str(self.lbnr) + "|"
        s += str(self.kildehenvisning) + "|"
        s += str(self.stednavn) + "|"
        s += str(self.husstands_familienr) + "|"
        s += str(self.matr_nr_adresse) + "|"
        s += str(self.navn) + "|"
        if self.kon:
            s += "M"
        else:
            s += "K"
        s += "|"
        s += str(self.alder_tal) + "|"
        s += str(self.fodeaar) + "|"
        s += str(self.fodested) + "|"
        s += str(self.civilstand_source) + "|"
        s += str(self.valid) + "\n"
        return s

    @staticmethod
    def topline():
        return "id|group|year|KIPnr|kilde|sogn|herred|amt|lbnr|kildehenvisning|stednavn|husstands_familienr|" \
               "matr_nr_adresse|navn|køn|alder_tal|fodeaar|fødested|civilstand|erhverv|valid\n"

    def get_closests(self):
        lowest = None
        closest = None
        for key, value in self.matches.items():
            if lowest is None:
                lowest = key
                closest = value
                continue
            if key < lowest:
                lowest = key
                closest = value
        if lowest is None:
            return None
        return closest, lowest

    def get_proximity(self, other, people, config):
        proximity = self.compare_name(other) * config["name_importance"]
        proximity += self.compare_origin(other, people) * config["origin_importance"]
        proximity += self.compare_where_they_live(other) * config["where_they_live_importance"]
        proximity += self.compare_family(other) * config["family_importance"]
        return proximity

    def compare_name(self, other):
        return damerau_levenshtein_distance(self.navn, other.navn)

    # Forudsætter, at navnet på personerne også er ens
    def compare_origin(self, other, people):
        proximity = 0

        herisognet = ["her i sognet", "heri sognet", "i sognet", "her sognet", "heri s", "her i s", "h. i sognet"]
        reference = ["do ", "do.", "ditto ", "dito ", "dto.", "dítto", "ds.", "das ", "item ", "it.", "ietm", "ibidem"]
        sogn = [" sogn", " s.", " s:", " s/", " s "]
        amt = [" amt"]

        if self.fodested != "" and other.fodested != "":
            personfodested = ""
            otherfodested = ""

            while personfodested == "":
                fodested = ""
                fodestedsogn = ""

                # Fødested her i sognet
                if any(element in self.fodested.lower() for element in herisognet):
                    personfodested = self.sogn.lower()
                    break

                # Fødested i et andet sogn
                elif any(element in self.fodested.lower() for element in sogn):

                        for term in sogn:
                            if term in self.fodested.lower():
                                fodested = self.fodested.lower().split(term)

                        if fodested != "":
                            personfodested = fodested[0]
                            break

                # Fødested indeholder et andet sogn og amt
                elif any(element in self.fodested.lower() for element in amt):

                    if "," in self.fodested.lower():
                        fodested = self.fodested.lower().split(",")

                    elif "." in self.fodested.lower():
                        fodested = self.fodested.lower().split(".")

                    else:
                        fodested = self.fodested.lower().split(" ")

                    if fodested is not []:
                        personfodested = fodested[0]
                        break

                # Fødested referet til forrige persons fødested i hjemmet
                elif any(element in self.fodested.lower() for element in reference):
                    fodested = getData.get_ditto_fodested(people, self.kilde, self.sogn, self.herred, self.amt,
                                                          self.stednavn, self.husstands_familienr, self.lbnr)

                    while any(element in fodested.lower() for element in reference):
                        fodested = getData.get_ditto_fodested(people, self.kilde, self.sogn, self.herred, self.amt,
                                                              self.stednavn, self.husstands_familienr, self.lbnr - 1)

                    if any(element in fodested.lower() for element in herisognet):
                        personfodested = self.sogn.lower()
                        break

                    elif any(element in fodested.lower() for element in sogn):

                        for term in sogn:
                            if term in fodested.lower():
                                fodestedsogn = fodested.lower().split(term)

                        if fodestedsogn != "":
                            personfodested = fodestedsogn[0]
                            break

                    elif any(element in self.fodested.lower() for element in amt):

                        if "," in self.fodested.lower():
                            fodested = self.fodested.lower().split(",")

                        elif "." in self.fodested.lower():
                            fodested = self.fodested.lower().split(".")

                        else:
                            fodested = self.fodested.lower().split(" ")

                        if fodested is not []:
                            personfodested = fodested[0]
                            break

                    else:
                        personfodested = self.fodested.lower()
                        break

                # Fødested er kun angivet til et navn på et sogn
                else:
                    personfodested = self.fodested.lower()
                    break

            while otherfodested == "":
                fodested = ""
                fodestedsogn = ""

                # Fødested her i sognet
                if any(element in other.fodested.lower() for element in herisognet):
                    otherfodested = other.sogn.lower()
                    break

                # Fødested i et andet sogn
                elif any(element in other.fodested.lower() for element in sogn):

                        for term in sogn:
                            if term in other.fodested.lower():
                                fodested = other.fodested.lower().split(term)

                        if fodested != "":
                            otherfodested = fodested[0]
                            break

                # Fødested indeholder et andet sogn og amt
                elif any(element in other.fodested.lower() for element in amt):

                    if "," in other.fodested.lower():
                        fodested = other.fodested.lower().split(",")

                    elif "." in other.fodested.lower():
                        fodested = other.fodested.lower().split(".")

                    else:
                        fodested = other.fodested.lower().split(" ")

                    if fodested is not []:
                        otherfodested = fodested[0]
                        break

                # Fødested referet til forrige persons fødested i hjemmet
                elif any(element in other.fodested.lower() for element in reference):
                    fodested = getData.get_ditto_fodested(people, other.kilde, other.sogn, other.herred, other.amt,
                                                          other.stednavn, other.husstands_familienr, other.lbnr)

                    while any(element in fodested.lower() for element in reference):
                        fodested = getData.get_ditto_fodested(people, other.kilde, other.sogn, other.herred, other.amt,
                                                              other.stednavn, other.husstands_familienr, other.lbnr - 1)

                    if any(element in fodested.lower() for element in herisognet):
                        otherfodested = other.sogn.lower()
                        break

                    elif any(element in fodested.lower() for element in sogn):

                        for term in sogn:
                            if term in fodested.lower():
                                fodestedsogn = fodested.lower().split(term)

                        if fodestedsogn != "":
                            otherfodested = fodestedsogn[0]
                            break

                    elif any(element in other.fodested.lower() for element in amt):

                        if "," in other.fodested.lower():
                            fodested = other.fodested.lower().split(",")

                        elif "." in other.fodested.lower():
                            fodested = other.fodested.lower().split(".")

                        else:
                            fodested = other.fodested.lower().split(" ")

                        if fodested is not []:
                            otherfodested = fodested[0]
                            break

                    else:
                        otherfodested = other.fodested.lower()
                        break

                # Fødested er kun angivet til et navn på et sogn
                else:
                    otherfodested = other.fodested.lower()
                    break

            if personfodested != "" and otherfodested != "":

                if personfodested == otherfodested:
                    proximity = 0

                else:
                    prox = damerau_levenshtein_distance(personfodested, otherfodested)

                    if prox <= 3:
                        proximity = prox

        return proximity

    def compare_family(self, other):

        # Sammenlign personerne efter deres mand eller kones navn - Forudsætter, at personernes navne er ens
        if self.civilstand == 2 and other.civilstand == 2:

            person_home = getData.get_home(self.home_index)
            other_home = getData.get_home(other.home_index)

            kone = ["kone", "konen", "hustru", "madmoder", "madmoeder", "huusmoder", "ehefrau", "frau"]

            if self.kon is True and other.kon is True:

                for person in person_home:

                    if any(element in person.erhverv.lower().split() for element in kone):
                        person_aegtefaelle = person.navn

                        for other in other_home:

                            if any(element in other.erhverv.lower().split() for element in kone):
                                other_aegtefaelle = other.navn

                                proximity = damerau_levenshtein_distance(person_aegtefaelle, other_aegtefaelle)

                                if proximity <= 3:
                                    return proximity  # Begge personer har en ægtefælle med samme navn

            if self.kon is False and other.kon is False:

                if any(element in self.erhverv.lower().split() for element in kone):
                    person_aegtefaelle = person_home[0].navn
                    print(str(person_home))

                    if person_aegtefaelle is not None:

                        if any(element in other.erhverv.lower().split() for element in kone):
                            other_aegtefaelle = other_home[0].navn
                            print(str(other_home))

                            if other_aegtefaelle is not None:

                                proximity = damerau_levenshtein_distance(person_aegtefaelle, other_aegtefaelle)

                                if proximity <= 3:
                                    return proximity  # Begge personer har en ægtefælle med samme navn
        return 0

    def compare_where_they_live(self, possible_match):
        if self.amt == possible_match.amt:
            return 4

        if self.herred == possible_match.herred:
            return 3

        if self.sogn == possible_match.sogn:
            return 2

        if self.stednavn != "" and possible_match.stednavn != "":
            proximity = damerau_levenshtein_distance(self.stednavn, possible_match.stednavn)
            if proximity <= 3:
                return 1
        return 0  # Begge personer bor præcis samme sted
