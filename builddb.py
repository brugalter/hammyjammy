#!/usr/bin/env python3.4


def main ():
    import re
    import collections
    import sqlite3
    import sys

    question = re.compile(r"^(T\d\w\d\d)\s\((\w)\).*")
    answer = re.compile(r"^([ABCD])\.\s(.*)$")
    eoq = re.compile(r"^~+\s+?$")
    q = collections.OrderedDict()
    conn = None
    with open(sys.argv[2], 'r', encoding='windows-1252') as fd:
        line = fd.readline()
        while line:
            if question.match(line):
                match = question.match(line)
                q[match.group(1)] = {}
                q[match.group(1)]['answer'] = match.group(2)
                line = fd.readline()
                q[match.group(1)]['question'] = line
                while True:
                    line = fd.readline()
                    if eoq.match(line):
                        break
                    a = answer.match(line)
                    q[match.group(1)][a.group(1)] = a.group(2)
            else:
                line = fd.readline()

    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()
    try:
        c.execute('''create table questions
                     (qnumber text,
                      question text,
                      A text,
                      B text,
                      C text,
                      D text,
                      answer text,
                      correct integer,
                      incorrect integer,
                      seen integer)''')
    except sqlite3.OperationalError:
        print("Database and table already exists", file=sys.stderr)
        sys.exit(-1)
    else:
        for question, data in q.items():
            c.execute('insert into questions values (?,?,?,?,?,?,?,?,?,?)', 
                       (question.strip(),
                        data['question'].strip(),
                        data['A'].strip(),
                        data['B'].strip(),
                        data['C'].strip(),
                        data['D'].strip(),
                        data['answer'].strip(),
                        0,
                        0,
                        0))

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
