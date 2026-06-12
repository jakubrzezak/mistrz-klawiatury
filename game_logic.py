import random
import data_manager

def pobierz_talie_slow(poziom):
    baza = data_manager.wczytaj_dane_json('words.json')
    if poziom not in baza:
        poziom = 'latwy'
        
    talia = baza[poziom].copy()
    random.shuffle(talia)
    return talia

def wymieszaj_litery(slowo):
    litery = list(slowo)
    random.shuffle(litery)
    pomieszane = "".join(litery)
    while pomieszane == slowo and len(slowo) > 1:
        random.shuffle(litery)
        pomieszane = "".join(litery)
    return pomieszane

def sprawdz_wpis(prawidlowe, wpisane):
    return prawidlowe.strip().lower() == wpisane.strip().lower()

def aktualizuj_statystyki_i_sprawdz_questy(czy_poprawne, czas_sekundy, poziom, tryb, czy_koniec_gry=False):
    stats = data_manager.wczytaj_dane_json('stats.json')
    questy_baza = data_manager.wczytaj_dane_json('quests.json')
    
    
    if czy_koniec_gry:
        stats['rozegrane_gry'] = stats.get('rozegrane_gry', 0) + 1
    else:
        stats['wpisane_slowa_ogolem'] = stats.get('wpisane_slowa_ogolem', 0) + 1
        
        if czy_poprawne:
            stats['poprawne_slowa'] = stats.get('poprawne_slowa', 0) + 1
            stats['aktualna_seria_bez_bledu'] = stats.get('aktualna_seria_bez_bledu', 0) + 1
            
            if stats['aktualna_seria_bez_bledu'] > stats.get('najlepsza_seria_bez_bledu', 0):
                stats['najlepsza_seria_bez_bledu'] = stats['aktualna_seria_bez_bledu']
                
            if tryb == 'rozsypanka':
                stats['poprawne_rozsypanka'] = stats.get('poprawne_rozsypanka', 0) + 1
            elif poziom == 'latwy':
                stats['poprawne_latwe'] = stats.get('poprawne_latwe', 0) + 1
            elif poziom == 'sredni':
                stats['poprawne_srednie'] = stats.get('poprawne_srednie', 0) + 1
            elif poziom == 'trudny':
                stats['poprawne_trudne'] = stats.get('poprawne_trudne', 0) + 1
                
            if czas_sekundy > 0 and tryb != 'nauka':
                najlepszy_czas = stats.get('najlepszy_czas_slowa_sekundy', 99.0)
                if czas_sekundy < najlepszy_czas:
                    stats['najlepszy_czas_slowa_sekundy'] = czas_sekundy
        else:
            stats['bledne_slowa'] = stats.get('bledne_slowa', 0) + 1
            stats['aktualna_seria_bez_bledu'] = 0

    
    odblokowane_teraz = []
    lista_odblokowanych = stats.get('odblokowane_questy', [])
    
    
    warunki_questow = {
        "pierwsze_starcie": stats.get('rozegrane_gry', 0) >= 1,
        "rozgrzewka": stats.get('poprawne_latwe', 0) >= 30,
        "zloty_srodek": stats.get('poprawne_srednie', 0) >= 30,
        "twardziel": stats.get('poprawne_trudne', 0) >= 30,
        "mistrz_ortografii": stats.get('poprawne_slowa', 0) >= 50,
        "maszyna_do_pisania": stats.get('wpisane_slowa_ogolem', 0) >= 200,
        "niezatrzymany": stats.get('najlepsza_seria_bez_bledu', 0) >= 10,
        "perfekcjonista": stats.get('najlepsza_seria_bez_bledu', 0) >= 30,
        "szybki_bill": 0 < stats.get('najlepszy_czas_slowa_sekundy', 99.0) < 2.0,
        "flash": 0 < stats.get('najlepszy_czas_slowa_sekundy', 99.0) < 1.0,
        "wymiatacz": stats.get('poprawne_rozsypanka', 0) >= 10,
        "pan_chaosu": stats.get('poprawne_rozsypanka', 0) >= 30,
        "maratonczyk": stats.get('rozegrane_gry', 0) >= 20,
        "weteran": stats.get('rozegrane_gry', 0) >= 50,
        "tragiczny_pisarz": stats.get('bledne_slowa', 0) >= 30
    }
    
    
    for id_questa, warunek_spelniony in warunki_questow.items():
        if warunek_spelniony and id_questa not in lista_odblokowanych and id_questa in questy_baza:
            lista_odblokowanych.append(id_questa)
            odblokowane_teraz.append(questy_baza[id_questa]['nazwa'])
    
    
    stats['odblokowane_questy'] = lista_odblokowanych
    data_manager.zapisz_dane_json('stats.json', stats)
    
    return odblokowane_teraz
