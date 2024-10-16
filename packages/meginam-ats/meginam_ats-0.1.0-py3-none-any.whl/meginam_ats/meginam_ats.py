import datetime as dt
import os
import pickle

class Knyga:
    def __init__(self, pavadinimas, autorius, leidybos_metai, zanras):
        if not pavadinimas or not autorius or not leidybos_metai or not zanras:
            raise ValueError("Visi laukai privalo būti užpildyti")
        self.pavadinimas = pavadinimas
        self.autorius = autorius
        self.leidybos_metai = leidybos_metai
        self.zanras = zanras
        self.pasiskolinta = False
        self.grazinimo_data = None
        self.skaitytojas = None

    def __str__(self):
        return (f"Pavadinimas: {self.pavadinimas}, Autorius: {self.autorius}, "
                f"Leidimo metai: {self.leidybos_metai}, Žanras: {self.zanras}, "
                f"Pasiskolinta: {self.pasiskolinta}, Grazinimo data: {self.grazinimo_data}")

class Skaitytojas:
    def __init__(self, vardas, pavarde):
        if not vardas or not pavarde:
            raise ValueError("Visi laukai privalo būti užpildyti")
        self.vardas = vardas
        self.pavarde = pavarde
        self.pasiskolintos_knygos = []


            
    def pasiimti_knyga(self, knyga):
        self.pasiskolintos_knygos.append(knyga)
        print ("Knyga paiimta sekmingai!")




    def prideti_skaitytoja(self, vardas, pavarde):
        skaitytojas = Skaitytojas(vardas, pavarde)
        self.skaitytojai.append(skaitytojas)
        self.save_skaitytojai()
        print(f"Skaitytojas '{vardas} {pavarde}' pridėtas sėkmingai!")

