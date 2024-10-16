
import datetime as dt

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
