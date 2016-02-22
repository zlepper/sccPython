from comparison import damerau_levenshtein_distance

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
        s += str(self.valid) + "\n"
        return s

    @staticmethod
    def topline():
        return "id|year|KIPnr|kilde|sogn|herred|amt|lbnr|kildehenvisning|stednavn|husstands_familienr|matr_nr_adresse|navn|køn|alder_tal|fodeaar|fødested|civilstand|valid\n"

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

        if self.fodested and other.fodested != "":

            if "Her i Sognet" in self.fodested & "Her i Sognet" in other.fodested:
                proximity = damerau_levenshtein_distance(self.sogn, other.sogn)

            else:
                if "Her i Sognet" in self.fodested:
                    proximity = damerau_levenshtein_distance(self.sogn, other.fodested)

                if "Her i Sognet" in other.fodested:
                    proximity = damerau_levenshtein_distance(self.fodested, other.sogn)

                else:
                    proximity = damerau_levenshtein_distance(self.fodested, other.fodested)

            if proximity > 0.50:
                return 1
            else:
                return 0

        else:
            return 0