class Biblioteka:
    def __init__(self):
        self.knygos = self.load_knygos()
        self.skaitytojai = self.load_skaitytojai()
        if self.skaitytojai is None:
            self.skaitytojai = []
            
            


    def load_knygos(self):
        try:
            with open("knygos.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def load_skaitytojai(self):
        try:
            with open("skaitytojai.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def save_knygos(self):
        with open("knygos.pkl", "wb") as f:
            pickle.dump(self.knygos, f)

    def save_skaitytojai(self):
        with open("skaitytojai.pkl", "wb") as f:
            pickle.dump(self.skaitytojai, f)

    def prideti_knyga(self, knyga):
        self.knygos.append(knyga)
        self.save_knygos()
        print(f"Knyga '{knyga.pavadinimas}' įtraukta sėkmingai!")

    def ieskoti_knygos(self, pavadinimas_arba_autorius):
        rezultatai = []
        pavadinimas_arba_autorius = pavadinimas_arba_autorius.lower()
        for knyga in self.knygos:
            if pavadinimas_arba_autorius in knyga.pavadinimas.lower() or pavadinimas_arba_autorius in knyga.autorius.lower():
                rezultatai.append(knyga)
        if len(rezultatai) == 1:
            return rezultatai[0]
        elif len(rezultatai) > 1:
            return rezultatai
        else:
            return None

    def istrinti_knyga(self, knyga):
        if knyga in self.knygos:
            self.knygos.remove(knyga)
            self.save_knygos()
            print(f"Knyga '{knyga.pavadinimas}' pašalinta sėkmingai!")
        else:
            print(f"Knyga '{knyga.pavadinimas}' nerasta!")

    def rasti_knyga(self, pavadinimas):
        for knyga in self.knygos:
            if knyga.pavadinimas == pavadinimas:
                return knyga
        return None
    def paskolinti_knyga(self, pavadinimas, vardas, pavarde):
        skaitytojas = self.rasti_skaitytoja(vardas, pavarde)
        if skaitytojas is None:
            skaitytojas = Skaitytojas(vardas, pavarde)
            self.skaitytojai.append(skaitytojas)
            self.save_skaitytojai()
            print(f"Skaitytojas '{vardas} {pavarde}' pridėtas sėkmingai!")

        knyga = self.ieskoti_knygos(pavadinimas)
        if knyga is not None:
            if isinstance(knyga, list):
                if len(knyga) == 1:
                    knyga = knyga[0]
                else:
                    print("Rasta daugiau nei viena knyga. Prašome pasirinkti vieną knygą.")
                    return
            if knyga.pasiskolinta:
                print(f"Knyga '{knyga.pavadinimas}' jau yra paskolinta kitam skaitytojui.")
            else:
                veluojancios_knygos = [knyga for knyga in skaitytojas.pasiskolintos_knygos if knyga.grazinimo_data and knyga.grazinimo_data < dt.date.today()]
                if veluojancios_knygos:
                    print(f"Skaitytojas '{vardas} {pavarde}' turi veluojančių knygų. Prieš paskolinti naują knygą, reikia grąžinti veluojančias knygas.")
                elif len(skaitytojas.pasiskolintos_knygos) >= 5:
                    print(f"Skaitytojas '{vardas} {pavarde}' jau turi maksimalią leidžiamą knygų skaičių.")
                else:
                    knyga.pasiskolinta = True
                    knyga.grazinimo_data = dt.datetime.now() + dt.timedelta(days=10)
                    skaitytojas.pasiimti_knyga(knyga)
        else:
            print(f"Knyga '{pavadinimas}' nerasta!")
    def grazinti_knyga(self, pavadinimas, vardas, pavarde):
        for knyga in self.knygos:
            if knyga.pavadinimas == pavadinimas:
                if knyga.pasiskolinta:
                    knyga.pasiskolinta = False
                    knyga.grazinimo_data = None
                    knyga.skaitytojas = None
                    skaitytojas = self.rasti_skaitytoja(vardas, pavarde)
                    if skaitytojas:
                        skaitytojas.pasiskolintos_knygos.remove(knyga)
                        self.save_skaitytojai()
                        print(f"Knyga '{knyga.pavadinimas}' grąžinta sėkmingai!")
                    else:
                        print(f"Skaitytojas '{vardas} {pavarde}' nerastas!")
                else:
                    print("Knyga nėra paskolinta.")
                return

        print(f"Knyga '{pavadinimas}' nerasta!")

    def rasti_skaitytoja(self, vardas, pavarde):
        for skaitytojas in self.skaitytojai:
            if skaitytojas.vardas == vardas and skaitytojas.pavarde == pavarde:
                return skaitytojas
        return None

    def rasti_skaitytojus_su_skolomis(self):
        skaitytojai_su_skolomis = [skaitytojas for skaitytojas in self.skaitytojai if skaitytojas.pasiskolintos_knygos]
        if skaitytojai_su_skolomis:
            print("Skaitytojai su skolomis:")
            for skaitytojas in skaitytojai_su_skolomis:
                veluojancios_knygos = [knyga for knyga in skaitytojas.pasiskolintos_knygos if knyga.grazinimo_data and knyga.grazinimo_data < dt.date.today()]
                if veluojancios_knygos:
                    print(f"{skaitytojas.vardas} {skaitytojas.pavarde}:")
                    for knyga in veluojancios_knygos:
                        print(f"  - {knyga.pavadinimas} (veluoja grąžinti nuo {knyga.grazinimo_data})")
        else:
            print("Nėra skaitytojų su skolomis.")


def naudotojo_funkcija():
    biblioteka = Biblioteka()       
    while True:
        print("Bibliotekos valdymo sistema")
        print("1. Įtraukti knygą")
        print("2. Pašalinti seną knygą")
        print("3. Pasiimti knygą išsinešimui ")
        print("4. Ieškoti knygos")
        print("5. Rodyti visas knygas")
        print("6. Peržiūrėti visas vėluojančias knygas")
        print("7 Baigti darbą")
        print("8 Visi skaitytojai")
        pasirinkimas = input("Įveskite savo pasirinkimą: ")
        if pasirinkimas == "1":
            try:
                pavadinimas = input("Įveskite knygos pavadinimą: ")
                autorius = input("Įveskite knygos autorių: ")
                leidybos_metai = int(input("Įveskite leidybos metus: "))
                zanras = input(" Įveskite žanrą: ")
                knyga = Knyga(pavadinimas, autorius, leidybos_metai, zanras)
                biblioteka.prideti_knyga(knyga)
            except ValueError as e:
                    print(f"Klaida: {e}")

        elif pasirinkimas == "2":
            try:
                knyga_pavadinimas = str(input("Įveskite knygos pavadinimą kuria norite Ištrinti "))
                for knyga in biblioteka.knygos:
                    if knyga.pavadinimas == knyga_pavadinimas:
                         biblioteka.istrinti_knyga(knyga)
                         break
                else:
                        print(f"Knyga '{knyga_pavadinimas}' nerasta!")
            except Exception as e:
                        print(f"Klaida: {e}")

        elif pasirinkimas == "3":
            try:
                pavadinimas = input("Įveskite knygos pavadinimą: ")
                vardas = input("Įveskite skaitytojo vardą: ")
                pavarde = input("Įveskite skaitytojo pavardę: ")
                biblioteka.paskolinti_knyga(pavadinimas, vardas, pavarde)
            except Exception as e:
                print(f"Klaida: {e}")
                
        elif pasirinkimas == "4":
                    try:
                        pavadinimas_arba_autorius = input("Įveskite knygos pavadinimą arba autorių: ")
                        rezultatai = biblioteka.ieskoti_knygos(pavadinimas_arba_autorius)
                        if rezultatai is not None:
                            if isinstance(rezultatai, list):
                                for knyga in rezultatai:
                                    print(knyga)
                            else:
                                print(rezultatai)
                        else:
                            print(f"Knyga '{pavadinimas_arba_autorius}' nerasta!")
                    except Exception as e:
                        print(f"Klaida: {e}")

        elif pasirinkimas == "5":
            try:
                print("Visos knygos:")
                for i, knyga in enumerate(biblioteka.knygos, start=1):
                    if knyga.pasiskolinta:
                        skaitytojas = next((s for s in biblioteka.skaitytojai if knyga in s.pasiskolintos_knygos), None)
                        if skaitytojas:
                             print(f"{i}. Pavadinimas: {knyga.pavadinimas}, Autorius: {knyga.autorius}, Leidimo metai: {knyga.leidybos_metai}, Žanras: {knyga.zanras}, Pasiskolinta: {knyga.pasiskolinta}, Grazinimo data: {knyga.grazinimo_data}, Skaitytojas: {skaitytojas.vardas} {skaitytojas.pavarde}")
                        else:
                            print(f"{i}. Pavadinimas: {knyga.pavadinimas}, Autorius: {knyga.autorius}, Leidimo metai: {knyga.leidybos_metai}, Žanras: {knyga.zanras}, Pasiskolinta: {knyga.pasiskolinta}, Grazinimo data: {knyga.grazinimo_data}")
                    else:
                        print(f"{i}. Pavadinimas: {knyga.pavadinimas}, Autorius: {knyga.autorius}, Leidimo metai: {knyga.leidybos_metai}, Žanras: {knyga.zanras}, Pasiskolinta: {knyga.pasiskolinta}, Grazinimo data: {knyga.grazinimo_data}")
            except Exception as e:
                    print(f"Klaida: {e}")

        elif pasirinkimas == "6":
            try:
                biblioteka.rasti_skaitytojus_su_skolomis()
            except Exception as e:
                print(f"Klaida: {e}")

        elif pasirinkimas == "7":
            try:
                biblioteka.save_knygos()
                biblioteka.save_skaitytojai()
                print("Biblioteka uždaryta!")
                break
            except Exception as e:
                print(f"Klaida: {e}")
                
        elif pasirinkimas == "8":
            try:
                print("Visi skaitytojai:")
                for i, skaitytojas in enumerate(biblioteka.skaitytojai, start=1):
                    print(f"{i}. Vardas: {skaitytojas.vardas}, Pavardė: {skaitytojas.pavarde}")
                skaitytojo_numeris = int(input("Įveskite skaitytojo numerį, kurį norite ištrinti: "))
                if skaitytojo_numeris > 0 and skaitytojo_numeris <= len(biblioteka.skaitytojai):
                    skaitytojas = biblioteka.skaitytojai[skaitytojo_numeris - 1]
                    print("Skaitytojas yra pasiskolintas šias knygas:")
                    for knyga in skaitytojas.pasiskolintos_knygos:
                        print(f"- {knyga.pavadinimas}")
                    biblioteka.skaitytojai.remove(skaitytojas)
                    biblioteka.save_skaitytojai()
                    print(f"Skaitytojas '{skaitytojas.vardas} {skaitytojas.pavarde}' ištrintas sėkmingai!")
                    for knyga in skaitytojas.pasiskolintos_knygos:
                        knyga.pasiskolinta = False
                        knyga.grazinimo_data = None
                        biblioteka.save_knygos()
                    print("Visos skolintos knygos ištrintos sėkmingai!")
                else:
                    print("Neteisingas skaitytojo numeris.")
            except Exception as e:
                print(f"Klaida: {e}")
        elif pasirinkimas == "9":
            try:
                biblioteka.save_knygos()
                biblioteka.save_skaitytojai()
                print("Biblioteka uždaryta!")
                break
            except Exception as e:
                 print(f"Klaida: {e}")

if __name__ == "__main__":           
    naudotojo_funkcija()