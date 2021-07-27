import csv # For the saves and reads, this project uses csv (commaseperated values) files.
import random

class Student:
    
    def __init__(self, name, number, grade, lectures):
        self.name = name
        self.number = number
        self.grade = grade
        self.lectures = lectures


class Lecture:
    
    def __init__(self, name, grade, day, hour):
        self.name = name
        self.grade = grade
        self.day = day
        self.hour = hour
        
class Days:
    
    def __init__(self, day):
        self.day = day
        self.start_hour = [8,11,14]
   
class Schedule:
    def __init__(self, year, overlap_lectures):
        self.year = year # A grade of schedule.
        self.overlap_lectures = overlap_lectures # A list of lectures that can't have time with this schedule.
        self.days = [Days("Monday"), Days("Tuesday"), Days("Wednesday"), Days("Thursday"), Days("Friday")]
        self.temp = [Days("Monday"), Days("Tuesday"), Days("Wednesday"), Days("Thursday"), Days("Friday")]
    

    
def readstudents(lectures):
   
    students = []
    lectures_ = []
    
    with open("data/students.csv", "r", encoding="utf8") as file:
            reader = csv.DictReader(file, delimiter=';')
            for student in reader: # Checks which students takes which lecture. 1 means students take this lecture, 0 means not. The indexes of lectures written in main function.
                if int(student["BilProg"]) == 1:
                    lectures_.append(lectures[0])
                if int(student["Mat"]) == 1:
                    lectures_.append(lectures[1])
                if int(student["TekRes"]) == 1:
                    lectures_.append(lectures[2])
                if int(student["Fiz"]) == 1:
                    lectures_.append(lectures[3])
                if int(student["ElDevTem"]) == 1:
                    lectures_.append(lectures[4])
                if int(student["Mek"]) == 1:
                    lectures_.append(lectures[5])
                if int(student["Kont"]) == 1:
                    lectures_.append(lectures[6])
                if int(student["Elek"]) == 1:
                    lectures_.append(lectures[7])
                if int(student["Termo"]) == 1:
                    lectures_.append(lectures[8])
                if int(student["MuhMat"]) == 1:
                    lectures_.append(lectures[9])
                students.append(Student(student["name"], student["number"], student["grade"], lectures_)) # Creates a list of student objects.
                lectures_ = [] # Clear lecture list for next studet.
    return students

def readlectures():
    lectures = []
    with open("data/lectures.csv", "r", encoding="utf8") as file:
            reader = csv.DictReader(file, delimiter=';')
            for lecture in reader:
                lectures.append(Lecture(lecture["lecture"], lecture["grade"], "0", "0")) # Read name and grade of lectures and skips the time (day and hour = 0) that lectures have.
    return lectures

    
