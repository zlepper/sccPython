from comparison import damerau_levenshtein_distance
import getData
import re


class Person:
    def __init__(self, year):
        self.year = year
        self.KIPnr = str()
        self.kilde = str()
        self.sogn = str()
        self.herred = str()
        self.amt = str()
        self.lbnr = int()
        self.stednavn = str()
        self.husstands_familienr = int()
        self.navn = str()
        self.kon = bool()
        self.alder_tal = int()
        self.fodeaar = int()
        self.civilstand = int()
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
        s += str(self.group) + "|"
        s += str(self.year) + "|"
        s += str(self.KIPnr) + "|"
        s += str(self.lbnr) + "|"
        s += str(self.amt) + "|"
        s += str(self.navn) + "|"
        s += str(self.fodeaar) + "\n"
        return s

    @staticmethod
    def topline():
        return "linkID|kilde|KIPnr|lbnr|amt|navn|fodeaar\n"

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

    def to_small_copy(self):
        return str(self.kon) + "|" + str(self.civilstand) + "|" + str(self.nregteskab) + "|" + self.erhverv

    def get_proximity(self, other, config):
        proximity = self.compare_name_fornavn(other) * config["name_fornavn_importance"]
        proximity += self.compare_name_efternavn(other) * config["name_efternavn_importance"]
        proximity += self.compare_origin(other) * config["origin_importance"]
        proximity += self.compare_where_they_live(other) * config["where_they_live_importance"]
        proximity += self.compare_aegteskab(other) * config["aegteskab_importance"]
        proximity += self.compare_barn_foraeldre(other) * config["barn_foraeldre_importance"]
        return proximity

    def compare_name_fornavn(self, other):
        return damerau_levenshtein_distance(re.sub("[,.:?\[\]\(\)\{\}]", "", self.navn.lower()).split(" ")[0], re.sub("[,.:?\[\]\(\)\{\}]", "", other.navn.lower()).split(" ")[0])

    def compare_name_efternavn(self, other):
        if self.kon is True:
            return damerau_levenshtein_distance(re.sub("[,.:?\[\]\(\)\{\}]", "", self.navn.lower()).split(" ")[-1], re.sub("[,.:?\[\]\(\)\{\}]", "", other.navn.lower()).split(" ")[-1])

        else:
            if self.civilstand == 2 and other.civilstand == 2:
                return damerau_levenshtein_distance(re.sub("[,.:?\[\]\(\)\{\}]", "", self.navn.lower()).split(" ")[-1], re.sub("[,.:?\[\]\(\)\{\}]", "", other.navn.lower()).split(" ")[-1])

            elif self.civilstand >= 2 or other.civilstand >= 2:
                return 0

            elif self.civilstand <= 1 and other.civilstand <= 1:
                return damerau_levenshtein_distance(re.sub("[,.:?\[\]\(\)\{\}]", "", self.navn.lower()).split(" ")[-1], re.sub("[,.:?\[\]\(\)\{\}]", "", other.navn.lower()).split(" ")[-1])


    def compare_origin(self, other):

        if self.fodested != "" and self.fodested is not None and other.fodested != "" and other.fodested is not None:
            return damerau_levenshtein_distance(self.fodested, other.fodested)

        return 0

    def compare_aegteskab(self, other):

        # Ret fejl ved indtastning - hvis de er gift, så må deres nr. ægteskab mindst være 1
        if self.civilstand == 2 and self.nregteskab == 0 or self.nregteskab == "":
            self.nregteskab = 1

        if other.civilstand == 2 and other.nregteskab == 0 or other.nregteskab == "":
            other.nregteskab = 1

        # Sammenlign personerne efter deres mand eller kones navn - Forudsætter, at personernes navne er ens
        if self.civilstand == 2 and other.civilstand == 2 and self.nregteskab == other.nregteskab:

            person_home = getData.get_home(self.home_index)
            other_home = getData.get_home(other.home_index)

            kone = ["kone", "konen", "koun", "koune", "koene", "hustru", "madmoder", "madmoeder", "huusmoder", "husmoder", "moder", "ehefrau", "frau"]
            if person_home is not [] and other_home is not []:
                if self.kon is True and other.kon is True:

                        for person in person_home:
                            if any(element in re.sub("[,.\-?:\[\]\(\)\{\}]", "", person.erhverv.lower()).split(" ") for element in kone):
                                if person.civilstand == self.civilstand and person.nregteskab == self.nregteskab:
                                    person_aegtefaelle = person.navn

                                    if person_aegtefaelle is not None:

                                        for andenperson in other_home:

                                            if any(element in re.sub("[,.\-?:\[\]\(\)\{\}]", "", andenperson.erhverv.lower()).split(" ") for element in kone):

                                                if andenperson.civilstand == other.civilstand and andenperson.nregteskab == other.nregteskab:
                                                    other_aegtefaelle = andenperson.navn

                                                    if other_aegtefaelle is not None:

                                                        proximity = damerau_levenshtein_distance(person_aegtefaelle, other_aegtefaelle)

                                                        if proximity is not None:
                                                            return proximity

                if self.kon is False and other.kon is False:

                    if any(element in re.sub("[,.\-?:\[\]\(\)\{\}]", "", self.erhverv.lower()).split(" ") for element in kone):

                            if self in person_home and person_home[person_home.index(self) - 1].kon is True and person_home[person_home.index(self) - 1].civilstand == self.civilstand and person_home[person_home.index(self) - 1].nregteskab == self.nregteskab:
                                person_aegtefaelle = person_home[person_home.index(self) - 1].navn

                                if person_aegtefaelle is not None:

                                    if any(element in re.sub("[,.\-?:\[\]\(\)\{\}]", "", other.erhverv.lower()).split(" ") for element in kone):

                                        if other in other_home and other_home[other_home.index(other) - 1].kon is True and other_home[other_home.index(other) - 1].civilstand == other.civilstand and other_home[other_home.index(other) - 1].nregteskab == other.nregteskab:
                                            other_aegtefaelle = other_home[other_home.index(other) - 1].navn

                                            if other_aegtefaelle is not None:
                                                proximity = damerau_levenshtein_distance(person_aegtefaelle, other_aegtefaelle)

                                                if proximity is not None:
                                                    return proximity

        return 0

    def compare_barn_foraeldre(self, other):
        barn = ["søn", "datter", "dater", "barn", "barn.", "børn", "kinder", "sohn", "tochter", "deres søn", "deres datter", "deres døttre", "deres barn", "deres børn", "deres ægte søn", "deres ægte datter", "deres fælles søn", "deres fælles datter", "deres fælles børn", "deres fælles barn", "en søn", "en datter", "ægte søn", "ægte datter", "ihre kinder", "ihre sohn", "ihre tochter", "ihr kinder", "ihr sohn", "ihr tochter"]
        kone = ["kone", "konen", "koun", "koune", "koene", "hustru", "hustrue", "madmoder", "madmoeder", "huusmoder", "husmoder", "moder", "ehefrau", "frau"]

        if any(element in re.sub("[,.\-?:\[\]\(\)\{\}]", "", self.erhverv.lower()) for element in barn) and any(element in re.sub("[,.\-?:\[\]\(\)\{\}]", "", other.erhverv.lower()) for element in barn):
            person_home = getData.get_home(self.home_index)
            other_home = getData.get_home(other.home_index)

            for person in person_home:

                if any(element in re.sub("[,.\-?:\[\]\(\)\{\}]", "", person.erhverv.lower()).split(" ") for element in kone):

                    if person.kon is False and person.civilstand == 2:
                        person_moder = person.navn

                        if person in person_home and person_home[person_home.index(person) - 1].kon is True and person_home[person_home.index(person) - 1].civilstand == 2 and person_home[person_home.index(person) - 1].nregteskab == person.nregteskab:
                            person_fader = person_home[person_home.index(person) - 1].navn

                            for other in other_home:

                                if any(element in re.sub("[,.\-?:\[\]\(\)\{\}]", "", other.erhverv.lower()).split(" ") for element in kone):

                                    if other.kon is False and other.civilstand == 2:
                                        other_moder = other.navn

                                        if other in other_home and other_home[other_home.index(other) - 1].kon is True and other_home[other_home.index(other) - 1].civilstand == 2 and other_home[other_home.index(other) - 1].nregteskab == other.nregteskab:
                                            other_fader = other_home[other_home.index(other) - 1].navn

                                            if person_fader != "" and person_fader is not None and person_moder != "" and person_moder is not None and other_fader != "" and other_fader is not None and other_moder != "" and other_moder is not None:
                                                proximity = int(damerau_levenshtein_distance(person_fader, other_fader)) + int(damerau_levenshtein_distance(person_moder, other_moder))

                                                if proximity is not None:
                                                    return proximity

        return 0

    def compare_where_they_live(self, possible_match):
        if self.amt != possible_match.amt:
            return 4

        if self.herred != possible_match.herred:
            return 3

        if self.sogn != possible_match.sogn:
            return 2

        if self.stednavn != "" and possible_match.stednavn != "":
            return damerau_levenshtein_distance(self.stednavn, possible_match.stednavn)

        return 0
