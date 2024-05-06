import math

class Mjerenje():
    def __init__(self, broj_mjerenja: int, napon: int, struja: float, snaga_kocnice: float, visokotlacna: float, niskotlacna: float, stvarni_moment: float, brzina_vrtnje: float, mehanicka_snaga: float, specificni_protok: float):
        self.napon_volt = napon
        self.struja_amper = struja
        self.snaga_kocnice_kilovat = snaga_kocnice
        self.tlak_u_visokotlacnoj_cijevi_bar = visokotlacna
        self.tlak_u_niskotlacnoj_cijevi_bar = niskotlacna
        self.stvarni_moment_njutnmetar = stvarni_moment
        self.brzina_vrtnje_u_minuti = brzina_vrtnje
        self.mehanicka_snaga_kilovat = mehanicka_snaga
        self.specificni_protok_litra_po_minuti = specificni_protok
        self.broj_mjerenja = broj_mjerenja

        self.tlak_u_visokotlacnoj_cijevi_paskal = self.tlak_u_visokotlacnoj_cijevi_bar * 10_000
        self.tlak_u_niskotlacnoj_cijevi_paskal = self.tlak_u_niskotlacnoj_cijevi_bar * 10_000
        self.brzina_vrtnje_herc = self.brzina_vrtnje_u_minuti / 60
        self.specificni_protok_metar_kubicni_po_sekundi = self.specificni_protok_litra_po_minuti / (1_000 * 60)

        self.pad_tlaka_bar = self.tlak_u_visokotlacnoj_cijevi_bar - self.tlak_u_niskotlacnoj_cijevi_bar
        self.pad_tlaka_paskal = self.tlak_u_visokotlacnoj_cijevi_paskal - self.tlak_u_niskotlacnoj_cijevi_paskal
        self.teorijski_moment_njutn_metar = teorijski_moment(self.specificni_protok_metar_kubicni_po_sekundi, self.pad_tlaka_paskal)

        self.teorijski_protok_metar_kubicni_po_sekundi = teorijski_protok(self.specificni_protok_metar_kubicni_po_sekundi, self.brzina_vrtnje_herc)

    def __str__(self):
        output = f"Mjerenje: {self.broj_mjerenja}\n"
        
        output += f"Specifični protok: {self.specificni_protok_metar_kubicni_po_sekundi} m3/s\n"
        output += f"Pad tlaka: {self.pad_tlaka_bar} bar\n"
        output += f"Brzina vrtnje: {self.brzina_vrtnje_herc} 1/s\n"
        output += f"Teorijski moment: {self.teorijski_moment_njutn_metar} Nm\n"
        output += f"Teorijski protok: {self.teorijski_protok_metar_kubicni_po_sekundi} m3/s\n"

        return output

def teorijski_protok(specificni_protok: float, brzina_vrtnje: float):
    return specificni_protok * brzina_vrtnje

def stvarni_protok(teorijski_protok: float, gubitak_protoka: float):
    return teorijski_protok + gubitak_protoka

def volumetricki_stupanj_iskoristivosti(teorijski_protok: float, stvarni_protok: float):
    return teorijski_protok / stvarni_protok

def teorijski_moment(specificni_protok: float, promjena_tlaka: float):
    return (specificni_protok * promjena_tlaka) / (2 * math.pi)

def stvarni_protok(teorijski_moment: float, gubitak_momenta: float):
    return teorijski_moment - gubitak_momenta

def hidromehanicki_stupanj_iskoristivosti(stvarni_moment: float, teorijski_moment: float):
    return stvarni_moment / teorijski_moment

def teorijska_snaga(teorijski_protok: float, pad_tlaka: float):
    return teorijski_protok * pad_tlaka

def hidraulicka_snaga(stvarni_protok: float, pad_tlaka: float):
    return stvarni_protok * pad_tlaka

def ukupni_stupanj_iskoristivosti(stvarna_mehanicka_snaga: float, hidraulicka_snaga: float):
    return stvarna_mehanicka_snaga / hidraulicka_snaga

def snaga_hidromotora_na_vratilu(stvarni_protok: float, pad_tlaka: float, ukupni_stupanj_iskoristivosti: float):
    return stvarni_protok * pad_tlaka * ukupni_stupanj_iskoristivosti