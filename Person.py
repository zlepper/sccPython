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
        s += self.KIPnr + "|"
        s += self.kilde + "|"
        s += self.sogn + "|"
        s += self.herred + "|"
        s += self.amt + "|"
        s += str(self.lbnr) + "|"
        s += self.kildehenvisning + "|"
        s += self.stednavn + "|"
        s += str(self.husstands_familienr) + "|"
        s += self.matr_nr_adresse + "|"
        s += self.navn + "|"
        if self.kon:
            s += "M"
        else:
            s += "K"
        s += "|"
        s += str(self.alder_tal) + "|"
        s += str(self.fodeaar) + "|"
        s += self.civilstand_source + "|"
        s += str(self.valid) + "|"
        return s

    @staticmethod
    def topline():
        return "id|year|KIPnr|kilde|sogn|herred|amt|lbnr|kildehenvisning|stednavn|husstands_familienr|matr_nr_adresse|navn|køn|alder_tal|fodeaar|civilstand|valid"
