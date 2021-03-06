#!/usr/bin/env python3.4

class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'

    def blue(text):
        return Colors.BLUE + text + Colors.WHITE

    def bold(text):
        return Colors.BOLD + text + Colors.WHITE

    def green(text):
        return Colors.GREEN + text + Colors.WHITE

    def yellow(text):
        return Colors.YELLOW + text + Colors.WHITE

    def red(text):
        return Colors.RED + text + Colors.WHITE


class Question(object):

    def __init__(self, q):
        self.qnumber = q[0]
        self.question = q[1]
        self.a = q[2]
        self.b = q[3]
        self.c = q[4]
        self.d = q[5]
        self.answer = q[6]
        self.correct = q[7]
        self.incorrect = q[8]
        self.seen = q[9]
    
    def __str__(self):
        return self.qnumber

class Player(object):
    max_questions = 35

    def __init__(self, db_name):
        self.correct = []
        self.incorrect = []
        self.total = 0
        self.db_name = db_name
        self.conn = None
        self.cur = None
       
    def __call__(self):
        import sys
        self.intro()
        self.setup_db()
        for i in range(0, self.max_questions):
            question = self.get_question()
            self.print_question(question)
            self.get_answer(question)
        self.close_db()
        self.print_report()

    def print_answer(self, q):
        print(Colors.bold("{} - {}".format(q.qnumber, q.question)))
        print("\t{}: {}".format(q.answer, getattr(q, q.answer.lower())))


    def print_report(self):
        print("{}/{}={}".format(len(self.correct), self.total, 100 * (len(self.correct)/self.total)))
        if len(self.incorrect) > 0:
            print("\n\n{}\n".format(Colors.bold(Colors.red("Questions you missed"))))
            for i in self.incorrect:
                self.print_answer(i)

        if len(self.correct) > 0:
            print("\n\n{}\n".format(Colors.bold(Colors.blue("Questions you got correct"))))
            for i in self.correct:
                self.print_answer(i)

    def print_question(self, question):
        print(Colors.blue("Question: {} Seen: {} Correct: {} Incorrect: {}".format(
              question.qnumber,
              question.seen,
              question.correct,
              question.incorrect)))
        print('------------------------------------------------------')
        print(Colors.bold('\n>>> {}\n'.format(question.question)))
        print("a: {}".format(question.a))
        print("b: {}".format(question.b))
        print("c: {}".format(question.c))
        print("d: {}".format(question.d))

    def get_question(self):
        self.cur.execute('select * from questions group by seen order by seen limit 1')
        tmp = self.cur.fetchone()
        question = Question(tmp)
        self.set_seen(question)
        self.total = self.total + 1
        return question

    def set_seen(self, q):
        self.cur.execute("update questions set seen = seen + 1 where qnumber=?", (q.qnumber,))
        self.conn.commit()

    def set_correct(self, q):
        self.cur.execute("update questions set correct = correct + 1 where qnumber=?", (q.qnumber,))
        self.conn.commit()

    def set_incorrect(self, q):
        self.cur.execute("update questions set incorrect = incorrect + 1 where qnumber=?", (q.qnumber,))
        self.conn.commit()

    def award(self, q):
        self.set_correct(q)
        self.correct.append(q)
        print(Colors.yellow("\n>>> Correct!\n"))

    def participation_award(self, q):
        self.set_incorrect(q)
        self.incorrect.append(q)
        print(Colors.red('\n>>> You tried and that is all we can really ask of you\n'))

    def get_answer(self, q):
        import re
        acceptable = re.compile("^\s*[abcd]\s*$")
        while True:
            i = input("(a|b|c|d): ")
            if acceptable.match(i):
                if i.lower() == q.answer.lower():
                    self.award(q)
                    break
                else:
                    self.participation_award(q)
                    break

    def intro(self):
        print("\n\n")
        print('####################################')
        print('######     Hammi Jammy    ##########')
        print('####################################')
        print("\n\n")

    def setup_db(self):
        import sqlite3
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

    def close_db(self):
        if self.conn:
            self.conn.close()

def main():
    import sys

    if len(sys.argv) < 2:
        print('Please provide a database')
        sys.exit(-1)
    else:
        player = Player(sys.argv[1])
        player()


if __name__ == '__main__':
    main()
