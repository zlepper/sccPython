from Person import Person
import codecs
import re
from os import sep
from time import time


def kipnr(p, value):
    assert isinstance(p, Person)
    p.KIPnr = value
    p.valid = not not value

    # if p.valid is False:
    # print("mangler KIPnr")


def kilde(p, value):
    assert isinstance(p, Person)
    p.kilde = value
    p.valid = not not value
    # if p.valid is False:
    #  print("mangler kilde")


def sogn(p, value):
    assert isinstance(p, Person)
    p.sogn = value
    p.valid = not not value
    # if p.valid is False:
    # print("mangler sogn")


def herred(p, value):
    assert isinstance(p, Person)
    p.herred = value
    p.valid = not not value
    # if p.valid is False:
    # print("mangler herred")


def amt(p, value):
    assert isinstance(p, Person)
    p.amt = value
    p.valid = not not value
    #  if p.valid is False:
    # print("mangler amt")


def lbnr(p, value):
    assert isinstance(p, Person)
    if "," in value:
        value = value[:value.rfind(",")]
    try:
        p.lbnr = int(value)
    except ValueError:
        p.lbnr = 0
        p.valid = False

        # if p.valid is False:
        # print("mangler ibnr")


def kildehenvisning(p, value):
    assert isinstance(p, Person)
    p.kildehenvisning = value
    p.valid = not not value
    # if p.valid is False:
    # print("mangler kildehenvisning")


def stednavn(p, value):
    assert isinstance(p, Person)
    p.stednavn = value
    p.valid = not not value
    # if p.valid is False:
    # print("mangler stednavn")


def husstands_familienr(p, value):
    assert isinstance(p, Person)
    p.husstands_familienr = value
    p.valid = not not value
    # if p.valid is False:
    # print("mangler husnr")


def matr_nr_adresse(p, value):
    assert isinstance(p, Person)
    p.matr_nr_adresse = value
    p.valid = not not value


def navn(p, value):
    assert isinstance(p, Person)
    p.navn = value
    p.valid = not not value
    # if p.valid is False:
    # print("mangler navn")


def kon(p, value):
    assert isinstance(p, Person)
    p.kon = value == "M"
    p.valid = not not value

    if p.valid is False:
        p.kon = None

        # if p.valid is False:
        # print("mangler køn")


def alder_tal(p, value):
    import logging
    if value:
        before_value = value
        assert isinstance(p, Person)
        assert isinstance(value, str)
        if "," in value:
            index = value.index(",")
            if index > 0:
                value = value[:index]
        try:
            p.alder_tal = int(value)
        except ValueError:
            logging.error(before_value + " : " + value)
            p.valid = False
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
        # print("mangler alder")

        # if p.valid is False:
        # print("mangler fødeår")


civil_dic = {
    "gift": 2,
    "Gift": 2,
    "ugift": 1,
    "Ugift": 1,
    "ukendt": 0,
    "Ukendt": 0,
    "enke": 3,
    "Enke": 3,
    "Enkemand": 3,
    "sepereret": 3,
    "Sepereret": 3,
    "fraskilt": 3,
    "Fraskilt": 3
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


def civilstkode(p, value):
    assert isinstance(p, Person)
    try:
        p.civilstand = int(value)
    except ValueError:
        p.valid = False
    p.civilstand_source = value


def ng_ægteskab(p, value):
    assert isinstance(p, Person)
    p.nregteskab = value


switcher = {
    "KIPnr": kipnr,
    "kilde": kilde,
    "sogn": sogn,
    "herred": herred,
    "amt": amt,
    "lbnr": lbnr,
    "kildehenvisning": kildehenvisning,
    "stednavn": stednavn,
    "husstnr": husstands_familienr,
    "matr_nr_adresse": matr_nr_adresse,
    "navn": navn,
    "køn": kon,
    "alder_tal": alder_tal,
    "alder": alder_tal,
    "fødeår": fodeaar,
    "nr_ægteskab": ng_ægteskab,
    "civilstand": civiltilstand,
    "fødested": fodested,
    "erhverv": erhverv,
    "stilling_i_husstanden": erhverv,
    "civilstkode": civilstkode
}


def get_people(path):
    import logging
    logging.basicConfig(filename='log.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
        self.path = path

    def get_people(self):
        return get_people(self.path)
