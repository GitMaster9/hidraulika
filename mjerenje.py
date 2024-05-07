import math

SPECIFICNI_PROTOK_KUBICNI_CENTIMETAR_PO_OKRETAJU = 51.5
SPECIFICNI_PROTOK_KUBICNI_METAR_PO_OKRETAJU = SPECIFICNI_PROTOK_KUBICNI_CENTIMETAR_PO_OKRETAJU / 1_000_000

class Mjerenje():
    def __init__(self, broj_mjerenja: int, napon: int, struja: float, snaga_kocnice: float, visokotlacna: float, niskotlacna: float, stvarni_moment: float, brzina_vrtnje: float, mehanicka_snaga_tablica: float, stvarni_protok: float):
        self.broj_mjerenja = broj_mjerenja
        self.napon_volt = napon
        self.struja_amper = struja
        self.snaga_kocnice_kilovat = snaga_kocnice
        self.tlak_u_visokotlacnoj_cijevi_bar = visokotlacna
        self.tlak_u_niskotlacnoj_cijevi_bar = niskotlacna
        self.stvarni_moment_njutn_metar = stvarni_moment
        self.brzina_vrtnje_u_minuti = brzina_vrtnje
        self.mehanicka_snaga_tablica_kilovat = mehanicka_snaga_tablica
        self.stvarni_protok_litra_po_minuti = stvarni_protok

        self.tlak_u_visokotlacnoj_cijevi_paskal = self.tlak_u_visokotlacnoj_cijevi_bar * 100_000
        self.tlak_u_niskotlacnoj_cijevi_paskal = self.tlak_u_niskotlacnoj_cijevi_bar * 100_000
        self.brzina_vrtnje_u_sekundi = self.brzina_vrtnje_u_minuti / 60
        self.specificni_protok_kubicni_metar_po_okretaju = SPECIFICNI_PROTOK_KUBICNI_METAR_PO_OKRETAJU
        self.specificni_protok_kubicni_metar_po_sekundi = self.specificni_protok_kubicni_metar_po_okretaju / self.brzina_vrtnje_u_sekundi
        self.stvarni_protok_kubicni_metar_po_sekundi = (self.stvarni_protok_litra_po_minuti / 1000) / 60

        self.pad_tlaka_bar = self.tlak_u_visokotlacnoj_cijevi_bar - self.tlak_u_niskotlacnoj_cijevi_bar
        self.pad_tlaka_paskal = self.tlak_u_visokotlacnoj_cijevi_paskal - self.tlak_u_niskotlacnoj_cijevi_paskal
        
        self.teorijski_moment_njutn_metar = teorijski_moment(self.specificni_protok_kubicni_metar_po_okretaju, self.pad_tlaka_paskal)
        self.hidromehanicki_stupanj_iskoristivosti = hidromehanicki_stupanj_iskoristivosti(self.stvarni_moment_njutn_metar, self.teorijski_moment_njutn_metar)

        self.teorijski_protok_kubicni_metar_po_sekundi = teorijski_protok(self.specificni_protok_kubicni_metar_po_okretaju, self.brzina_vrtnje_u_sekundi)
        self.teorijski_protok_litra_po_minuti = self.teorijski_protok_kubicni_metar_po_sekundi * 1000 * 60

        self.volumetricki_stupanj_iskoristivosti = volumetricki_stupanj_iskoristivosti(self.teorijski_protok_kubicni_metar_po_sekundi, self.stvarni_protok_kubicni_metar_po_sekundi)

        self.gubitak_protoka_kubicni_metar_po_sekundi = gubitak_protoka(self.stvarni_protok_kubicni_metar_po_sekundi, self.teorijski_protok_kubicni_metar_po_sekundi)
        self.gubitak_protoka_litra_po_minuti = self.gubitak_protoka_kubicni_metar_po_sekundi * 1000 * 60

        self.teorijska_snaga_vat = teorijska_snaga(self.teorijski_protok_kubicni_metar_po_sekundi, self.pad_tlaka_paskal)
        self.hidraulicka_snaga_vat = hidraulicka_snaga(self.stvarni_protok_kubicni_metar_po_sekundi, self.pad_tlaka_paskal)

        self.ukupni_stupanj_iskoristivosti = ukupni_stupanj_iskoristivosti_stupnjevi(self.volumetricki_stupanj_iskoristivosti, self.hidromehanicki_stupanj_iskoristivosti)

        self.mehanicka_snaga_kilovat = snaga_hidromotora_na_vratilu(self.stvarni_protok_kubicni_metar_po_sekundi, self.pad_tlaka_paskal, self.ukupni_stupanj_iskoristivosti)
        
    def __str__(self):
        output = f"Mjerenje: {self.broj_mjerenja}\n"
        
        output += f"Pad tlaka: {self.pad_tlaka_bar} bar\n"
        output += f"Brzina vrtnje: {self.brzina_vrtnje_u_sekundi} 1/s\n"

        output += "\n"
        
        output += f"Teorijski moment: {self.teorijski_moment_njutn_metar} Nm\n"
        output += f"Stvarni moment: {self.stvarni_moment_njutn_metar} Nm\n"
        output += f"Hidro-mehanički stupanj iskoristivosti: {self.hidromehanicki_stupanj_iskoristivosti}\n"

        output += "\n"
        
        output += f"Teorijski protok: {self.teorijski_protok_kubicni_metar_po_sekundi} m3/s\n"
        output += f"Teorijski protok: {self.teorijski_protok_litra_po_minuti} l/min\n"
        output += f"Stvarni protok: {self.stvarni_protok_kubicni_metar_po_sekundi} m3/s\n"
        output += f"Stvarni protok: {self.stvarni_protok_litra_po_minuti} l/min\n"
        output += f"Gubitak protoka: {self.gubitak_protoka_kubicni_metar_po_sekundi} m3/s\n"
        output += f"Gubitak protoka: {self.gubitak_protoka_litra_po_minuti} l/min\n"
        output += f"Volumetricki stupanj iskoristivosti: {self.volumetricki_stupanj_iskoristivosti}\n"
        
        output += "\n"

        output += f"Ukupni stupanj iskoristivosti: {self.ukupni_stupanj_iskoristivosti}\n"

        output += "\n"

        output += f"Teorijska snaga: {self.teorijska_snaga_vat} W\n"
        output += f"Hidraulička snaga: {self.hidraulicka_snaga_vat} W\n"
        output += f"Mehanička snaga: {self.mehanicka_snaga_kilovat} W\n"

        return output

