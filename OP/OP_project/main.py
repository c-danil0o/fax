from user import User
# from reservation import Reservation
from room_res import Room, Reservation
import os

f1 = open('db/users.txt', 'r+')
f2 = open('db/passwords.txt', 'r+')
f3 = open('db/rooms.txt', 'r+')
f4 = open('db/amenities.txt', 'r+')
f5 = open('db/reservations.txt', 'r+')
User.loadfiles(f1, f2)
User.load_users()
Room.load_files(f3, f4)
Reservation.load_files(f5)
Room.load_amenities()
Room.load_rooms()
Reservation.load_reservations()


def welcome():
    # cls()          ne radi u pycharm
    print('{:-^50s}'.format('-'), end='\n\n')
    print('{:^50s}'.format('Dobrodosli u airBNB!'), end='\n\n')
    # cls()
    options = ['1', '2', '3', '4', '5', '6', '7']
    while 1:
        print('{:-^50s}'.format('-'), end='\n')
        print('{0: <50s}\n{1:50s}\n{2:50s}\n{3:50s}\n{4:50s}\n{5:50s}\n{6:50s}'.format('1. Prijava',
                                                                                       '2. Registracija',
                                                                                       '3. Pregled apartmana',
                                                                                       '4. Pretraga apartmana',
                                                                                       '5. Visekriterijumska pretraga '
                                                                                       'apartmana',
                                                                                       '6. 10 najpopularnijih gradova',
                                                                                       '7. Izlaz'), end='\n')
        print('{:-^50s}'.format('-'))
        option = input('unesite opciju: ')
        if option not in options:
            continue
        if option == '1':
            User.login()
            menu()
        elif option == '2':
            User.register('guest')
        elif option == '3':
            Room.print_rooms('aktivan')
        elif option == '4':
            while Room.search():
                pass
        elif option == '5':
            print(Room.multi_search())
        elif option == '6':
            Reservation.top10()
        elif option == '7':
            app_exit()


def menu():
    while 1:
        if User.logged.role == 'admin':
            print('Admin Menu')
            print('{:-^50s}'.format('-'), end='\n')
            print('1. Pregled apartmana')
            print('2. Pretraga apartmana')
            print('3. Visekriterijumska pretraga apartmana')
            print('4. Pretraga rezervacija')
            print('5. Registracija novih domacina')
            print('6. Kreiranje dodatne opreme')
            print('7. Brisanje dodatne opreme')
            print('8. Blokiranje korisnika')
            print('9. Izvestaji')
            print('10. Top 10 gradova')
            print('11. Odjava')
            print('{:-^50s}'.format('-'))
            while 1:
                user_in = input('unesite opciju: ')
                if user_in == '1':
                    Room.print_rooms('all')
                    break
                elif user_in == '2':
                    Room.search()
                    break
                elif user_in == '3':
                    Room.multi_search()
                    break
                elif user_in == '4':
                    Reservation.search_reservations()
                    break
                elif user_in == '5':
                    User.register('host')
                    break
                elif user_in == '6':
                    Room.add_amenities()
                    break
                elif user_in == '7':
                    Room.remove_amenities()
                    break
                elif user_in == '8':
                    User.block_user()
                    Reservation.decline()
                    Room.decline()
                    break
                elif user_in == '9':
                    while 1:
                        print(
                            'Generisanje izvestaja! \n a) potvrdjene rezervacije za izabrani dan\n '
                            'b) potvrdjene rezervacije za izabranog domacina\n '
                            'c) godisnji pregled angazovanja domacina\n '
                            'd) mesecni pregled angazovanja domacina\n '
                            'e) ukupan broj i cena rezervacija\n '
                            'f) zastupljenost gradova\n '
                            'g) izlaz\n')
                        user_in = input('unesite opciju: ')
                        if user_in == 'a':
                            Reservation.report_resday()
                        elif user_in == 'b':
                            Reservation.report_reshost()
                        elif user_in == 'c':
                            Reservation.report_yearhost()
                        elif user_in == 'd':
                            Reservation.report_monthhost()
                        elif user_in == 'e':
                            Reservation.report_resnum()
                        elif user_in == 'f':
                            Reservation.report_city()
                        elif user_in == 'g':
                            break
                        else:
                            continue
                    break
                elif user_in == '10':
                    Reservation.top10()
                    break
                elif user_in == '11':
                    User.logged = None
                    welcome()

        elif User.logged.role == 'guest':
            print('Guest Menu:')
            print('{:-^50s}'.format('-'), end='\n')
            print('1. Pregled apartmana')
            print('2. Pretraga apartmana')
            print('3. Visekriterijumska pretraga apartmana')
            print('4. Pregled vasih rezervacija')
            print('5. Nova rezervacija')
            print('6. Ponistavanje rezervacije')
            print('7. Top 10 gradova')
            print('8. Odjava')
            print('{:-^50s}'.format('-'), end='\n')
            while 1:
                user_in = input('unesite zeljenu opciju:  ')
                if user_in == '1':
                    Room.print_rooms('aktivan')
                    break
                elif user_in == '2':
                    Room.search()
                    break
                elif user_in == '3':
                    Room.multi_search()
                    break
                elif user_in == '4':
                    Reservation.print_reservations(User.logged)
                    break
                elif user_in == '5':
                    Reservation.make_reservation(User.logged)
                    break
                elif user_in == '6':
                    Reservation.cancel_reservation(User.logged)
                    break
                elif user_in == '7':
                    Reservation.top10()
                    break
                elif user_in == '8':
                    User.logged = None
                    welcome()

        elif User.logged.role == 'host':
            print('Host menu: ')
            print('{:-^50s}'.format('-'), end='\n')
            print('1. Pregled apartmana')
            print('2. Pretraga apartmana')
            print('3. Visekriterijumska pretraga apartmana')
            print('4. Pregled vasih apartmana')
            print('5. Dodavanje apartmana')
            print('6. Izmena apartmana')
            print('7. Brisanje apartmana')
            print('8. Pregled rezervacija')
            print('9. Potvrda i odbijanje rezervacija')
            print('10. Top 10 gradova')
            print('11. Odjava')
            print('{:-^50s}'.format('-'), end='\n')
            while 1:
                user_in = input('unesite zeljenu opciju:  ')
                if user_in == '1':
                    Room.print_rooms('all')
                    break
                elif user_in == '2':
                    Room.search()
                    break
                elif user_in == '3':
                    Room.multi_search()
                    break
                elif user_in == '4':
                    Room.print_rooms('all', User.logged)
                    break
                elif user_in == '5':
                    Room.add_room()
                    break
                elif user_in == '6':
                    Room.manage_room()
                    break
                elif user_in == '7':
                    Room.delete_room()
                    break
                elif user_in == '8':
                    Reservation.print_reservations(User.logged)
                    break
                elif user_in == '9':
                    Reservation.approve_reservation(User.logged)
                    break
                elif user_in == '10':
                    Reservation.top10()
                    break
                elif user_in == '11':
                    User.logged = None
                    welcome()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def app_exit():
    Room.save_to_file()
    User.save_to_file()
    Reservation.save_to_file()
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    exit(0)


def main():
    welcome()


if __name__ == '__main__':
    main()
