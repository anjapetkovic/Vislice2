import random
import json

STEVILO_DOVOLJENIH_NAPAK = 9
PRAVILNA_CRKA = "+"
PONOVLJENA_CRKA = "O"
VEC_KOT_CRKA = ">"
POSEBEN_ZNAK = "#"
NAPACNA_CRKA = "-"
ZMAGA = "W"
PORAZ = "X"
ZACETEK = "S"


class Igra:

    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        if crke is None:
            self.crke = []
        else:
            self.crke = crke

    def napacne_crke(self):
        return [crka for crka in self.crke if crka not in self.geslo]

    def pravilne_crke(self):
        return [crka for crka in self.crke if crka in self.geslo]

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def zmaga(self):
        return all(crka in self.crke for crka in self.geslo)

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK

    def pravilni_del_gesla(self):
        delni = ''
        for crka in self.geslo:
            if crka in self.crke:
                delni += crka + " "
            else:
                delni += '_ '
        return delni[:-1]

    def nepravilni_ugibi(self):
        return " ".join(self.napacne_crke())

    def ugibaj(self, ugib):
        if len(ugib) > 1 or len(ugib) == 0:
            return VEC_KOT_CRKA
        crka = ugib.upper()
        if crka not in 'ABCČDEFGHIJKLMNOPRSŠTUVZŽXYZWQĆĐ':
            return POSEBEN_ZNAK
        if crka in self.crke:
            return PONOVLJENA_CRKA
        else:
            self.crke.append(crka)

            if crka in self.geslo:
                if self.zmaga():
                    return ZMAGA
                else:
                    return PRAVILNA_CRKA
            else:
                if self.poraz():
                    return PORAZ
                else:
                    return NAPACNA_CRKA

    def stevilo_pravilnih_crk_s_ponovitvami(self):
        stevec = 0
        for crka in self.geslo:
            if crka in self.crke:
                stevec += 1
            else:
                pass
        return stevec



with open("besede.txt", "r", encoding="utf-8") as datoteka_z_besedami:
    bazen_besed = [vrstica.strip().upper() for vrstica in datoteka_z_besedami]


def nova_igra():
    return Igra(random.choice(bazen_besed))


class Vislice:

    def __init__(self, datoteka_s_stanjem, datoteka_z_besedami='besede.txt'):
        self.igre = {}
        self.datoteka_s_stanjem = datoteka_s_stanjem
        self.datoteka_z_besedami = datoteka_z_besedami

    def prost_id_igre(self):
        if len(self.igre) == 0:
            return 0
        else:
            return max(self.igre.keys()) + 1

    def nova_igra(self):
        self.nalozi_igre_iz_datoteke()
        with open(self.datoteka_z_besedami, 'r', encoding='utf-8') as f:
            bazen_besed = [vrstica.strip().upper() for vrstica in f]
        igra = Igra(random.choice(bazen_besed))
        id_igre = self.prost_id_igre()
        self.igre[id_igre] = (igra, ZACETEK)
        self.zapisi_igre_v_datoteko()
        return id_igre

    def ugibaj(self, id_igre, crka):
        self.nalozi_igre_iz_datoteke()
        igra, _ = self.igre[id_igre]
        poskus = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, poskus)
        self.zapisi_igre_v_datoteko()

    def zapisi_igre_v_datoteko(self):
        with open(self.datoteka_s_stanjem, 'w', encoding='utf-8') as f:
            igre1 = {id_igre: ((igra.geslo, igra.crke), poskus)
                     for id_igre, (igra, poskus) in self.igre.items()}
            json.dump(igre1, f)
        return

    def nalozi_igre_iz_datoteke(self):
        with open(self.datoteka_s_stanjem, 'r', encoding="utf-8") as f:
            igre = json.load(f)
            self.igre = {int(id_igre): (Igra(geslo, crke), poskus)
                         for id_igre, ((geslo, crke), poskus) in igre.items()}


def odstotek(stevec, imenovalec):
    return round((stevec / imenovalec) * 100)


def statistika(datoteka_s_stanjem):
    slovar_statistik = {}
    vislice = Vislice(datoteka_s_stanjem)
    vislice.nalozi_igre_iz_datoteke()

    stevilo_iger = len(vislice.igre.keys())
    slovar_statistik["stevilo_iger"] = stevilo_iger

    stevilo_zmag = sum([1 if poskus == ZMAGA else 0 for _, poskus in vislice.igre.values()])
    slovar_statistik["odstotek_zmag"] = odstotek(stevilo_zmag, stevilo_iger)

    stevilo_porazov = sum([1 if poskus == PORAZ else 0 for _, poskus in vislice.igre.values()])
    slovar_statistik["odstotek_porazov"] = odstotek(stevilo_porazov, stevilo_iger)

    stevilo_nedokoncnih_iger = stevilo_iger - stevilo_zmag - stevilo_porazov
    slovar_statistik["odstotek_nedokoncanih_iger"] = odstotek(stevilo_nedokoncnih_iger, stevilo_iger)

    najdaljse_uganjeno_geslo = max([igra.geslo if poskus == ZMAGA else "" for igra, poskus in vislice.igre.values()], key=len)
    slovar_statistik["najdaljse_uganjeno_geslo"] = najdaljse_uganjeno_geslo

    odstotki_uganjenih_crk = [odstotek(igra.stevilo_pravilnih_crk_s_ponovitvami(), len(igra.geslo)) for igra, _ in vislice.igre.values()]
    slovar_statistik["povprecen_odstotek_uganjenih_crk"] = "{0:.2f}".format(sum(odstotki_uganjenih_crk) / len(odstotki_uganjenih_crk))

    return slovar_statistik
