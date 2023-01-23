import sqlite3
import random

from cryptography.fernet import Fernet

conn = sqlite3.connect(r'C:\Users\Daniel\PycharmProjects\logowanie_dwuetapowe\users2.sqlite')
key = Fernet.generate_key()
fernet = Fernet(key)

c = conn.cursor()
c.execute('''DROP table IF EXISTS login''')
c.execute('''CREATE TABLE login
            (login TEXT, haslo TEXT, kod TEXT,UNIQUE(login))''')


def add_new_user():
    print("-------------------------")
    print("|      Rejestracja      |")
    print("-------------------------")
    login = input("Podaj Login: ")
    haslo = input("Podaj hasło: ")
    kod = str(random.randint(10000, 99999))
    haslo_h = fernet.encrypt(haslo.encode())
    kod_h = fernet.encrypt(kod.encode())
    query = "INSERT INTO login (login, haslo, kod) VALUES (?, ?, ?)"
    c.execute(query, (login, haslo_h, kod_h))
    conn.commit()
    print("Użytkownik dodany pomyślnie.")
    print("Twój unikalny kod logowania to: " + kod + " . Zapisz go gdzieś!")
    start()


def check_user(login, haslo, kod):
    query = 'SELECT * FROM login WHERE login = ?'
    x = c.execute(query, (login,))
    x = c.fetchone()
    check_login = x[0]
    check_haslo = x[1]
    check_haslo = fernet.decrypt(check_haslo)
    check_haslo = check_haslo.decode('utf-8')
    check_kod = x[2]
    check_kod = fernet.decrypt(check_kod)
    check_kod = check_kod.decode('utf-8')
    if login == check_login:
        print("Login poprawny......")
    else:
        print("Błąd")
        if haslo == check_haslo:
            print("Hasło poprawne......")
        else:
            print("Błąd")
            if kod == check_kod:
                print("Kod poprawny......")
                print("--------------------------")
                print("|    Jesteś zalogowany    |")
                print("--------------------------")
            else:
                print("Błąd")


def login():
    print("-------------------------")
    print("|       Logowanie       |")
    print("-------------------------")
    login = input("Podaj Login: ")
    haslo = input("Podaj hasło: ")
    kod = input("Podaj twój kod logowania: ")
    check_user(login, haslo, kod)
    start()


def start():
    print("1.Rejestracja.")
    print("2.Logowanie.")
    answer = input("Wybierz operację: ")

    if answer == "1":
        add_new_user()

    if answer == "2":
        login()


print("-------------------------")
print("|       LoginApp        |")
print("-------------------------")
start()
conn.commit()
conn.close()