def create_schedule(lectures, grade):
    
    header = ["time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] 
    
    time_8 = ["08.00 AM","-","-","-","-","-"]
    time_11 = ["11.00 AM","-","-","-","-","-"]
    time_14 = ["14.00 PM","-","-","-","-","-"]
    
    for day in header:
        for lecture in lectures:
            if int(lecture.grade) == grade:
                if lecture.day == day:
                    if int(lecture.hour) == 0:
                        time_8[header.index(day)] = lecture.name
                    if int(lecture.hour) == 1:
                        time_11[header.index(day)] = lecture.name
                    if int(lecture.hour) == 2:
                        time_14[header.index(day)] = lecture.name
                        
    file_name = f"schedule{grade}.csv"
    try:
        with open(file_name, 'w') as f:
        
            writer = csv.writer(f, delimiter = ";", quotechar='"')
        
            writer.writerow(header)
            writer.writerow(time_8)
            writer.writerow(time_11)
            writer.writerow(time_14)
            
        print(f"{file_name} has been successfully written.")
        print("You can open this file with notepad or Microsoft Excel")
    except:
        print(f"Some errors appeared during writing {file_name}.")
        print(f"Try to close if {file_name} is open.")
        
        
def print_schedules(lectures):
    
    print("GRADE 1 SCHEDULE")
    print()
    for lecture in lectures:
        print(lecture.name, lecture.day, end="")
        if int(lecture.hour) == 0:
            print(" 8.00 AM")
        elif int(lecture.hour) == 1:
            print(" 11.00 AM")
        elif int(lecture.hour) == 2:
            print(" 14.00 PM")
        if lecture.name == "ElDevTem":
            print("\n\nGRADE 2 SCHEDULE\n")
            
    print()
    
    
def main():
    
    lectures = readlectures() # A list of lectures (as objects).
    
    # Indexes and names of lectures in the list of above (for example: lectures[0].name == BilProg)
    # 0 BilProg     1 Mat           2 TekRes    3 Fiz       4 ElDevTem      5 Mek 
    # 6 Kont        7 Elek          8 Termo     9 MuhMat 
    
    students = readstudents(lectures) # A list of students (as objects).
         
    # Firstly program detects overlaps lectures.
    
    overlaps_grade1 = [] # Lectures taken by 1'st grade students from upper grade.
    overlaps_grade2 = [] # Lectures taken by 2'st grade students from upper grade or lower grade.
    
    for student in students: 
        if int(student.grade) == 1:
            for lecture in student.lectures: # Program checks which lecture is overlapping grade 1 students has take.
                if int(lecture.grade) != 1:
                    overlaps_grade1.append(lecture)
        if int(student.grade) == 2: # Program checks which lecture is overlapping grade 2 students has take.
            for lecture in student.lectures:
                if int(lecture.grade) != 2:
                    overlaps_grade2.append(lecture)
    
    overlaps_grade1 = set(overlaps_grade1) # Program deletes recurring lectures.
    overlaps_grade2 = set(overlaps_grade2) # Program deletes recurring lectures.

    schedule_grade1 = Schedule(1, overlaps_grade1)
    schedule_grade2 = Schedule(2, overlaps_grade2)
    
    # Firstly program placing lectures that can't have same time with 1'st grade lectures.
        
    for lecture in overlaps_grade1: # Every lecture that overlapping with grade 1 lectures.
        day = random.randint(0,4)
        hour = random.randint(0,2)
        while int(schedule_grade1.temp[day].start_hour[hour]) not in [8, 11, 14]: # Check the hour whether is taken.
            day = random.randint(0,4)
            hour = random.randint(0,2)
        if int(lecture.grade) == 2: # If there is more lecture you can put down with elif and the same structure with replacing grade 3 grade 4 ....
            schedule_grade2.days[day].start_hour[hour] = lecture # Placing lecture into schedule object because it will use while placing other grades.
            schedule_grade2.temp[day].start_hour[hour] = -2 # -2 means that hour taken. Program uses temp object because the original object will used for schedule.
            lecture.day = schedule_grade2.temp[day].day # Program placeses day into lecture object because it will use while writing to the files.
            lecture.hour = hour # Program placeses hour into lecture object because it will use while writing to the files.
        schedule_grade1.temp[day].start_hour[hour] = -2 # -2 means that hour taken.
            
    # Secondly program placing lectures that can't have same time with 2'st grade lectures. Logically same with above process. 
    
    for lecture in overlaps_grade2:
        day = random.randint(0,4)
        hour = random.randint(0,2)
        while int(schedule_grade2.temp[day].start_hour[hour]) not in [8, 11, 14]:
            day = random.randint(0,4)
            hour = random.randint(0,2)
        if int(lecture.grade) == 1: 
            schedule_grade1.days[day].start_hour[hour] = lecture 
            schedule_grade1.temp[day].start_hour[hour] = -2 
            lecture.day = schedule_grade1.temp[day].day
            lecture.hour = hour
        schedule_grade2.temp[day].start_hour[hour] = -2 
    
    # Thirdly program placing 1'st grade lectures that do not overlap.
    
    for lecture in lectures:
        if lecture not in overlaps_grade1 and lecture not in overlaps_grade2:
            if int(lecture.grade) == 1:
                day = random.randint(0,4)
                hour = random.randint(0,2)
                while int(schedule_grade1.temp[day].start_hour[hour]) not in [8, 11, 14]:
                    day = random.randint(0,4)
                    hour = random.randint(0,2)
                schedule_grade1.days[day].start_hour[hour] = lecture # Placing lecture.
                schedule_grade1.temp[day].start_hour[hour] = -2 # -2 means that hour taken.
                lecture.day = schedule_grade1.temp[day].day
                lecture.hour = hour
    
    # Fourthly program placing 1'st grade lectures that do not overlap.
    
    for lecture in lectures:
        if lecture not in overlaps_grade1 and lecture not in overlaps_grade2:
            if int(lecture.grade) == 2:
                day = random.randint(0,4)
                hour = random.randint(0,2)
                while int(schedule_grade2.temp[day].start_hour[hour]) not in [8, 11, 14]:
                    day = random.randint(0,4)
                    hour = random.randint(0,2)
                schedule_grade2.days[day].start_hour[hour] = lecture # Placing lecture.
                schedule_grade2.temp[day].start_hour[hour] = -2 # -2 means that hour taken.
                lecture.day = schedule_grade2.temp[day].day
                lecture.hour = hour
    

    print_schedules(lectures)
    create_schedule(lectures,1)
    print()
    create_schedule(lectures,2)
            

if __name__ == "__main__":
    main()