def teorijski_protok(specificni_protok: float, brzina_vrtnje: float):
    return specificni_protok * brzina_vrtnje

def gubitak_protoka(stvarni_protok: float, teorijski_protok: float):
    return stvarni_protok - teorijski_protok

def stvarni_protok(teorijski_protok: float, gubitak_protoka: float):
    return teorijski_protok + gubitak_protoka

def volumetricki_stupanj_iskoristivosti(teorijski_protok: float, stvarni_protok: float):
    return teorijski_protok / stvarni_protok

def teorijski_moment(specificni_protok: float, pad_tlaka: float):
    return (specificni_protok * pad_tlaka) / (2 * math.pi)

def stvarni_protok(teorijski_moment: float, gubitak_momenta: float):
    return teorijski_moment - gubitak_momenta

def hidromehanicki_stupanj_iskoristivosti(stvarni_moment: float, teorijski_moment: float):
    return stvarni_moment / teorijski_moment

def teorijska_snaga(teorijski_protok: float, pad_tlaka: float):
    return teorijski_protok * pad_tlaka

def hidraulicka_snaga(stvarni_protok: float, pad_tlaka: float):
    return stvarni_protok * pad_tlaka

def ukupni_stupanj_iskoristivosti_snage(stvarna_mehanicka_snaga: float, hidraulicka_snaga: float):
    return stvarna_mehanicka_snaga / hidraulicka_snaga

def ukupni_stupanj_iskoristivosti_stupnjevi(volumetricki_stupanj_iskoristivosti: float, hidromehanicki_stupanj_iskoristivosti: float):
    return volumetricki_stupanj_iskoristivosti * hidromehanicki_stupanj_iskoristivosti

def ukupni_stupanj_iskoristivosti_sve(broj_okretaja: float, stvarni_moment: float, stvarni_protok: float, pad_tlaka: float):
    return (2 * math.pi * broj_okretaja * stvarni_moment) / (stvarni_protok * pad_tlaka)

def snaga_hidromotora_na_vratilu(stvarni_protok: float, pad_tlaka: float, ukupni_stupanj_iskoristivosti: float):
    return stvarni_protok * pad_tlaka * ukupni_stupanj_iskoristivosti