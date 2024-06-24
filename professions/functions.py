import json


def get_prof_dict():
    with open('professions\professions.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def get_prof_list(intellect, personality):
    prof_list = []
    for pprof in personality:
        for iprof in intellect: 
            if pprof in iprof:
                prof_list.append(iprof)
    return prof_list


def test_results(intellect, personality):
    intellect_list = []
    personality_list = []
    professions = []

    for key in intellect:
        if intellect[key] >= 8: intellect_list.append(key)
    for key in personality:
        if personality[key] >= 8: personality_list.append(key)

    prof_dict = get_prof_dict()

    for pprof in personality_list:
        for iprof in intellect_list:
            professions.append(get_prof_list(prof_dict[iprof], prof_dict[pprof]))
    
    return [intellect_list, personality_list, professions]