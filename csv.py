from Person import Person
import codecs
import re
from os import sep


def kipnr(p, value):
    assert isinstance(p, Person)
    p.KIPnr = value


def kilde(p, value):
    assert isinstance(p, Person)
    p.kilde = value


def sogn(p, value):
    assert isinstance(p, Person)
    p.sogn = value


def herred(p, value):
    assert isinstance(p, Person)
    p.herred = value


def amt(p, value):
    assert isinstance(p, Person)
    p.amt = value


def lbnr(p, value):
    assert isinstance(p, Person)
    p.lbnr = int(value)


def kildehenvisning(p, value):
    assert isinstance(p, Person)
    p.kildehenvisning = value


def stednavn(p, value):
    assert isinstance(p, Person)
    p.stednavn = value


def husstands_familienr(p, value):
    assert isinstance(p, Person)
    p.husstands_familienr = value


def matr_nr_adresse(p, value):
    assert isinstance(p, Person)
    p.matr_nr_adresse = value


def navn(p, value):
    assert isinstance(p, Person)
    p.navn = value


def kon(p, value):
    assert isinstance(p, Person)
    p.kon = value == "M"


def alder_tal(p, value):
    if value:
        assert isinstance(p, Person)
        assert isinstance(value, str)
        index = value.index(",")
        if index > 0:
            value = value[0:index]
        p.alder_tal = int(value)
    else:
        p.valid = False


def fodeaar(p, value):
    value = re.search(r"[0-9]+", value, re.M | re.I)
    if (value):
        value = value.group()
        assert isinstance(p, Person)
        p.fodeaar = int(value)
    else:
        p.valid = False


civil_dic = {
    "gift": 2,
    "ugift": 0,
    "ukendt": 0,
    "enke": 3,
    "sepereret": 3,
    "fraskilt": 3
}


def civiltilstand(p, value):
    p.civilstand = civil_dic.get(value, 0)


switcher = {
    "KIPnr": kipnr,
    "kilde": kilde,
    "sogn": sogn,
    "herred": herred,
    "amt": amt,
    "lbnr": lbnr,
    "kildehenvisning": kildehenvisning,
    "stednavn": stednavn,
    "husstands_familienr": husstands_familienr,
    "matr_nr_adresse": matr_nr_adresse,
    "navn": navn,
    "køn": kon,
    "alder_tal": alder_tal,
    "fødeår": fodeaar,
    "nr_ægteskab": civiltilstand
}


def get_people(path):
    people = []

    with codecs.open(path, "r", "iso-8859-1") as f:
        assert isinstance(path, str)
        ind = path.rindex(sep)
        fi = path[ind:]
        year = re.search("[0-9]{4}", fi).group()
        year = int(year)
        d = {}
        first = True
        for line in f:
            fields = line.split(";")
            if first:
                for i in range(len(fields)):
                    field = fields[i]
                    d[i] = field.replace("\r\n", "")
                first = False
            else:
                p = Person(year)
                for i in range(len(fields)):
                    field = fields[i]
                    r = d[i]
                    method = switcher.get(r, None)
                    if callable(method):
                        method(p, field)
                people.append(p)
    return people


class CsvParser:
    def __init__(self, path):
        self.people = []
        self.path = path

    def get_people(self):
        people = get_people(self.path)
        assert isinstance(self.people, list)
        self.people.extend(people)
        return self.people
