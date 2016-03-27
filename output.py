import Person


class Outputter:
    @staticmethod
    def output(people, path):
        print(path)
        with open(path, 'w+') as file:
            file.write(Person.Person.topline())
            print(len(people))
            for person in people:
                s = person.to_csv()
                file.write(s)
        print("Done writing")
