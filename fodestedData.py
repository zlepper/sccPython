
def get_ditto_fodested(people):

    dic = dict()
    for person in people:
        KIPnr_list = dic.get(person.KIPnr, [])
        KIPnr_list.append(person)
        dic[person.sogn] = KIPnr_list

        KIPnr_list = dic.get(person.KIPnr, [])
        KIPnr_list.append(person)
        dic[person.sogn] = KIPnr_list

def get_all_sogn(people):

    dic = dict()
    for person in people:
        sogn_list = dic.get(person.sogn, [])
        sogn_list.append(person)
        dic[person.sogn] = sogn_list



