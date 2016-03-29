from Person import Person
import codecs
import re
from os import sep
from time import time


def kipnr(p, value):
    p.KIPnr = value
    p.valid = p.valid and not not value


def kilde(p, value):
    p.kilde = value
    p.valid = p.valid and not not value


def sogn(p, value):
    p.sogn = p.valid and value
    p.valid = p.valid and not not value


def herred(p, value):
    p.herred = value
    p.valid = p.valid and not not value


def amt(p, value):
    p.amt = value
    p.valid = p.valid and not not value


def lbnr(p, value):
    if "," in value:
        value = value[:value.rfind(",")]
    try:
        p.lbnr = int(value)
    except ValueError:
        p.lbnr = 0
        p.valid = False


def kildehenvisning(p, value):
    p.kildehenvisning = value
    p.valid = p.valid and not not value


def stednavn(p, value):
    p.stednavn = value
    p.valid = p.valid and not not value


def husstands_familienr(p, value):
    p.husstands_familienr = value
    p.valid = p.valid and not not value


def matr_nr_adresse(p, value):
    p.matr_nr_adresse = value
    p.valid = p.valid and not not value


def navn(p, value):
    p.navn = value
    assert isinstance(value, str)
    p.valid = p.valid and not value.isspace()
    if p.navn == "":
        p.navn = "  "


def kon(p, value):
    p.kon = value == "M"
    p.valid = p.valid and not value.isspace()

    if p.valid is False:
        p.kon = None


def alder_tal(p, value):
    if value:
        before_value = value
        if "," in value:
            index = value.index(",")
            if index > 0:
                value = value[:index]
        try:
            p.alder_tal = int(value)
        except ValueError:
            p.valid = False
    else:
        p.valid = False


def fodeaar(p, value):
    value = re.search(r"[0-9]+", value, re.M | re.I)
    if value:
        value = value.group()
        p.fodeaar = int(value)
    else:
        p.valid = False


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
    p.civilstand = civil_dic.get(value, 0)


def fodested(p, value):
    herisognet = ["her i sognet", "heri sognet", "i sognet", "her sognet", "heri s", "her i s", "h. i sognet"]
    reference = ["do ", "do.", "ditto ", "dito ", "dto.", "dítto", "ds.", "das ", "item ", "it.", "ietm ", "ibidem "]
    sogn = [" sogn", " s.", " s:", " s/", " s "]
    amt = [" amt"]

    if value != "":
        p.fodested = ""

        while p.fodested == "":

            # Fødested referet til forrige persons fødested i hjemmet
            if any(element in value.lower() for element in reference):
                value = get_previous(1)

            # Fødested her i sognet
            if any(element in value.lower() for element in herisognet):
                p.fodested = p.sogn.lower()
                break

            # Fødested i et andet sogn
            elif any(element in value.lower() for element in sogn):

                for term in sogn:
                    if term in value.lower():
                        personfodested = value.lower().split(term)

                        if fodested != "":
                            p.fodested = personfodested[0]
                            break

            # Fødested indeholder et andet sogn og amt
            elif any(element in value.lower() for element in amt):

                if "," in value.lower():
                    personfodested = value.lower().split(",")

                elif "." in value.lower():
                    personfodested = value.lower().split(".")

                else:
                    personfodested = value.lower().split(" ")

                if personfodested is not []:
                    p.fodested = personfodested[0]
                    break

            # Fødested er kun angivet til et navn på et sogn
            else:
                p.fodested = value.lower()
                break


def erhverv(p, value):
    if p.erhverv:
        p.erhverv += " "
    p.erhverv += value


def civilstkode(p, value):
    try:
        p.civilstand = int(value)
    except ValueError:
        p.valid = False
    p.civilstand_source = value


def ng_ægteskab(p, value):
    p.nregteskab = value


switcher = {
    "KIPnr": kipnr,
    "kipnr": kipnr,
    "kilde": kilde,
    "sogn": sogn,
    "herred": herred,
    "amt": amt,
    "lbnr": lbnr,
    "stednavn": stednavn,
    "husstnr": husstands_familienr,
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


def get_previous(n):
    import globals_scc
    # Make n a negative number, so we go back in the list
    n *= -1
    try:
        return globals_scc.people[n].fodested
    except IndexError:
        return ""
    except TypeError:
        return ""


def get_people(path):
    # import logging
    import globals_scc
    # logging.basicConfig(filename='log.log', level=logging.DEBUG,
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    people = globals_scc.people
    if people is not None:
        globals_scc.people = people

    with codecs.open(path, "r", "iso-8859-1") as f:
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
                    d[i] = field.rstrip()
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
