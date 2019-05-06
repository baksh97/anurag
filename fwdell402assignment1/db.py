import numpy as np 


class Database:
    def __init__(self):
        
        self.names = {}
        self.usernames = {}
        self.marks = []
        self.passwords = []
        self.students = []
        self.users = []
        self.subjects = ['English', 'Math', 'Physics', 'Chemistry', 'Computers']
        self.inst_pwd = ""

        lines = []
        with open('student_marks.csv', "r") as fd:
            lines = fd.read().splitlines()
            fd.close()

        count = 0        
        for line in lines:
            row = line.split(',')
            self.names[row[0]] = count
            self.usernames[row[1]] = count
            self.students.append(row[0])
            self.users.append(row[1])
            self.marks.append(row[2:])
            count += 1

        self.marks = np.array(self.marks).astype(np.int32)
        
        with open('user_pass.csv', "r") as fd:
            lines = fd.read().splitlines()
            fd.close()
    
        for line in lines:
            row = line.split(',')
            self.passwords.append(row[1])

        self.inst_pwd = self.passwords[-1]
        self.passwords.pop()
        
        print("database initiated")

    def print_stuff(self):
        print(self.usernames)
        print(self.passwords)
        print(self.usernames)
        print(self.marks)

    def get_marks_student(self, usr):
        # print(self.usernames)
        index = self.usernames[usr]
        return self.marks[index].astype(np.int)
        
    def get_aggr_student(self, usr):
        marks = self.get_marks_student(usr)
        return np.mean(marks)

    def get_min_max_student(self,usr):
        marks = self.get_marks_student(usr)
        m1 = np.argmin(marks)
        m2 = np.argmax(marks)
        return [self.subjects[m1], marks[m1], self.subjects[m2], marks[m2]]

    def get_subjectwise_bw(self):
        m1 = np.min(self.marks.astype(float), axis = 0)
        m2 = np.max(self.marks.astype(float), axis = 0)
        return m2, m1

    def get_marks_all(self):
        marklist = {}
        for name in self.names:
            marklist[name] = self.marks[self.names[name]].astype(np.uint32)
        return marklist

    def get_aggr_all(self):
        aggrs = np.mean(self.marks.astype(float), axis=1)
        aggr_list = {}
        for name in self.names:
            aggr_list[name] = aggrs[self.names[name]]
        return aggr_list

    def get_class_mean(self):
        return np.mean(self.marks.astype(float), axis=0)

    def get_num_failed(self):
        return np.sum(self.marks.astype(float) < 33.33, axis=0)
        
    def get_bestnworst(self):
        aggrs = np.mean(self.marks.astype(float), axis=1)
        # print(aggrs)

        m1 = np.argmin(self.marks, axis = 0)
        m2 = np.argmax(self.marks, axis = 0)

        # print(self.students[m1])
        worst = []
        best = []
        

        for row in m1:
            worst.append(self.students[row])

        for row in m2:
            best.append(self.students[row])
        

        n1 = np.argmin(aggrs)
        n2 = np.argmax(aggrs)

        worst.append(self.students[n1])
        best.append(self.students[n2])
        # print(self.students[n1])
        return best,worst

    def update(self, name, subject, mark):

        if name not in self.students:
            return False
        if subject not in self.subjects:
            return False

        stud_index = self.names[name]
        subj_index = self.subjects.index(subject)
        self.marks[stud_index][subj_index] = int(mark)

        # if(mark == 100 and self.marks[stud_index][subj_index] == 10):
        #     self.marks[stud_index][subj_index] = 100
        #     print(self.marks[stud_index][subj_index])

        with open('student_marks.csv', 'r') as file:
            data = file.readlines()
        newline = name + "," + self.get_username(name)
        for m in self.marks[stud_index]:
            newline += "," + str(m)
        newline += '\n'
        # print(newline)
        data[stud_index] = newline
        # print(newline)
        with open('student_marks.csv', 'w') as file:
            file.writelines( data )
        return True

    def get_username(self, name):
        n = name.lower()
        n = n.replace(" ", "_")
        return(n)

    def get_name(self, username):
        if username == 'instructor':
            return username
        n = username.replace("_"," ").title()
        return n

    def login(self, uid, pwd):
        if uid == 'instructor':
            return pwd == self.inst_pwd
        else:
            if uid not in self.users:
                return False
            if pwd != self.passwords[self.usernames[uid]]:
                return False
            return True


def main():
    db = Database()
    # print(db.login("instructor","jdf84Rv8pZ"))
    # db.get_bestnworst() 
    print(db.update('Eric Denmark', 'Computers', 100))
        
if __name__ == '__main__':
    main()