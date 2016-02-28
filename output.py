import Person


class Outputter:
    @staticmethod
    def output(people, path):
        assert isinstance(path, str)
        assert isinstance(people, list)
        print(path)
        with open(path, 'w+') as file:
            file.write(Person.Person.topline())
            print(len(people))
            for person in people:
                assert isinstance(person, Person.Person)
                s = person.to_csv()
                g = person.get_closests()
                if g is not None:
                    for h in g[0]:
                        s += "\t" + str(g[1]) + "\t" + h.to_csv()
                file.write(s)
        print("Done writing")
