import xlwings as xw
# Specifying a sheet
ws_courses = xw.Book("resources/xl_files/CS_Major_(Science)_Nodes.xlsx").sheets['Nodes-Course']
ws_professors = xw.Book("resources/xl_files/CS_Major_(Science)_Nodes.xlsx").sheets['Nodes-Prof']
ws_prog_fac = xw.Book("resources/xl_files/CS_Major_(Science)_Nodes.xlsx").sheets['Nodes-Program_and_Faculty']

def courses():
    dictionary_compsci_course = {}
    list_course_codes = ws_courses.range("C2:C142").value
    list_course_subjects = ws_courses.range("B2:B142").value
    list_course_title = ws_courses.range("D2:D142").value
    list_course_credits = ws_courses.range("E2:E142").value
    list_course_available = ws_courses.range("F2:F142").value
    list_course_gradeAvg = ws_courses.range("G2:G142").value
    list_course_link = ws_courses.range("H2:H142").value
    list_course_note = ws_courses.range("I2:J142").value
    for index, course in enumerate(list_course_codes):
        dictionary_compsci_course[course] = {}
        dictionary_compsci_course[course]["unlocked"] = False
        if len(course) > 8:
            dictionary_compsci_course[course]["type"] = "multi-term"
        else:
            dictionary_compsci_course[course]["type"] = "single-term"
        dictionary_compsci_course[course]["level"] = int(course.split()[1][:3])
        dictionary_compsci_course[course]["taken"] = False
        dictionary_compsci_course[course]["subject"] = list_course_subjects[index]
        dictionary_compsci_course[course]["title"] = list_course_title[index]
        if(list_course_credits[index] == "N/A"):
            dictionary_compsci_course[course]["credits"] = -1
        else:
            dictionary_compsci_course[course]["credits"] = list_course_credits[index]
        if list_course_available[index] == "Y":
            dictionary_compsci_course[course]["available"] = True
        else:
            dictionary_compsci_course[course]["available"] = False
        dictionary_compsci_course[course]["gradeAvg"] = list_course_gradeAvg[index]
        dictionary_compsci_course[course]["link"] = list_course_link[index]
        dictionary_compsci_course[course]["note"] = list_course_note[index]
    return dictionary_compsci_course

def professors():
    dictionary_professor = {}
    list_names = ws_professors.range("B2:B53").value
    list_ratings = ws_professors.range("C2:C53").value
    list_ratemyProf = ws_professors.range("D2:D53").value

    for index, prof in enumerate(list_names):
        dictionary_professor[prof] = {}
        if(list_ratings[index] == "N/A"):
            dictionary_professor[prof]["rating"] = -1
        else:
            dictionary_professor[prof]["rating"] = list_ratings[index]
        dictionary_professor[prof]["rateMyProfLink"] = list_ratemyProf[index]
    return dictionary_professor



#TODO: JUST separate programs and faculty sheets eventually
def programs():
    dictionary_programs = {}
    list_names = ws_prog_fac.range("B2:B3").value
    list_credits = ws_prog_fac.range("C2:C3").value 
    for index, name in enumerate(list_names): 
        dictionary_programs[name] = {}
        dictionary_programs[name]["Credits"] = list_credits[index] 

    return dictionary_programs

def faculties():
    dictionary_faculties = {}
    list_names = ws_prog_fac.range("B4:B5").value
    for index, name in enumerate(list_names): 
        dictionary_faculties[name] = {}

    return dictionary_faculties


ws_course_to_program = xw.Book("resources/xl_files/CS_Major_(Science)_Edges.xlsx").sheets["Edges-Course_to_Program"]
ws_program_to_faculty = xw.Book("resources/xl_files/CS_Major_(Science)_Edges.xlsx").sheets['Edges-Program_to_Faculty']
ws_course_to_prof = xw.Book("resources/xl_files/CS_Major_(Science)_Edges.xlsx").sheets['Edges-Prof_to_Course']
ws_course_to_course = xw.Book("resources/xl_files/CS_Major_(Science)_Edges.xlsx").sheets['Edges-Course_to_Course']

def programToFaculty():
    dict_prog_fac = {}
    list_origin = ws_program_to_faculty.range("B2:B3").value
    list_destination = ws_program_to_faculty.range("C2:C3").value
    for index, origin in enumerate(list_origin):
        dict_prog_fac[origin] = {}
        dict_prog_fac[origin]["destination"] = list_destination[index]
    return dict_prog_fac

def courseToProf():
    dict_prof_course = {}
    list_origin = ws_course_to_prof.range("B2:B102").value
    list_destination = ws_course_to_prof.range("C2:C102").value
    list_semester = ws_course_to_prof.range("D2:D102").value
    for index, origin in enumerate(list_origin):
        dict_prof_course[origin] = {}
        dict_prof_course[origin]["destination"] = list_destination[index]
        dict_prof_course[origin]["semester"] = list_semester[index]
    return dict_prof_course

def programToCourse():
    course_to_program_list_courses = ws_course_to_program.range("B2:B102").value
    course_to_program_list_relationship = ws_course_to_program.range("A2:A102").value
    course_to_program_list_programs = ws_course_to_program.range("C2:C102").value
    course_to_program_list_notes = ws_course_to_program.range("D2:D102").value
    dictionary_ptoc = {}
    for index,program in enumerate(course_to_program_list_programs):
        if(program not in dictionary_ptoc):
            dictionary_ptoc[program] = {}
        if(course_to_program_list_relationship[index] != "Elective" and course_to_program_list_relationship[index] != "Complementary"):
            #TODO: Tackle complementary courses with everyone, danlin luo pls help
            dictionary_ptoc[program][course_to_program_list_courses[index]] = {}
            dictionary_ptoc[program][course_to_program_list_courses[index]]["relationship"] = course_to_program_list_relationship[index]
            dictionary_ptoc[program][course_to_program_list_courses[index]]["notes"] = course_to_program_list_notes[index] 
    
    return dictionary_ptoc

ws_ctoc_origin = ws_course_to_course.range("B2:B245").value
ws_ctoc_destination = ws_course_to_course.range("C2:C245").value
ws_ctoc_relation = ws_course_to_course.range("A2:A245").value
ws_ctoc_OR = ws_course_to_course.range("D2:D245").value
ws_ctoc_note = ws_course_to_course.range("E2:E245").value

def coreqRelation():
    dictionary_coreq ={}
    for index, origin in enumerate(ws_ctoc_origin):
        if ws_ctoc_relation[index] == "Corequisite":
            if origin not in dictionary_coreq:
                dictionary_coreq[origin]= []
            coreq_details = [ws_ctoc_destination[index], ws_ctoc_note[index]]
            dictionary_coreq[origin].append(coreq_details)
    return dictionary_coreq


def restrictRelation():
    dictionary_restrict ={}
    for index, origin in enumerate(ws_ctoc_origin):
        if ws_ctoc_relation[index] == "Restricts":
            if origin not in dictionary_restrict:
                dictionary_restrict[origin]= []
            restrict_details = [ws_ctoc_destination[index], ws_ctoc_note[index]]
            dictionary_restrict[origin].append(restrict_details)
    return dictionary_restrict