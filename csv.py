from Person import Person
import codecs
import re
from os import sep
from time import time


def kipnr(p, value):
    assert isinstance(p, Person)
    p.KIPnr = value
    p.valid = not not value


def kilde(p, value):
    assert isinstance(p, Person)
    p.kilde = value
    p.valid = not not value


def sogn(p, value):
    assert isinstance(p, Person)
    p.sogn = value
    p.valid = not not value


def herred(p, value):
    assert isinstance(p, Person)
    p.herred = value
    p.valid = not not value


def amt(p, value):
    assert isinstance(p, Person)
    p.amt = value
    p.valid = not not value


def lbnr(p, value):
    assert isinstance(p, Person)
    value = value[:value.rfind(",")]
    try:
        p.lbnr = int(value)
    except ValueError:
        p.lbnr = 0
        p.valid = False


def kildehenvisning(p, value):
    assert isinstance(p, Person)
    p.kildehenvisning = value
    p.valid = not not value


def stednavn(p, value):
    assert isinstance(p, Person)
    p.stednavn = value
    p.valid = not not value

def husstands_familienr(p, value):
    assert isinstance(p, Person)
    p.husstands_familienr = value
    p.valid = not not value

def matr_nr_adresse(p, value):
    assert isinstance(p, Person)
    p.matr_nr_adresse = value
    p.valid = not not value


def navn(p, value):
    assert isinstance(p, Person)
    p.navn = value
    p.valid = not not value

def kon(p, value):
    assert isinstance(p, Person)
    p.kon = value == "M"
    p.valid = not not value

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
    assert isinstance(p, Person)
    p.civilstand = civil_dic.get(value, 0)
    p.civilstand_source = value


def fodested(p, value):
    assert isinstance(p, Person)
    p.fodested = value


def erhverv(p, value):
    if p.erhverv:
        p.erhverv += " "
    p.erhverv += value


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
    "nr_ægteskab": civiltilstand,
    "fødested": fodested,
    "erhverv": erhverv,
    "stilling_i_husstanden": erhverv
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
            fields = line.split("|")
            if first:
                for i in range(len(fields)):
                    field = fields[i]
                    d[i] = field.replace("\r\n", "")
                first = False
            else:
                p = Person(year)
                for i in range(len(fields)):
                    field = fields[i]
                    try:
                        r = d[i]
                        method = switcher.get(r, None)
                        if method is not None:
                            method(p, field)
                    except KeyError:
                        print(fields)
                        p.valid = False
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
