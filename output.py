import Person


class Outputter:
    @staticmethod
    def output(people, path):
        assert isinstance(path, str)
        assert isinstance(people, list)
        with open(path) as file:
            file.write(Person.Person.topline())
            for person in people:
                assert isinstance(person, Person.Person)
                s = person.to_csv()
                file.write(s)
