from comparison import damerau_levenshtein_distance
from fodestedData import get_ditto_fodested
from fodestedData import get_home

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
        self.id = -1
        pass

    def __str__(self):
        return "Person(" + self.navn + ")"

    def __repr__(self):
        return self.__str__()

    def to_csv(self):
        s = ""
        s += str(self.id) + "|"
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
        s += str(self.erhverv) + "|"
        s += str(self.valid) + "\n"
        return s

    @staticmethod
    def topline():
        return "id|year|KIPnr|kilde|sogn|herred|amt|lbnr|kildehenvisning|stednavn|husstands_familienr|matr_nr_adresse|navn|køn|alder_tal|fodeaar|fødested|civilstand|erhverv|valid\n"

    def get_closests(self):
        highest = None
        closest = None
        for key, value in self.matches.items():
            if highest == None:
                highest = key
                closest = value
                continue
            if key > highest:
                highest = key
                closest = value
        return closest

    def compare_origin(self, other):

        if self.fodested != "" and other.fodested != "":

            if "her i sognet" in self.fodested.lower() and "her i sognet" in other.fodested.lower():
                proximity = damerau_levenshtein_distance(self.sogn, other.sogn)

            else:
                if "her i sognet" in self.fodested.lower() and "do" in other.fodested.lower() or "ditto" in other.fodested.lower():
                    fodested = get_ditto_fodested(people, other.KIPnr, other.ibnr) # Tilføj liste af personer

                    while other.husstands_familienr is fodested[0]:
                        fodested = get_ditto_fodested(people, other.KIPnr, other.ibnr - 1) # Tilføj liste af personer

                    if "her i sognet" in fodested[1].lower():
                        proximity = damerau_levenshtein_distance(self.sogn, other.sogn)

                if "her i sognet" in other.fodested.lower() and "do" in self.fodested.lower() or "ditto" in self.fodested.lower():
                    fodested = get_ditto_fodested(people, self.KIPnr, self.ibnr) # Tilføj liste af personer

                    while self.husstands_familienr is fodested[0]:
                        fodested = get_ditto_fodested(people, self.KIPnr, self.ibnr - 1) # Tilføj liste af personer

                    if "her i sognet" in fodested[1].lower():
                        proximity = damerau_levenshtein_distance(self.sogn, other.sogn)

                '''
                if "her i sognet" not in self.fodested.lower() and "her i sognet" not in other.fodested.lower():
                    proximity = damerau_levenshtein_distance(self.fodested, other.fodested)
                '''

            return proximity # Begge personer er født i samme sogn

        else:
            return 10

    def compare_family(self, other):

        # Sammenlign personerne efter deres mand eller kones navn
        if self.civilstand_source is "gift" and self.civilstand is 1 and other.civilstand_source is "gift" and other.civilstand is 1: # Hvis personerne ikke er gift, så findes personens mand eller kone ikke
            person_home = get_home(people, self.kilde, self.sogn, self.herred, self.amt, self.stednavn, self.husstands_familienr) # Tilføj liste af personer
            other_home = get_home(people, other.kilde, other.sogn, other.herred, other.amt, other.stednavn, other.husstands_familienr) # Tilføj liste af personer

            mand = ["mand", "hosbonde", "huusbond", "huusbonde", "boelsmand", "gaardmand", "huusmand", "dagleier", "huusfader", "huusfad"]
            kone = ["kone", "madmoder", "konen", "madmoeder", "huusmoder"]

            for person in person_home:

                if mand in person.erhverv.lower() or kone in person.erhverv.lower():
                    person_aegtefaelle = person.navn

                    for other in other_home:
                        if mand in other.erhverv.lower() or kone in other.erhverv.lower():
                            other_aegtefaelle = other.navn

                            proximity = damerau_levenshtein_distance(person_aegtefaelle, other_aegtefaelle)

            return proximity # Begge personer har en ægtefælle med samme navn



