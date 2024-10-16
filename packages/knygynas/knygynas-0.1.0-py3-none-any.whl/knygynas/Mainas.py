
# import sys

# sys.path.insert(0, r'C:\Users\Silver\knygynas\Biblioteka')
import Biblioteka

# from Biblioteka import Biblioteka


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

            
naudotojo_funkcija()