import json
import os
from datetime import datetime, timedelta

TIEDOSTO = "ruokakomero.json"

def lataa_tiedot():
    """Lataa tuotteet JSON-tiedostosta. Palauttaa tyhjän listan, jos tiedostoa ei ole."""
    if os.path.exists(TIEDOSTO):
        try:
            with open(TIEDOSTO, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Virhe: Tiedosto on vioittunut. Aloitetaan tyhjällä listalla.")
            return []
    return []

def tallenna_tiedot(tiedot):
    """Tallentaa tuotelistan JSON-tiedostoon."""
    with open(TIEDOSTO, "w", encoding="utf-8") as f:
        json.dump(tiedot, f, ensure_ascii=False, indent=4)

def pyyda_paivamaara():
    """Kysyy käyttäjältä päivämäärän ja tarkistaa sen oikeellisuuden."""
    while True:
        pvm_syote = input("Anna parasta ennen -päiväys (pp-kk-vvvv): ")
        try:
            # Yritetään jäsentää syöte datetime-olioksi
            datetime.strptime(pvm_syote, "%d-%m-%Y")
            return pvm_syote
        except ValueError:
            print("Virheellinen päivämäärämuoto! Käytä muotoa pp-kk-vvvv (esim. 31-12-2023).")

def lisaa_tuote(tiedot):
    """Lisää uuden tuotteen listalle ja tallentaa sen."""
    nimi = input("Anna tuotteen nimi: ").strip()
    if not nimi:
        print("Tuotteen nimi ei voi olla tyhjä.")
        return
    
    pvm = pyyda_paivamaara()
    
    tiedot.append({"nimi": nimi, "pvm": pvm})
    tallenna_tiedot(tiedot)
    print(f"Tuote '{nimi}' lisätty onnistuneesti!")

def jarjesta_tuotteet(tiedot):
    """Järjestää tuotteet aikajärjestykseen päivämäärän perusteella."""
    return sorted(tiedot, key=lambda x: datetime.strptime(x["pvm"], "%d-%m-%Y"))

def listaa_kaikki(tiedot):
    """Listaa kaikki tuotteet aikajärjestyksessä."""
    if not tiedot:
        print("Ruokakomero on tyhjä.")
        return

    jarjestetyt = jarjesta_tuotteet(tiedot)
    print("\n--- Kaikki tuotteet ---")
    for i, tuote in enumerate(jarjestetyt, 1):
        print(f"{i}. {tuote['nimi']} (Parasta ennen: {tuote['pvm']})")
    print("-----------------------")

def listaa_vanhenevat(tiedot):
    """Listaa tuotteet, jotka vanhenevat 3 päivän sisällä tai ovat jo vanhentuneet."""
    if not tiedot:
        print("Ruokakomero on tyhjä.")
        return

    tanaan = datetime.now()
    raja = tanaan + timedelta(days=3)
    loytyi = False

    print("\n--- Vanhenevat 3 päivän sisällä ---")
    jarjestetyt = jarjesta_tuotteet(tiedot)
    for tuote in jarjestetyt:
        tuotteen_pvm = datetime.strptime(tuote["pvm"], "%d-%m-%Y")
        
        if tuotteen_pvm <= raja:
            tila = "VANHENTUNUT!" if tuotteen_pvm < tanaan.replace(hour=0, minute=0, second=0, microsecond=0) else "Vanhenemassa"
            print(f"- {tuote['nimi']} ({tuote['pvm']}) [{tila}]")
            loytyi = True
            
    if not loytyi:
        print("Ei lähiaikoina vanhenevia tuotteita. Hienoa!")
    print("-----------------------------------")

def poista_tuote(tiedot):
    """Poistaa tuotteen listalta numeron perusteella."""
    listaa_kaikki(tiedot)
    if not tiedot:
        return

    try:
        valinta = int(input("\nAnna poistettavan tuotteen numero: "))
        if 1 <= valinta <= len(tiedot):
            jarjestetyt = jarjesta_tuotteet(tiedot)
            poistettava = jarjestetyt[valinta - 1]
            tiedot.remove(poistettava) # Poistetaan alkuperäisestä listasta
            tallenna_tiedot(tiedot)
            print(f"Tuote '{poistettava['nimi']}' poistettu.")
        else:
            print("Virheellinen numero.")
    except ValueError:
        print("Virhe: Syötä pelkkä numero.")

def paavalikko():
    """Sovelluksen pääsilmukka ja komentorivivalikko."""
    tiedot = lataa_tiedot()
    
    while True:
        print("\n=== RUOKAKOMEROAPULAINEN ===")
        print("1. Lisää tuote")
        print("2. Listaa kaikki tuotteet")
        print("3. Näytä pian vanhenevat (3 pv)")
        print("4. Poista tuote")
        print("0. Lopeta")
        
        valinta = input("Valitse toiminto (0-4): ")
        
        if valinta == '1':
            lisaa_tuote(tiedot)
        elif valinta == '2':
            listaa_kaikki(tiedot)
        elif valinta == '3':
            listaa_vanhenevat(tiedot)
        elif valinta == '4':
            poista_tuote(tiedot)
        elif valinta == '0':
            print("Näkemiin! Muista tarkistaa ruokakomero säännöllisesti.")
            break
        else:
            print("Tuntematon valinta, yritä uudelleen.")

if __name__ == "__main__":
    paavalikko()
