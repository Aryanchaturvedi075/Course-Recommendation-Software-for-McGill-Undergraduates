from neo4j import GraphDatabase
import xl_reader

#TODO: Bean for the neo4j database connection
class Neo4jDbConnection:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()


    @staticmethod
    def _execute_query(tx, query):
        tx.run(query)


    def _csv_toNeoDatabase(self):
        #TODO: should return the create statements string from reading the csv file for neo4j;
        courses_nodes = xl_reader.courses()
        professors = xl_reader.professors()
        program = xl_reader.programs()
        faculty = xl_reader.faculties()
        edges_prog_fac = xl_reader.programToFaculty()
        edges_course_prof = xl_reader.courseToProf()
        program_to_course = xl_reader.programToCourse()
        course_to_course_coReq = xl_reader.coreqRelation()
        course_to_course_restrict = xl_reader.restrictRelation()

        with self.driver.session() as session:

             # Clear Database before repopulating everything (aka the lazy way of updating database)
            for constraints in session.run("show constraints"):
                session.run("drop constraint " + constraints[1])

            session.execute_write(self._execute_query, "match (n) detach delete n")

            session.execute_write(self._execute_query,
                                  "CREATE CONSTRAINT FOR (n:COURSE) REQUIRE n.name IS UNIQUE")

            session.execute_write(self._execute_query,
                                  "CREATE CONSTRAINT FOR (a:PROFESSOR) REQUIRE a.name IS UNIQUE")
            
            session.execute_write(self._execute_query,
                                  "CREATE CONSTRAINT FOR (a:PROGRAM) REQUIRE a.name IS UNIQUE")
            
            session.execute_write(self._execute_query,
                                  "CREATE CONSTRAINT FOR (a:FACULTY) REQUIRE a.name IS UNIQUE")

            for key in courses_nodes:
                NEO_STRING =  "create (:COURSE {name: \"%s\", unlocked: %r , " \
                              "subject: \"%s\", type: \"%s\", title: \"%s\", credits: %d, " \
                              "level: %d, available: %r, taken: %r, " \
                              "gradeAvg: \"%s\", link: \"%s\", note: \"%s\"})" % (key,courses_nodes[key]["unlocked"],
                                                                      courses_nodes[key]["subject"],
                                                                      courses_nodes[key]["type"],
                                                                      courses_nodes[key]["title"],
                                                                      courses_nodes[key]["credits"],
                                                                      courses_nodes[key]["level"],
                                                                      courses_nodes[key]["available"],
                                                                      courses_nodes[key]["taken"],
                                                                      courses_nodes[key]["gradeAvg"],
                                                                      courses_nodes[key]["link"],
                                                                      courses_nodes[key]["note"])
                print(NEO_STRING)
                session.execute_write(self._execute_query, NEO_STRING)

            for key in professors:
                rating = professors[key]["rating"]
                name = key
                rateMyProfLink = professors[key]["rateMyProfLink"]
                NEO_STRING = f"create (:PROFESSOR {{name: \"{name}\", rating: {rating}, rateMyProfLink: \"{rateMyProfLink}\"}})"
                print(NEO_STRING)
                session.execute_write(self._execute_query, NEO_STRING)

            for key in program:
                name = key
                credits = program[key]["Credits"]
                NEO_STRING = f"create (:PROGRAM {{name: \"{name}\", credits: \"{credits}\"}})"
                print(NEO_STRING)
                session.execute_write(self._execute_query, NEO_STRING)

            for key in faculty:
                name = key
                NEO_STRING = f"create (:FACULTY {{name: \"{name}\"}})"
                print(NEO_STRING)
                session.execute_write(self._execute_query, NEO_STRING)

            for program in program_to_course:
                for course in program_to_course[program]:
                    relationship = program_to_course[program][course]['relationship'].upper()+"_COURSE"
                    NEO_STRING = f"""match (course:COURSE {{name: \"{course}\"}}), (prog:PROGRAM {{name: \"{program}\"}}) 
                                    create (prog) -[:{relationship}]-> (course)"""
                    print(NEO_STRING)
                    session.execute_write(self._execute_query, NEO_STRING)

            for key in edges_prog_fac:
                destination = edges_prog_fac[key]["destination"]
                NEO_STRING = f"""match (faculty:FACULTY {{name: \"{destination}\"}}), (program:PROGRAM {{name:\"{key}\"}}) 
                                create (program) -[:OFFERED_PROGRAM]-> (faculty)"""
                print(NEO_STRING)
                session.execute_write(self._execute_query, NEO_STRING)
            
            for key in edges_course_prof:
                destination = edges_course_prof[key]["destination"]
                semester = edges_course_prof[key]["semester"]
                NEO_STRING =    f"""match (course:COURSE {{name:\"{destination}\"}}), (professor:PROFESSOR {{name:\"{key}\"}}) 
                                    create (professor) -[:TEACHES {{semester:\"{semester}\"}}]-> (course)"""
                print(NEO_STRING)
                session.execute_write(self._execute_query, NEO_STRING)

            for origin in course_to_course_coReq:
                # match (origin:COURSE {name:"COMP 361D1"}), (destination:COURSE {name:"COMP 303"})
                # create (origin) -[:COREQUISITE {note:""}]-> (destination)
                for coreqs in course_to_course_coReq[origin]:
                    destination = coreqs[0]
                    note = coreqs[1]
                    NEO_STRING = f"match (origin:COURSE {{name: \"{origin}\"}}), (destination: COURSE {{name: \"{destination}\"}}) create (origin) -[:COREQUISITE {{note:\"{note}\"}}]-> (destination)"
                    print(NEO_STRING)
                    session.execute_write(self._execute_query, NEO_STRING)

            for origin in course_to_course_restrict:
                # match (origin:COURSE {name:"COMP 204"}), (destination:COURSE {name:"COMP 202"})
                # create (origin) -[:RESTRICTS {note:""}]-> (destination)
                for restrictions in course_to_course_restrict[origin]:
                    destination = restrictions[0]
                    note = restrictions[1]
                    NEO_STRING = f"match (origin:COURSE {{name: \"{origin}\"}}), (destination:COURSE {{name: \"{destination}\"}}) create (origin) -[:RESTRICTS {{note:\"{note}\"}}]-> (destination)"
                    print(NEO_STRING)
                    session.execute_write(self._execute_query, NEO_STRING)

if __name__ == "__main__":
    user = "neo4j"
    password = "jacob123"
    courses_science = Neo4jDbConnection("bolt://localhost:7687", user, password)
    courses_science._csv_toNeoDatabase()
    courses_science.close()