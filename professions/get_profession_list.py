def get_prof_list(intellect_list, personality_list) -> list:
    prof_list = []
    for pprof in personality_list:
        for iprof in intellect_list: 
            if pprof in iprof:
                prof_list.append(iprof)
    return prof_list