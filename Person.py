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
            if lowest == None:
                lowest = key
                closest = value
                continue
            if key < lowest:
                lowest = key
                closest = value
        if lowest is None:
            return None
        return closest, lowest

    def get_proximity(self, other, people):
        proximity = self.compare_name(other)
        proximity += self.compare_origin(other, people)
        proximity += self.compare_where_they_live(other)
        proximity += self.compare_family(other, people)
        return proximity

    def compare_name(self, other):
        return damerau_levenshtein_distance(self.navn, other.navn)

    # Forudsætter, at navnet på personerne også er ens
    def compare_origin(self, other, people):

        if self.fodested != "" and other.fodested != "":
            proximity = 0
            if "her i sognet" in self.fodested.lower() and "her i sognet" in other.fodested.lower():
                proximity = damerau_levenshtein_distance(self.sogn, other.sogn)

            else:
                if "her i sognet" in self.fodested.lower() and "do" in other.fodested.lower() or "ditto" in other.fodested.lower():
                    fodested = getData.get_ditto_fodested(people, other.KIPnr, other.lbnr)  # Tilføj liste af personer

                    while other.husstands_familienr == fodested[0]:
                        fodested = getData.get_ditto_fodested(people, other.KIPnr, other.lbnr - 1)  # Tilføj liste af personer

                    if "her i sognet" in fodested[1].lower():
                        proximity = damerau_levenshtein_distance(self.sogn, other.sogn)

                if "her i sognet" in other.fodested.lower() and "do" in self.fodested.lower() or "ditto" in self.fodested.lower():
                    fodested = getData.get_ditto_fodested(people, self.KIPnr, self.lbnr)  # Tilføj liste af personer

                    while self.husstands_familienr == fodested[0]:
                        fodested = getData.get_ditto_fodested(people, self.KIPnr, self.lbnr - 1)  # Tilføj liste af personer

                    if "her i sognet" in fodested[1].lower():
                        proximity = damerau_levenshtein_distance(self.sogn, other.sogn)

                '''
                if "her i sognet" not in self.fodested.lower() and "her i sognet" not in other.fodested.lower():
                    proximity = damerau_levenshtein_distance(self.fodested, other.fodested)
                '''

            return proximity  # Begge personer er født i samme sogn

        else:
            return 0

    def compare_family(self, other, people):

        # Sammenlign personerne efter deres mand eller kones navn - Forudsætter, at personernes navne er ens
        if self.civilstand == 2 and other.civilstand == 2:

            person_home = getData.get_home(people, self.kilde, self.sogn, self.herred, self.amt, self.stednavn, self.husstands_familienr, self.lbnr)  # Tilføj liste af personer
            other_home = getData.get_home(people, other.kilde, other.sogn, other.herred, other.amt, other.stednavn, other.husstands_familienr, other.lbnr)  # Tilføj liste af personer

            kone = ["kone", "konen", "hustru", "madmoder", "madmoeder", "huusmoder", "ehefrau", "frau"]

            if self.kon is True and other.kon is True:

                for person in person_home:

                        if any(element in person.erhverv.lower().split() for element in kone):
                            person_aegtefaelle = person.navn

                            for other in other_home:

                                if any(element in other.erhverv.lower().split() for element in kone):
                                    other_aegtefaelle = other.navn

                                    proximity = damerau_levenshtein_distance(person_aegtefaelle, other_aegtefaelle)

                                    if proximity < 3:
                                        return proximity # Begge personer har en ægtefælle med samme navn

            if self.kon is False and other.kon is False:

                if any(element in self.erhverv.lower().split() for element in kone):
                    person_aegtefaelle = getData.get_mand_home(person_home, self.lbnr)

                    if person_aegtefaelle is not None:

                        if any(element in other.erhverv.lower().split() for element in kone):
                            other_aegtefaelle = getData.get_mand_home(other_home, other.lbnr)

                            if other_aegtefaelle is not None:

                                proximity = damerau_levenshtein_distance(person_aegtefaelle, other_aegtefaelle)

                                if proximity < 3:
                                    return proximity # Begge personer har en ægtefælle med samme navn
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
            if proximity < 3:
                return 1
        return 0 # Begge personer bor præcis samme sted

