from datetime import datetime
file1 = open('ispiti.txt', 'r+')
exams = {}

def load_exams():
    for line in file1.readlines():
        ln = line.split('|')
        exam = {'broj_indexa': ln[0], 'predmet': ln[1], 'broj_bodova': ln[4], 'ime': ln[2],
                'prezime': ln[3], 'datum': ln[5]}
        exams[ln[0]] = exam
def main():
    load_exams()
    while 1:
        print(' 1. Dodavanje novog ispita\n 2. Listanje ispita u tabeli')
        user_in = input('unesite opciju ili "x" za izlaz')
        if user_in == 'x' or user_in == 'X':
            file1.close()
            exit()
        elif user_in == '1':
            add_exam()
        elif user_in == '2':
            list_exam()

def add_exam():
    broj_indexa = ime = prezime = predmet = ''
    while broj_indexa == '':
        broj_indexa = input('Unesite broj indeksa')
    while len(predmet) < 4:
        predmet = input('Unesite predmet')
    while len(ime) < 4:
        ime = input('Unesite ime')
    while len(prezime) < 4:
        prezime = input('Unesite prezime')
    date = ''
    while 1:
        try:
            user_in = input('Unesite datum polaganja: ')
            date = datetime.strptime(user_in, '%d.%m.%Y').date()
            break
        except ValueError:
            print('Greska!')
            continue
    broj_bodova = 0
    while 1:
        try:
            user_in = input('Unesite broj bodova: ')
            broj_bodova = int(user_in)
            if 0 <= broj_bodova <= 100:
                break
            else:
                print('Greska!')
                continue
        except ValueError:
            print('Greska!')
            continue
    exam = {'broj_indexa': broj_indexa, 'predmet': predmet, 'broj_bodova': broj_bodova, 'ime': ime, 'prezime': prezime, 'datum': date}
    exams[broj_indexa] = exam
    file1.write(f'{broj_indexa}|{predmet}|{ime}|{prezime}|{broj_bodova}|{date}\n')

def list_exam():
    print('Broj indexa         Predmet             Ime                  Prezime           Datum             Bodovi            ')
    for ex in exams.keys():
        print('{0:<20s}{1:<20s}{2:<20s}{3:<20s}{4:<20s}{5:<20s}'.format(ex, exams[ex]['predmet'], exams[ex]['ime'], exams[ex]['prezime'], exams[ex]['datum'], str(exams[ex]['broj_bodova'])))
if __name__ == '__main__':
    main()