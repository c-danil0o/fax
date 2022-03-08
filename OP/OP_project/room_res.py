from user import User
import random
from datetime import datetime, timedelta
from tabulate import tabulate


class Room:
    all = {}
    ids = list(range(0, 100))
    rooms_file = None
    amenities_file = None
    amenities_list = {}
    search_list = []
    today = datetime.now().date()
    weekday = today.isoweekday()

    def __init__(self, room_id: str, room_type: str, numberofrooms: str, numberofguests: str,
                 adress: tuple,
                 availability: list, price: float, amenities: list,
                 status='neaktivan', host=User, fromfile=False):
        self._room_id = room_id
        self.room_type = room_type
        self.numberofrooms = numberofrooms
        self.numberofguests = numberofguests
        self.adress = adress
        self.availability = availability
        self.merge_dates()
        self.host = host
        self.price = price
        self.status = status
        self.amenities = amenities
        if not fromfile:
            avb = []
            for date in self.availability:
                date1 = date[0].strftime('%d.%m.%Y')
                date2 = date[1].strftime('%d.%m.%Y')
                avb.append(date1 + '-' + date2)
            Room.rooms_file.write(
                f'{self.room_id}|{self.room_type}|{self.numberofrooms}|{self.numberofguests}|'
                f'{"#".join(self.adress)}|{":".join(avb)}|{self.host.username}|{self.price}|{self.status}'
                f'|{":".join(self.amenities)}\n')
        # init actions
        Room.all[self.room_id] = self

    @property
    def room_id(self):
        return self._room_id

    @classmethod
    def load_files(cls, room_file, amen_file):
        cls.rooms_file = room_file
        cls.amenities_file = amen_file

    @classmethod
    def load_rooms(cls):
        cls.rooms_file.seek(0)
        cls.rooms_file.readline()  # preskace se prvi red
        for line in cls.rooms_file:
            line = line.strip('\n')
            if line == '':
                continue
            data = line.split('|')
            avb = data[5].split(':')
            dt = []
            adress = tuple(data[4].split('#'))
            cls.ids.remove(int(data[0]))
            for a in avb:
                date = a.split('-')
                tpl = [datetime.strptime(date[0], '%d.%m.%Y').date(), datetime.strptime(date[1], '%d.%m.%Y').date()]
                dt.append(tpl)
            Room(room_id=data[0], room_type=data[1], numberofrooms=data[2],
                 numberofguests=data[3], adress=adress, availability=dt,
                 host=User.all[data[6]], price=float(data[7]), status=data[8], amenities=data[9].split(':'),
                 fromfile=True)

    @classmethod
    def load_amenities(cls):
        cls.amenities_file.seek(0)
        for line in cls.amenities_file:
            line = line.strip('\n')
            if line == '':
                continue
            data = line.split(':')
            cls.amenities_list[data[0]] = data[1]

    @classmethod
    def add_amenities(cls):
        print('Dodavanje novih sadrzaja za apartmane: ')
        while 1:
            user_in = input('Unesite novu dodatnu opremu ili "x" za kraj: ')
            if user_in == 'x':
                break
            else:
                if user_in not in cls.amenities_list.values():
                    cls.amenities_list[str(len(cls.amenities_list) + 1)] = user_in
                else:
                    print('Uneseni sadrzaj vec postoji! ')
                    continue

    @classmethod
    def remove_amenities(cls):
        print('Brisanje dodatne opreme: ')
        for f in cls.amenities_list:
            print(f'{f}: {cls.amenities_list[f]}')

        while 1:
            nonvalid = 0
            user_in = input('Unesite sifru sadrzaja koji zelite obrisati ili "x" za kraj:  ')
            if user_in == 'x':
                break
            if user_in in cls.amenities_list.keys():
                item = cls.amenities_list[user_in]
                for room in cls.all:
                    if item in cls.all[room].amenities:
                        print('Izabrani sadrzaj nije moguce obrisati! ')
                        nonvalid = 1
                        break
                if nonvalid:
                    continue
                del cls.amenities_list[user_in]
                print('Sadrzaj uspesno obrisan! ')
                temp_list = {}
                for i, j in zip(range(1, len(cls.amenities_list) + 1), cls.amenities_list):
                    temp_list[str(i)] = cls.amenities_list[j]
                cls.amenities_list = temp_list
                continue

    @classmethod
    def add_room(cls):
        room_id = random.choice(cls.ids)
        cls.ids.remove(room_id)
        room_id = str(room_id)
        print('Adresa apartmana: ')
        street = ''
        while street == '' or len(street) < 5:
            street = input('Unesite ulicu: ')
        while 1:
            num = input('Unesite broj: ')
            if num != '':
                if num[0].isdecimal() or num == 'bb':
                    break
        city = ''
        while city == '' or len(city) < 3:
            city = input('Unesite grad: ')
        postal_num = ''
        while postal_num == '' or (not postal_num.isnumeric()):
            postal_num = input('Unesite postanski broj: ')
        adress = (street, num, city, postal_num)
        while 1:
            room_type = input('Tip smestaja  (apartman/soba): ')
            room_type = room_type.lower()
            if room_type == 'apartman' or room_type == 'soba':
                break
            else:
                continue
        while 1:
            numberofrooms = input('Broj spavacih soba: ')
            if numberofrooms.isnumeric() and int(numberofrooms) < 50:
                break
        while 1:
            numberofguests = input('Maksimalan broj gostiju: ')
            if numberofguests.isnumeric() and int(numberofguests) < 50:
                break
        print('Dostupnost apartmana: \nUnesite datume u formatu dd.mm.yyyy ili "x" da zavrsite')
        availability = []
        while 1:
            try:
                od = input('od: ')
                if od == 'x':
                    break
                date1 = datetime.strptime(od, '%d.%m.%Y').date()
                do = input('do: ')
                if do == 'x':
                    break
                date2 = datetime.strptime(do, '%d.%m.%Y').date()
                if date1 > date2:
                    print('Drugi datum mora biti veci od prvog!')
                    continue
                if date1 < cls.today or date2 < cls.today:
                    print('Nije moguce dodati datum iz proslosti! ')
                    continue
                dt = [date1, date2]
                availability.append(dt)
                print(tabulate(availability, tablefmt='fancy_grid'))
            except ValueError:
                print('Pogresan format datuma!')

        host = User.logged
        price = 0
        while 1:
            try:
                price = float(input('Cena: ').strip('$'))
                break
            except ValueError:
                print('Pogresan format cene! ')
                continue
        status = 'neaktivan'
        amenities = []
        print('Lista sadrzaja apartmana: ')
        for f in cls.amenities_list:
            print(f'{f}: {cls.amenities_list[f]}')
        while 1:
            user_in = input('Unesite ime ili sifru zeljenog sadrzaja ili "x" za kraj: ')
            if user_in == 'x':
                break
            if user_in in cls.amenities_list.keys():
                amenities.append(cls.amenities_list[user_in])
            else:
                if user_in in cls.amenities_list.values():
                    amenities.append(user_in)
        print('Vas apartman: ')
        print(f'Adresa: {adress}\n Tip apartmana: {room_type}\n '
              f'Broj spavacih soba: {numberofrooms}\n Maksimalan broj gostiju: {numberofguests}\n'
              f' Cena: {price}\n Lista sadrzaja: {amenities} ')
        print(' Dostupnost: ')
        print(tabulate(availability, tablefmt='fancy_grid'))
        user_in = input('Da li ste sigurni da zelite dodati apartman:  da/ne  ')
        if user_in == 'da':
            Room(room_id=room_id, adress=adress, amenities=amenities, availability=availability,
                 numberofguests=numberofguests, numberofrooms=numberofrooms, room_type=room_type, price=price,
                 status=status, host=host, fromfile=False)
        else:
            return

    @classmethod
    def manage_room(cls):
        print('Vasi apartmani: ')
        cls.print_rooms('all', User.logged)

        while 1:
            user_in = input('Unesite ID apartmana kojeg zelite izmeniti: ')
            if user_in in cls.all.keys():
                break
            else:
                print('Taj apartman ne postoji!')
                continue
        room_copy = cls.all[user_in]
        room_copy.manage_room_ins()

    def manage_room_ins(self):
        print('Lista dostupnih parametara za izmenu: \n  1. Adresa\n  2. Tip smestaja\n'
              '  3. Broj spavacih soba\n  4. Broj gostiju\n  5. Cena\n  6. Dostupnost\n  7. Sadrzaj\n  8. Status\n '
              ' 0. Kraj')

        while 1:
            user_in = input('Unesite opciju: ')
            if user_in == '1':
                print('Adresa apartmana: ')
                street = ''
                while street == '' or len(street) < 4:
                    street = input('Unesite ulicu: ')
                while 1:
                    num = input('Unesite broj: ')
                    if num != '':
                        if num[0].isdecimal() or num == 'bb':
                            break
                    else:
                        break
                city = ''
                while city == '' or len(city) < 3:
                    city = input('Unesite grad: ')
                postal_num = ''
                while postal_num == '' or (not postal_num.isnumeric()):
                    postal_num = input('Unesite postanski broj: ')
                self.adress = (street if street != '' else self.adress[0], num if num != '' else self.adress[1],
                               city if city != '' else self.adress[2],
                               postal_num if postal_num != '' else self.adress[3])
            elif user_in == '2':
                while 1:
                    room_type = input('Tip smestaja  (apartman/soba): ')
                    room_type = room_type.lower()
                    if room_type == 'apartman' or room_type == 'soba':
                        self.room_type = room_type if room_type != '' else self.room_type
                        break
                    else:
                        continue

            elif user_in == '3':
                while 1:
                    numberofrooms = input('Broj spavacih soba: ')
                    if numberofrooms.isnumeric() and int(numberofrooms) < 50:
                        self.numberofrooms = numberofrooms if numberofrooms != '' else self.numberofrooms
                        break
            elif user_in == '4':
                while 1:
                    numberofguests = input('Maksimalan broj gostiju: ')
                    if numberofguests.isnumeric() and int(numberofguests) < 50:
                        self.numberofguests = numberofguests if numberofguests != '' else self.numberofguests
                        break
            elif user_in == '5':
                while 1:
                    price = input('Cena')
                    try:
                        self.price = float(price) if price != '' else self.price
                    except ValueError:
                        print('Pogresan format cene! ')
                        continue
            elif user_in == '6':
                availability = []
                print('Dostupnost apartmana:')
                print(tabulate(self.availability, tablefmt='fancy_grid'))
                print('Unosenjem novih datuma ponistavate sve stare!')
                print('Unesite datume u formatu dd.mm.yyyy ili "x" da odustanete! ')

                while 1:
                    try:
                        od = input('od: ')
                        if od == 'x':
                            break
                        date1 = datetime.strptime(od, '%d.%m.%Y').date()
                        do = input('do: ')
                        if do == 'x':
                            break
                        date2 = datetime.strptime(do, '%d.%m.%Y').date()
                        if date1 >= date2:
                            print('Drugi datum mora biti veci od prvog!')
                            continue
                        dt = [date1, date2]
                        err = 0
                        for res in Reservation.all.keys():
                            reser = Reservation.all[res]
                            if reser.room_idd == self.room_id:
                                if reser.cin_cout[0] <= date1 <= reser.cin_cout[1] or reser.cin_cout[0] <= date2 <= \
                                        reser.cin_cout[1]:
                                    print('Termin nije moguce promeniti jer je vec rezervisan! ')
                                    err = 1
                                    continue
                        if not err:
                            availability.append(dt)

                        print(tabulate(availability, tablefmt='fancy_grid'))
                    except ValueError:
                        print('Pogresan format datuma!')
                user_in = input('Da li ste sigurni da zelite dodati nove termine? da/ne:  ')
                if user_in == 'da':
                    self.availability = availability
                    self.merge_dates()
            elif user_in == '7':
                amenities = []
                for f in Room.amenities_list:
                    print(f'{f}: {Room.amenities_list[f]}')
                while 1:
                    user_in = input('Unesite ime ili sifru zeljenog sadrzaja ili "x" za kraj: ')
                    if user_in == 'x':
                        self.amenities = amenities
                        break
                    if user_in.isdecimal():
                        amenities.append(Room.amenities_list[user_in])
                    else:
                        if user_in in Room.amenities_list.values():
                            amenities.append(user_in)
            elif user_in == '8':
                while 1:
                    status = input('Status apartmana (akivan/neaktivan):  ')
                    if status == 'aktivan' or status == 'neaktivan':
                        self.status = status
                        break
                    else:
                        continue
            elif user_in == '0':
                print('Vas apartman: ')
                print(f'Adresa: {self.adress}\n Tip apartmana: {self.room_type}\n '
                      f'Broj spavacih soba: {self.numberofrooms}\n Maksimalan broj gostiju: {self.numberofguests}\n'
                      f' Cena: {self.price}\n Lista sadrzaja: {self.amenities} ')
                print(' Dostupnost: ')
                print(tabulate(self.availability, tablefmt='fancy_grid'))
                user_in = input('Da li zelite potvrditi izmene? da/ne: ')
                if user_in == 'da':
                    Room.all[self.room_id] = self
                    Room.save_to_file()
                return

    def merge(self):
        for x in range(len(self.availability) - 1):
            if self.availability[x][1] >= self.availability[x + 1][0] - timedelta(days=1):
                if self.availability[x][1] <= self.availability[x + 1][1]:
                    self.availability[x][1] = self.availability[x + 1][1]
                    del self.availability[x + 1]
                    self.merge()
                    return
                if self.availability[x][1] >= self.availability[x + 1][1]:
                    del self.availability[x + 1]
                    self.merge()
                    return
        return

    def merge_dates(self):
        # sortiranje
        for i in range(len(self.availability)):
            for j in range(len(self.availability)):
                if self.availability[j][0] > self.availability[i][0]:
                    tmp = self.availability[j]
                    self.availability[j] = self.availability[i]
                    self.availability[i] = tmp
        self.merge()
        return

    @classmethod
    def delete_room(cls):
        print('Lista vasih apartmana je: ')
        cls.print_rooms('all', User.logged)
        print('Brisanjem apartmana, brisete i sve rezervacije povezane sa njim! ')
        while 1:
            user_in = input('Unesite ID apartmana koji zelite obrisati ili "x" da izadjete: ')
            if user_in == 'x':
                break
            if user_in in cls.all.keys():
                print('Da li ste sigurni da zelite obrisati apartman: ')
                room = cls.all[user_in]
                rid = user_in
                lst = [room.room_id, ", ".join(room.adress), room.price, ", ".join(room.amenities), room.status]
                print(tabulate([lst], headers=['id', 'adress', 'price', 'amenities', 'status'], tablefmt='fancy_grid'))
                user_in = input('da/ne: ')
                if user_in == 'da':
                    room.status = 'obrisan'
                    for res in Reservation.all.keys():
                        if Reservation.all[res].reservation_id == rid:
                            del Reservation.all[res]
                    break
            else:
                print('Taj apartman ne postoji!')
                continue
        return

    @classmethod
    def search_byplace(cls):
        place = input('Unesite mesto: ')
        for room in cls.all:
            if place in cls.all[room].adress[2]:
                cls.search_list.append(cls.all[room])

        return 0

    @classmethod
    def search_bydate(cls):
        print('Unesite datume u formatu dd.mm.yyyy.\n'
              ' Ukoliko zelite samo uneti samo jedan od datuma, drugi mozete ostaviti prazan.')
        while 1:
            od = input('od: ')
            do = input('do: ')
            if od != '' and do != '':
                date1 = cls.date_convert(od)
                if not date1:
                    continue
                date2 = cls.date_convert(do)
                if not date2:
                    continue
                if date1 > date2:
                    print('Greska!')
                    continue
                for room in cls.all:
                    for avb in cls.all[room].availability:
                        if date1 >= avb[0] and date2 <= avb[1]:
                            cls.search_list.append(cls.all[room])
                return 0
            elif od == '' and do == '':
                cls.search_list = list(cls.all.values())
                return 0
            elif do == '':
                date1 = cls.date_convert(od)
                if not date1:
                    continue
                for room in cls.all:
                    for avb in cls.all[room].availability:
                        if date1 <= avb[0]:
                            cls.search_list.append(cls.all[room])
                            break
                return 0
            elif od == '':
                date2 = cls.date_convert(do)
                if not date2:
                    continue
                for room in cls.all:
                    for avb in cls.all[room].availability:
                        if date2 >= avb[1]:
                            cls.search_list.append(cls.all[room])
                return 0

    @classmethod
    def search_byrooms(cls):
        try:
            print('Broj soba: ')
            od = input('od: ')
            do = input('do: ')
            for room in cls.all:
                if od != '' and do != '':
                    if int(od) <= int(cls.all[room].numberofrooms) <= int(do):
                        cls.search_list.append(cls.all[room])
                elif od == '' and do == '':
                    cls.search_list = list(cls.all.values())

                elif do == '':
                    if int(od) <= int(cls.all[room].numberofrooms):
                        cls.search_list.append(cls.all[room])
                elif od == '':
                    if int(do) >= int(cls.all[room].numberofrooms):
                        cls.search_list.append(cls.all[room])
        except ValueError:
            return 1
        else:
            return 0

    @classmethod
    def search_byguests(cls):
        try:
            print('Broj gostiju: ')
            od = input('od: ')
            do = input('do: ')
            for room in cls.all:
                if od != '' and do != '':
                    if int(od) <= int(cls.all[room].numberofguests) <= int(do):
                        cls.search_list.append(cls.all[room])
                elif od == '' and do == '':
                    cls.search_list = list(cls.all.values())
                elif do == '':
                    if int(od) <= int(cls.all[room].numberofguests):
                        cls.search_list.append(cls.all[room])
                elif od == '':
                    if int(do) >= int(cls.all[room].numberofguests):
                        cls.search_list.append(cls.all[room])
        except ValueError:
            return 1
        else:
            return 0

    @classmethod
    def search_byprice(cls):
        try:
            print('Cena: ')
            od = input('od: ')
            do = input('do: ')
            for room in cls.all:
                if od != '' and do != '':
                    if float(od) <= cls.all[room].price <= float(do):
                        cls.search_list.append(cls.all[room])
                elif od == '' and do == '':
                    cls.search_list = list(cls.all.values())
                elif do == '':
                    if float(od) <= cls.all[room].price:
                        cls.search_list.append(cls.all[room])
                elif od == '':
                    if float(do) >= cls.all[room].price:
                        cls.search_list.append(cls.all[room])
        except ValueError:
            return 1
        else:
            return 0

    @classmethod
    def search(cls):
        options = ['1', '2', '3', '4', '5', '6']
        cls.search_list = []
        while 1:
            cls.search_list = []
            print('Kriterijumi za pretragu apartmana:\n 1. Mesto\n 2. Dostupnost\n '
                  '3. Broj soba\n 4. Broj osoba\n 5. Cena\n 6. Izlaz')
            user_in = input('Unesite zeljeni kriterijum: ')
            if user_in not in options:
                continue
            if user_in == '1':
                cls.search_byplace()
            elif user_in == '2':
                cls.search_bydate()
            elif user_in == '3':
                if cls.search_byrooms():
                    print('Greska!')
            elif user_in == '4':
                if cls.search_byguests():
                    print('Greska!')
            elif user_in == '5':
                if cls.search_byprice():
                    print('Greska!')
            elif user_in == '6':
                return 0
            lst = []
            for room in cls.search_list:
                if room.status == 'aktivan':
                    sublist = [room.room_id, ", ".join(room.adress), room.price, ", ".join(room.amenities),
                               room.numberofrooms, room.numberofguests,
                               room.status]
                    lst.append(sublist)
            print(tabulate(lst, headers=['ID', 'Adresa', 'Cena', 'Sadrzaj', 'Broj soba', 'Broj gostiju', 'Status'],
                           tablefmt='fancy_grid'))

    @classmethod
    def multi_search(cls):
        print('Unosite redom kriterijume. Ukoliko zelite preskociti neki kriterijum ostavite polje prazno. ')
        cls.search_list = []
        print('Kriterijumi za pretragu: ')
        cls.search_byplace()
        temp_list = cls.search_list
        cls.search_list = []
        cls.search_bydate()
        temp_list = cls.intersection(temp_list, cls.search_list)
        cls.search_list = []
        while cls.search_byrooms():
            print('Greska!')
        temp_list = cls.intersection(temp_list, cls.search_list)
        cls.search_list = []
        while cls.search_byguests():
            print('Greska!')
        temp_list = cls.intersection(temp_list, cls.search_list)
        cls.search_list = []
        while cls.search_byprice():
            print('Greska!')
        temp_list = cls.intersection(temp_list, cls.search_list)
        cls.search_list = []
        lst = []
        for line in temp_list:
            sublist = [line.room_id, ",".join(line.adress), line.price, ", ".join(line.amenities),
                       line.numberofrooms, line.status]
            lst.append(sublist)
        print(tabulate(lst, headers=['room_id', 'adress', 'price', 'amenities', 'num of rooms', 'status'],
                       tablefmt='fancy_grid'))

    # reformatirati pretragu da radi preko search liste

    @staticmethod
    def print_rooms(status, usr=''):
        lst = []
        if status == 'all':
            if usr == '':

                for rooms in Room.all:
                    room = Room.all[rooms]
                    sublist = [room.room_id, ", ".join(room.adress), room.price, ", ".join(room.amenities),
                               room.numberofrooms, room.numberofguests, room.status]
                    lst.append(sublist)
            else:
                for rooms in Room.all:
                    room = Room.all[rooms]
                    if Room.all[rooms].host == usr:
                        sublist = [room.room_id, ", ".join(room.adress), room.price, ", ".join(room.amenities),
                                   room.numberofrooms, room.numberofguests,
                                   room.status]
                        lst.append(sublist)
        else:
            for rooms in Room.all:
                room = Room.all[rooms]
                if Room.all[rooms].status == status:
                    sublist = [room.room_id, ", ".join(room.adress), room.price, ", ".join(room.amenities),
                               room.numberofrooms, room.numberofguests, room.status]
                    lst.append(sublist)
        print(tabulate(lst, headers=['ID', 'Adresa', 'Cena', 'Sadrzaj', 'Broj soba', 'Broj gostiju', 'Status'],
                       tablefmt='fancy_grid'))
        return

    @staticmethod
    def date_convert(date_str):
        try:
            date = datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            print('Greska u formatu datuma!')
            return 0
        else:
            return date

    @staticmethod
    def intersection(lst1, lst2):
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3

    @classmethod
    def decline(cls):
        for rm in cls.all.keys():
            hst = cls.all[rm].host.username
            if User.all[hst].blocked:
                cls.all[rm].status = 'neaktivan'

    @staticmethod
    def validate_input(user_in, options):
        if user_in not in options.keys():
            return 0  # greska
        return options[user_in]

    @classmethod
    def save_to_file(cls):
        cls.rooms_file.truncate(0)
        cls.amenities_file.truncate(0)
        cls.amenities_file.seek(0)
        cls.rooms_file.seek(0)
        cls.rooms_file.write(
            'room_id|numberofrooms|numberofguests|adress|availability|host|price|status|amenities\n')
        for rom in cls.all:
            room = cls.all[rom]
            avb = []
            for date in room.availability:
                date1 = date[0].strftime('%d.%m.%Y')
                date2 = date[1].strftime('%d.%m.%Y')
                avb.append(date1 + '-' + date2)
            cls.rooms_file.write(
                f'{room.room_id}|{room.room_type}|{room.numberofrooms}|{room.numberofguests}|'
                f'{"#".join(room.adress)}|{":".join(avb)}|{room.host.username}|{room.price}|{room.status}'
                f'|{":".join(room.amenities)}\n')

        for amen in cls.amenities_list.keys():
            cls.amenities_file.write(amen + ':' + cls.amenities_list[amen] + '\n')

    def __repr__(self):
        return f'id:{self.room_id}, adress:{self.adress}, price:{self.price}, amenities:{self.amenities}, ' \
               f'status: {self.status}'
    # def __repr__(self):
    # return [self.room_id, ",".join(self.adress), str(self.price), ",".join(self.amenities), self.guest.username,
    #       self.status]


