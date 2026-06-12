import json
import os

def wczytaj_dane_json(sciezka_pliku):
   
    if not os.path.exists(sciezka_pliku):
        return {}
        
    try:
        with open(sciezka_pliku, 'r', encoding='utf-8') as plik:
            return json.load(plik)
    except Exception as e:
        print(f"Błąd wczytywania pliku {sciezka_pliku}: {e}")
        return {}

def zapisz_dane_json(sciezka_pliku, dane_do_zapisu):
    
    try:
        with open(sciezka_pliku, 'w', encoding='utf-8') as plik:
            json.dump(dane_do_zapisu, plik, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Błąd zapisywania do pliku {sciezka_pliku}: {e}")
        return False