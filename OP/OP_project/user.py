import re
from tabulate import tabulate

email_valid = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class User:
    all = {}
    user_num = 0
    passwords = {}
    passw_file = None
    users_file = None
    logged = None

    @classmethod
    def load_users(cls):
        cls.passw_file.seek(0)
        cls.passw_file.readline()
        for passw in cls.passw_file.readlines():
            line = passw.strip('\n')
            if line == '':
                continue
            line = line.split('|')
            cls.passwords[line[0]] = line[1]
            cls.users_file.seek(0)
            cls.users_file.readline()
        for users in cls.users_file.readlines():
            line = users.strip('\n')
            if line == '':
                continue
            line = line.split('|')
            User(username=line[0], password=cls.passwords[line[0]], firstname=line[1], lastname=line[2],
                 role=line[3],
                 gender=line[4], phone=line[5], email=line[6],
                 blocked=(True if line[7] == '1' else False))

    @classmethod
    def loadfiles(cls, file1, file2):
        cls.users_file = file1
        cls.passw_file = file2

    @classmethod
    def login(cls):
        user_name = ''
        password = ''
        while 1:
            user_name = input('Unesite username: ')
            if user_name not in cls.all.keys():
                print('Korisnik ne postoji! ')
                continue
            else:
                if cls.all[user_name].blocked:
                    print('Korisnik je blokiran')
                    continue
                else:
                    break
        while 1:
            password = input('Unesite password: ')
            if password != User.passwords[user_name]:
                print('Pogresna lozinka!')
                continue
            else:
                break
        print(f'Uspesna prijava! Dobrodosao/la {user_name}')
        print('Vas role je:', User.all[user_name].role)
        cls.logged = User.all[user_name]
        return

    @classmethod
    def register(cls, user_role):
        while 1:
            user_name = input('Unesite username: ')
            if user_name != '':
                if user_name not in User.all.keys():
                    print('Korisnicko ime je dostupno! ')
                    break
                else:
                    print('Korisnicko ime nije dostupno! ')
                    continue
        while 1:
            password = input('Unesite password: ')
            if password != '':
                user_in = input('Ponovite password: ')
                if user_in == password:
                    cls.passwords[user_name] = password
                    break
        print('Unesite trazene podatke: ')
        firstname = lastname = ''
        while firstname == '' or lastname == '':
            firstname = input('Ime: ')
            lastname = input('Prezime: ')
        while 1:

            gender = input('Pol (musko/zensko): ')
            gender = gender.lower()
            if gender == 'musko' or gender == 'zensko':
                break
            else:
                continue
        while 1:
            phone = input('Telefon: ')
            if len(phone) >= 6 and phone.isnumeric():
                break
            else:
                print('Neispravan format telefona! ')
                continue
        while 1:
            email = input('E-mail: ')
            if re.fullmatch(email_valid, email):
                break
            else:
                print("Neispravan format emaila! ")
                continue

        User(username=user_name, password=password, firstname=firstname, lastname=lastname, gender=gender, phone=phone,
             email=email, role=('guest' if user_role == 'guest' else 'host'), blocked=False)
        input('Korisnik je uspesno registrovan!   Pritisnite ENTER da se vratite na pocetni ekran')
        cls.save_to_file()
        return

    @classmethod
    def block_user(cls):
        print('1. Blokiranje korisnika')
        print('2. Deblokiranje korisnika')
        print('3. Izlaz')
        while 1:
            user_in = input('Unesite opciju: ')
            if user_in == '1':
                cls.print_users('')
                while 1:
                    user_in = input('Unesite username korisnika koga zelite blokirati ili "x" za kraj: ')
                    if user_in == 'x':
                        break
                    if user_in not in cls.all.keys():
                        print('Korisnik ne postoji! ')
                        continue
                    else:
                        uname = user_in
                        if cls.all[uname].role == 'admin':
                            print('Nije moguce blokirati admina! ')
                            continue
                        elif cls.all[uname].blocked:
                            print('Korisnik je vec blokiran! ')
                            continue

                        else:
                            while 1:
                                user_in = input(
                                    'Da li ste sigurni da zelite blokirati korisnika ' + uname + '?  da/ne:  ')
                                if user_in == 'da':
                                    cls.all[uname].blocked = True
                                    print('Korisnik uspesno blokiran! ')
                                    break
                                else:
                                    break
            elif user_in == '2':
                print('Blokirani korisnici: ')
                cls.print_users('blocked')
                while 1:
                    user_in = input('Unesite username korisnika koga zelite odblokirati ili "x" za kraj: ')
                    if user_in == 'x':
                        break
                    if user_in not in cls.all.keys():
                        print('Korisnik ne postoji! ')
                        continue
                    else:
                        uname = user_in
                        if not cls.all[user_in].blocked:
                            print('Korisnik nije blokiran! ')
                        else:
                            while 1:
                                user_in = input(
                                    'Da li ste sigurni da zelite odblokirati korisnika: ' + uname + '?  da/ne: ')
                                if user_in == 'da':
                                    cls.all[uname].blocked = False
                                    print('Korisnik uspesno odblokiran! ')
                                    break
                                else:
                                    break
            elif user_in == '3':
                cls.save_to_file()
                return

    @classmethod
    def print_users(cls, status):
        lst = []
        if status == "blocked":
            for it in cls.all:
                user = cls.all[it]
                if user.blocked:
                    sublist = [user.firstName, user.lastName, user.username, user.email, user.role]
                    lst.append(sublist)
        else:
            for it in cls.all:
                user = cls.all[it]
                sublist = [user.firstName, user.lastName, user.username, user.email, user.role]
                lst.append(sublist)
        print(tabulate(lst, headers=['Ime', 'Prezime', 'username', 'email', 'uloga'], tablefmt='fancy_grid'))
        return

    def __init__(self, username: str, password: str, firstname: str, lastname: str, role: str, gender='m', phone='',
                 email='', blocked=False):
        self.__username = username
        self.__password = password
        self.firstName = firstname
        self.lastName = lastname
        self.gender = gender
        self.phone = phone
        self.email = email
        self._role = role
        User.user_num = User.user_num + 1
        self.userID = User.user_num
        self.blocked = blocked
        # Adding all users to a list
        User.all[self.username] = self

    def __repr__(self):
        return f'username:{self.username}, name: {self.firstName}, lastname: {self.lastName}, role: {self.role},' \
               f' gender: {self.gender}, phone: {self.phone}, email: {self.email}, password: {self.password}'

    @classmethod
    def save_to_file(cls):
        cls.users_file.truncate(0)
        cls.passw_file.truncate(0)
        cls.users_file.seek(0)
        cls.passw_file.seek(0)
        cls.users_file.write('username|firstname|lastname|role|gender|phone|email|blocked\n')
        cls.passw_file.write('username|password\n')
        for it in cls.all.keys():
            user = cls.all[it]
            cls.users_file.write(f'{user.username}|{user.firstName}|{user.lastName}|{user.role}|{user.gender}|'
                                 f'{user.phone}|{user.email}|{("1" if user.blocked else "0")}\n')
        for it in cls.passwords.keys():
            cls.passw_file.write(f'{it}|{cls.passwords[it]}\n')
        return

    # def __repr__(self):
    #  return self.username
    @property  # role read only
    def role(self):
        return self._role

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @username.setter
    def username(self, uname):
        self.__username = uname

    @password.setter
    def password(self, passw):
        self.__password = passw