class Reservation(User, Room):
    all = {}
    reservations_file = None
    discount = False
    holidays = ['01.01.2022', '02.01.2022', '03.01.2022', '07.01.2022', '27.01.2022', '15.02.2022', '16.02.2022',
                '15.04.2022', '16.04.2022', '17.04.2022', '18.04.2022',
                '22.04.2022', '23.04.2022', '24.04.2022', '25.04.2022', '01.05.2022', '02.05.2022', '03.05.2022',
                '09.05.2022', '28.06.2022', '09.07.2022', '05.10.2022', '21.10.2022', '11.11.2022', '25.12.2022']

    def __init__(self, reservation_id: str, room_idd: Room.room_id, cin_cout: list, nights: int, price: float,
                 guest: User, host: User,
                 aditional_guests: list, status='Kreirana'):
        self.reservation_id = reservation_id
        self.room_idd = room_idd
        self.cin_cout = cin_cout
        self.nights = nights
        self.price = price
        self.guest = guest
        self.host = host
        self.aditional_guests = aditional_guests
        self.status = status
        Reservation.all[self.reservation_id] = self

    @classmethod
    def load_files(cls, res_file, *args):
        cls.reservations_file = res_file

    @classmethod
    def load_reservations(cls):
        cls.reservations_file.seek(0)
        cls.reservations_file.readline()
        for line in cls.reservations_file:
            line = line.strip('\n')
            line = line.split('|')
            dt = line[1].split('-')
            d2 = datetime.strptime(dt[1], '%d.%m.%Y').date()
            dates = [datetime.strptime(dt[0], '%d.%m.%Y').date(), d2]
            status = line[5]
            if status == 'Kreirana' and cls.today > d2:
                status = 'Odbijena'
            if status == 'Potvrdjena' and cls.today > d2:
                status = 'Zavrsena'

            # room_id | cin - cout | nights | price | guest | status | aditional_guests | reservation_id | host
            Reservation(line[7], line[0], dates, line[2], float(line[3]), User.all[line[4]], User.all[line[8]],
                        line[6].split(','), status)

        return

    @classmethod
    def make_reservation(cls, user):
        cls.print_rooms('aktivan', 'all')
        while 1:
            print('Nova rezervacija: \n    1. Pretraga\n    2. Unos ID\n    3. Izlaz')
            user_in = input('Unesite opciju: ')
            if user_in == '1':
                Room.search()
            elif user_in == '2':
                idd = input('Unesite ID sobe: ')
                if (idd not in Room.all.keys()) or Room.all[idd].status == 'neaktivan':
                    print('Izabrani apartman nije aktivan ili ne postoji! ')
                    continue
                break
            elif user_in == '3':
                return
        today = datetime.now().date()
        print('Danas je: ', today.strftime('%d.%m.%Y'))
        print('Dostupnost apartmana: ')
        calendar = [today + timedelta(days=i) for i in range(31)]
        disp_calendar = [str(calendar[i].day) for i in range(31)]
        for avb in Room.all[idd].availability:
            for i in range(0, 31):
                if avb[0] <= calendar[i] <= avb[1]:
                    disp_calendar[i] = str(calendar[i].day) + ' ✓'
        print(tabulate([disp_calendar[0:7], disp_calendar[7: 14], disp_calendar[14:21], disp_calendar[21:28],
                        disp_calendar[28:31]], tablefmt='fancy_grid'))
        cin_date = ''
        date = None
        nights = 0
        while 1:
            try:
                cin_date = input('Unesite datum prijavljivanja(dd.mm.yyyy) ili "x": ')
                if cin_date == 'x':
                    return
                date = datetime.strptime(cin_date, '%d.%m.%Y').date()
                if date < cls.today:
                    print('Uneseni datum je prosao! ')
                    continue
                nights = 0
                while not nights:
                    try:
                        nights = int(input('Unesite broj noci: '))
                    except ValueError:
                        print('Greska!')
                        continue
                state = 'nonvalid'
                for avb in Room.all[idd].availability:
                    if avb[0] <= date <= avb[1] and date + timedelta(days=nights - 1) <= avb[1]:
                        print('Termin je validan!')
                        state = 'valid'
                        break
                if state == 'valid':
                    break
                print('Nemoguce je rezervisati uneseni termin!')

            except ValueError:
                print('Greska u formatu datuma ili broju noci!')
                continue
        aditional_guests = []
        count = 0
        while 1:
            user_in = input('Da li dolazite sami? da/ne:  ')
            if user_in == 'da':
                break
            elif user_in == 'ne':
                while 1:
                    if count == int(Room.all[idd].numberofguests):
                        print('Uneli ste maksimalan broj gostiju! ')
                        break
                    print('Unesite ime i prezime svakog dodatnog gosta ili "x" za kraj: ')
                    name = input('Ime: ')
                    if name == 'x':
                        break
                    lname = input('Prezime: ')
                    if lname == 'x':
                        break
                    aditional_guests.append(name + ' ' + lname)
                    count += 1
                break
        price = 0
        status = 'Kreirana'
        reservation_id = str(random.randint(10, 99))
        while reservation_id in cls.all.keys():
            reservation_id = str(random.randint(10, 99))
        for i in range(nights):
            dt = date + timedelta(days=i)
            if dt.isoweekday() == '5' or dt.isoweekday() == '6' or dt.isoweekday() == '7':
                price_temp = Room.all[idd].price * 0.9
                if dt.strftime('%d.%m.%Y') in cls.holidays:
                    price_temp = price_temp * 1.05
            else:
                price_temp = Room.all[idd].price
                if dt.strftime('%d.%m.%Y') in cls.holidays:
                    price_temp = price_temp * 1.05
            price += price_temp

        if cls.discount:
            price = price * 0.95
        print(
            f'Vasa rezervacija je:\n ID sobe: {idd}\n Datum dolaska: {cin_date}\n Broj noci: {nights}\n '
            f'Ukupna cena: {price}\n Dodatni gosti: {", ".join(aditional_guests)}')
        while 1:
            user_in = input('Da li zelite potvrditi rezervaciju?  da/ne: ')
            if user_in == 'ne':
                return
            elif user_in == 'da':
                break
        cdate = date + timedelta(days=nights - 1)
        for avb in Room.all[idd].availability:
            if avb[0] <= date <= avb[1] and date + timedelta(days=nights - 1) <= avb[1]:
                if cdate < avb[1]:
                    if date == avb[0]:
                        avb[0] = cdate + timedelta(days=1)
                        break
                    if date != avb[0]:
                        ol1 = avb[1]
                        avb[1] = date - timedelta(days=1)
                        ndate = [cdate + timedelta(days=1), ol1]
                        Room.all[idd].availability.append(ndate)
                        break
                if cdate == avb[1]:
                    if date == avb[0]:
                        Room.all[idd].availability.remove(avb)
                    else:
                        avb[1] = date - timedelta(days=1)
                    break
        Reservation(reservation_id, idd, [date, cdate], nights, price, user, Room.all[idd].host,
                    aditional_guests, status)
        print('Rezervacija je uspesno kreirana! ')
        user_in = input('Da li zelite zakazati jos rezervacija? (za svaku sledecu imate 5% popusta)  da/ne:  ')
        if user_in == 'da':
            cls.discount = True
            cls.make_reservation(user)
        cls.discount = False
        return

    @classmethod
    def cancel_reservation(cls, user):
        cls.print_reservations(user)
        res = ''
        while 1:
            user_in = input('Unesite ID rezevacije koju zelite otkazati:  ')
            if user_in in cls.all.keys():
                res = user_in
                if cls.all[res].status == 'Odustanak':
                    print('Rezervacija je vec otkazana! ')
                    continue
                if cls.all[res].status == 'Zavrsena':
                    print('Rezervacija je vec zavrsena!')
                    continue
                break
            else:
                print('Taj rezervacija ne postoji!')
                continue
        user_in = input('Da li ste sigurni da zelite otkazati rezervaciju ID:' + res + ' da/ne: ')
        if user_in == 'da':
            dates = cls.all[res].cin_cout
            idd = cls.all[res].room_idd
            Room.all[idd].availability.append(dates)
            Room.all[idd].merge_dates()
            cls.all[res].status = 'Odustanak'

            print('Rezervacija uspesno otkazana! ')
        return

    @classmethod
    def print_reservations(cls, user):
        lst = []
        if user.role == 'admin':
            #  room_id | cin - cout | nights | price | guest | status | aditional_guests | reservation_id | host
            # room id|datumi|noci|cena|gost|status|dodatni gosti|host
            for it in cls.all.keys():
                res = cls.all[it]
                lst.append([res.reservation_id, res.room_idd,
                            res.cin_cout[0].strftime('%d.%m.%Y-') +
                            res.cin_cout[1].strftime('%d.%m.%Y'),
                            res.nights,
                            res.price,
                            res.guest.username,
                            res.status,
                            res.host.username])
        elif user.role == 'host':
            for it in Reservation.all.keys():
                res = Reservation.all[it]
                if res.host == user:
                    lst.append([res.reservation_id, res.room_idd,
                                res.cin_cout[0].strftime('%d.%m.%Y-') +
                                res.cin_cout[1].strftime('%d.%m.%Y'),
                                res.nights,
                                res.price,
                                res.guest.username,
                                res.status,
                                res.host.username])
        elif user.role == 'guest':

            for it in Reservation.all.keys():
                res = cls.all[it]
                if res.guest == user:
                    lst.append([res.reservation_id, res.room_idd,
                                res.cin_cout[0].strftime('%d.%m.%Y-') +
                                res.cin_cout[1].strftime('%d.%m.%Y'),
                                res.nights,
                                res.price,
                                res.guest.username,
                                res.status,
                                res.host.username])
        print(tabulate(lst, headers=['ID', 'ID sobe', 'Datum', 'Nocenja', 'Cena', 'Gost', 'Status', 'Domacin'],
                       tablefmt='fancy_grid'))
        return

    @classmethod
    def approve_reservation(cls, user):
        lst = []
        for it in cls.all.keys():
            if cls.all[it].host == user and cls.all[it].status == 'Kreirana' or \
                    cls.all[it].status == 'Odbijena':
                res = cls.all[it]
                lst.append([res.reservation_id, res.room_idd,
                            res.cin_cout[0].strftime('%d.%m.%Y-') +
                            res.cin_cout[1].strftime('%d.%m.%Y'),
                            res.nights,
                            res.price,
                            res.guest.username,
                            res.status,
                            res.host.username])
        print(tabulate(lst, headers=['ID', 'ID sobe', 'Datum', 'Nocenja', 'Cena', 'Gost', 'Status', 'Domacin'],
                       tablefmt='fancy_grid'))
        print('  1. Potvrda\n  2. Odbijanje\n  3. Izlaz')
        while 1:
            user_in = input('Unesite opciju: ')
            if user_in == '1':
                while 1:
                    user_in = input('Unesite ID rezervacije koju zelite potvrditi ili "x" za izlaz: ')
                    nextr = 0
                    if user_in == 'x':
                        return
                    for res in lst:
                        nextr = 0
                        if res[0] == user_in:
                            rid = user_in
                            user_in = input('Da li ste sigurni da zelite potvrditi rezervaciju?  da/ne: ')
                            if user_in == 'da':
                                cls.all[rid].status = 'Prihvacena'
                            nextr = 1
                            break
                    if nextr:
                        continue

                    print('Pogresan ID')
                    continue
            elif user_in == '2':
                user_in = input('Unesite ID rezervacije koju zelite odbiti ili "x" za izlaz: ')
                nextr = 0
                if user_in == 'x':
                    return
                for res in lst:
                    nextr = 0
                    if res[0] == user_in:
                        rid = user_in
                        user_in = input('Da li ste sigurni da zelite odbiti rezervaciju?  da/ne: ')
                        if user_in == 'da':
                            cls.all[rid].status = 'Odbijena'
                            dates = cls.all[rid].cin_cout
                            idd = cls.all[rid].room_idd
                            Room.all[idd].availability.append(dates)
                            Room.all[idd].merge_dates()

                        nextr = 1
                        break
                if nextr:
                    continue

                print('Pogresan ID')
                continue
            elif user_in == '3':
                return

    @classmethod
    def search_reservations(cls):
        while 1:
            print('Pretraga po: \n 1. Statusu\n 2. Adresi\n 3. Domacinu\n 4. Izlaz')
            user_in = input('Unesite opciju: ')
            if user_in == '1':
                while 1:
                    print(' 1. Prihvacena\n 2. Odbijena\n 3. Izlaz')
                    user_in = input('Unesite opciju: ')
                    status = ''
                    if user_in == '1':
                        status = 'Prihvacena'
                    elif user_in == '2':
                        status = 'Odbijena'
                    elif user_in == '3':
                        break
                    else:
                        continue
                    lst = []
                    for it in cls.all:
                        if cls.all[it].status == status:
                            res = cls.all[it]
                            lst.append([res.reservation_id, res.room_idd,
                                        res.cin_cout[0].strftime('%d.%m.%Y-') +
                                        res.cin_cout[1].strftime('%d.%m.%Y'),
                                        res.nights,
                                        res.price,
                                        res.guest.username,
                                        res.status,
                                        res.host.username])
                    print(tabulate(lst,
                                   headers=['ID', 'ID sobe', 'Datum', 'Nocenja', 'Cena', 'Gost', 'Status', 'Domacin'],
                                   tablefmt='fancy_grid'))
            elif user_in == '2':
                user_in = input('Unesite adresu (ili dio adrese): ')
                lst = []
                for it in cls.all:
                    idd = cls.all[it].room_idd
                    adress = ', '.join(Room.all[idd].adress)
                    if user_in in adress:
                        res = cls.all[it]
                        lst.append([res.reservation_id, res.room_idd,
                                    res.cin_cout[0].strftime('%d.%m.%Y-') +
                                    res.cin_cout[1].strftime('%d.%m.%Y'),
                                    res.nights,
                                    res.price,
                                    res.guest.username,
                                    res.status,
                                    res.host.username,
                                    adress])
                print(tabulate(lst, headers=['ID', 'ID sobe', 'Datum', 'Nocenja', 'Cena', 'Gost', 'Status', 'Domacin',
                                             'Adresa'], tablefmt='fancy_grid'))
            elif user_in == '3':
                while 1:
                    user_in = input('Unesite username domacina ili "x" za kraj: ')
                    if user_in == 'x':
                        break
                    if user_in not in User.all.keys():
                        print('username ne postoji')
                        continue
                    else:
                        if User.all[user_in].role != 'host':
                            print('Korisnik nema status domacina! ')
                            continue
                        else:

                            lst = []
                            for it in cls.all:
                                if cls.all[it].host.username == user_in:
                                    res = cls.all[it]
                                    lst.append([res.reservation_id, res.room_idd,
                                                res.cin_cout[0].strftime('%d.%m.%Y-') +
                                                res.cin_cout[1].strftime('%d.%m.%Y'),
                                                res.nights,
                                                res.price,
                                                res.guest.username,
                                                res.status,
                                                res.host.username])
                            print(tabulate(lst, headers=['ID', 'ID sobe', 'Datum', 'Nocenja', 'Cena', 'Gost', 'Status',
                                                         'Domacin'],
                                           tablefmt='fancy_grid'))
                            break
            elif user_in == '4':
                break

    @classmethod
    def top10(cls):
        top = {}
        today = datetime.now().date()
        pastyear = today - timedelta(days=365)
        for it in cls.all.keys():
            res = cls.all[it]
            if today >= res.cin_cout[1] and res.cin_cout[0] >= pastyear and res.status == 'Zavrsena':
                idd = res.room_idd
                if Room.all[idd].adress[2] not in top.keys():
                    top[Room.all[idd].adress[2]] = 1
                else:
                    top[Room.all[idd].adress[2]] += 1
        lst = []
        for city, i in zip(sorted(top, key=top.get, reverse=True), range(10)):
            lst.append([city, top[city]])
        print(tabulate(lst, headers=['Grad', 'Broj rezervacija'], tablefmt='fancy_grid'))

    @classmethod
    def report_resday(cls):
        while 1:
            user_in = input('Unesite dan rezervacije (dd.mm.yyyy) ili "x" za kraj: ')
            if user_in == 'x':
                break
            date = cls.date_convert(user_in)
            if not date:
                continue
            lst = []
            for it in cls.all.keys():
                res = cls.all[it]
                if res.status == 'Zavrsena' and (res.cin_cout[0] <= date <= res.cin_cout[1]):
                    lst.append([res.reservation_id, res.room_idd,
                                res.cin_cout[0].strftime('%d.%m.%Y-') +
                                res.cin_cout[1].strftime('%d.%m.%Y'),
                                res.nights,
                                res.price,
                                res.guest.username,
                                res.status,
                                res.host.username])
            print(tabulate(lst, headers=['ID', 'ID sobe', 'Datum', 'Nocenja', 'Cena', 'Gost', 'Status',
                                         'Domacin'],
                           tablefmt='fancy_grid'))

    @classmethod
    def report_reshost(cls):
        while 1:
            user_in = input('Unesite username domacina ili "x" za kraj: ')
            if user_in == 'x':
                break
            if user_in not in User.all.keys():
                print('username ne postoji')
                continue
            else:
                if User.all[user_in].role != 'host':
                    print('Korisnik nema status domacina! ')
                    continue
                else:
                    lst = []
                    for it in cls.all.keys():
                        res = cls.all[it]
                        if res.status == 'Zavrsena' and Room.all[res.room_idd].host.username == user_in:
                            lst.append([res.reservation_id, res.room_idd,
                                        res.cin_cout[0].strftime('%d.%m.%Y-') +
                                        res.cin_cout[1].strftime('%d.%m.%Y'),
                                        res.nights,
                                        res.price,
                                        res.guest.username,
                                        res.status,
                                        res.host.username])
                    print(tabulate(lst, headers=['ID', 'ID sobe', 'Datum', 'Nocenja', 'Cena', 'Gost', 'Status',
                                                 'Domacin'],
                                   tablefmt='fancy_grid'))

    @classmethod
    def report_yearhost(cls):
        lst = []
        pastyear = cls.today - timedelta(days=365)
        for it in User.all.keys():
            if User.all[it].role == 'host':
                res_num = 0
                earned = 0
                for i in cls.all.keys():
                    if cls.all[i].host.username == User.all[it].username and (
                            cls.today >= cls.all[i].cin_cout[1] and cls.all[i].cin_cout[0]
                            >= pastyear) and cls.all[i].status == 'Zavrsena':
                        res_num += 1
                        earned += float(Reservation.all[i].price) * int(Reservation.all[i].nights)
                lst.append([User.all[it].username, str(res_num), str(earned)])
        print(tabulate(lst, headers=['username', 'Broj rezervacija', 'Zarada'], tablefmt='fancy_grid'))

    @classmethod
    def report_monthhost(cls):
        lst = []
        pastmonth = cls.today - timedelta(days=30)
        for it in User.all.keys():
            if User.all[it].role == 'host':
                res_num = 0
                earned = 0
                for i in cls.all.keys():
                    if cls.all[i].host.username == User.all[it].username and (
                            cls.today >= cls.all[i].cin_cout[1] and cls.all[i].cin_cout[0]
                            >= pastmonth) and cls.all[i].status == 'Zavrsena':
                        res_num += 1
                        earned += float(Reservation.all[i].price) * int(Reservation.all[i].nights)
                lst.append([User.all[it].username, str(res_num), str(earned)])
        print(tabulate(lst, headers=['username', 'Broj rezervacija', 'Zarada'], tablefmt='fancy_grid'))
        pass

    @classmethod
    def report_resnum(cls):
        while 1:
            user_in = input('Unesite dan rezervacije (dd.mm.yyyy) ili "x" za kraj: ')
            if user_in == 'x':
                break
            date = cls.date_convert(user_in)
            if not date:
                continue
            user_in = input('Unesite username domacina ili "x" za kraj: ')
            if user_in == 'x':
                break
            if user_in not in User.all.keys():
                print('username ne postoji')
                continue
            else:
                if User.all[user_in].role != 'host':
                    print('Korisnik nema status domacina! ')
                    continue
                else:
                    res_num = 0
                    price = 0
                    for it in cls.all.keys():
                        res = cls.all[it]
                        if res.status == 'Zavrsena' and res.cin_cout[0] <= date <= res.cin_cout[1] \
                                and res.host.username == user_in:
                            res_num += 1
                            price += res.price
                    print(tabulate([[res_num, price]], headers=['Broj rezervacija', 'Cena'], tablefmt='fancy_grid'))
                    return

    @classmethod
    def report_city(cls):
        city = {}
        res_number = 0
        for it in cls.all.keys():
            res = cls.all[it]
            if res.status == 'Zavrsena':
                res_number += 1
                if Room.all[res.room_idd].adress[2] not in city.keys():
                    city[Room.all[res.room_idd].adress[2]] = 1
                else:
                    city[Room.all[res.room_idd].adress[2]] += 1
        lst = []
        for it in city.keys():
            percent = round(city[it] * 100 / res_number, 1)
            lst.append([it, f'{city[it]}/{res_number}', f'{percent}%'])
        print(tabulate(lst, headers=['Grad', 'Rezervacije', '%'], tablefmt='fancy_grid'))

    @classmethod
    def decline(cls):
        for res in cls.all.keys():
            gst = cls.all[res].guest.username
            if User.all[gst].blocked:
                cls.all[res].status = 'Odbijena'

    @classmethod
    def save_to_file(cls):
        cls.reservations_file.truncate(0)
        cls.reservations_file.seek(0)
        cls.reservations_file.write(
            'room_id|cin-cout|nights|price|guest|status|aditional_guests|reservation_id|host\n')
        for res in cls.all.keys():
            reservation = cls.all[res]
            date = reservation.cin_cout[0]
            cdate = reservation.cin_cout[1]
            cls.reservations_file.write(
                f'{reservation.room_idd}|{date.strftime("%d.%m.%Y") + "-" + cdate.strftime("%d.%m.%Y")}|'
                f'{reservation.nights}|'
                f'{str(reservation.price)}|{reservation.guest.username}|'
                f'{reservation.status}|{",".join(reservation.aditional_guests)}|{reservation.reservation_id}|'
                f'{reservation.host.username}\n')
        return
