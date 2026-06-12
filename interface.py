import tkinter as tk
from tkinter import messagebox
import time
import game_logic
import data_manager

class MistrzKlawiaturyUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mistrz Klawiatury")
        self.root.geometry("600x500")
        
        self.aktualny_poziom = ""
        self.aktualny_tryb = ""
        self.talia = []
        self.indeks_slowa = 0
        self.czas_startu = 0.0
        
        self.pokaz_menu_glowne()

    def wyczysc_okno(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def pokaz_menu_glowne(self):
        self.wyczysc_okno()
        
        tytul = tk.Label(self.root, text="Mistrz Klawiatury", font=("Helvetica", 24, "bold"))
        tytul.pack(pady=15)
        
        ramka_przyciski = tk.Frame(self.root)
        ramka_przyciski.pack(pady=10)
        
        tk.Button(ramka_przyciski, text="Łatwy", width=20, command=lambda: self.start_gry("latwy", "normalny")).grid(row=0, column=0, pady=5)
        tk.Button(ramka_przyciski, text="Średni", width=20, command=lambda: self.start_gry("sredni", "normalny")).grid(row=1, column=0, pady=5)
        tk.Button(ramka_przyciski, text="Trudny", width=20, command=lambda: self.start_gry("trudny", "normalny")).grid(row=2, column=0, pady=5)
        
        tk.Button(ramka_przyciski, text="Nauka (bez czasu)", width=20, bg="lightblue", command=lambda: self.start_gry("latwy", "nauka")).grid(row=3, column=0, pady=5)
        tk.Button(ramka_przyciski, text="Rozsypanka", width=20, bg="lightcoral", command=lambda: self.start_gry("latwy", "rozsypanka")).grid(row=4, column=0, pady=5)
        
        ramka_dolna = tk.Frame(self.root)
        ramka_dolna.pack(pady=15)

        tk.Button(ramka_dolna, text="📜 Zasady Gry", width=15, command=self.pokaz_zasady).grid(row=0, column=0, padx=5)
        tk.Button(ramka_dolna, text="📊 Statystyki", width=15, command=self.pokaz_statystyki).grid(row=0, column=1, padx=5)
        tk.Button(ramka_dolna, text="🏆 Questy", width=15, command=self.pokaz_questy).grid(row=0, column=2, padx=5)

    def pokaz_zasady(self):
        zasady = (
            "🎯 ZASADY GRY:\n\n"
            "1. Cel gry: Przepisuj poprawnie pojawiające się słowa najszybciej, jak potrafisz.\n"
            "2. Tryby trudności: Różnią się długością i skomplikowaniem słów.\n"
            "3. Tryb Nauka: Ćwiczysz bez włączonego stopera i bicia rekordów.\n"
            "4. Rozsypanka: Musisz odgadnąć i wpisać ukryte słowo z wymieszanych liter.\n"
            "5. Sterowanie: Zawsze zatwierdzaj wpisane słowo klawiszem ENTER.\n"
            "6. System Questów: Gra w tle nagradza Cię za dobrą passę lub bicie rekordów. Powodzenia!"
        )
        messagebox.showinfo("Zasady Gry", zasady)

    def pokaz_statystyki(self):
        stats = data_manager.wczytaj_dane_json('stats.json')
        
        czas = stats.get('najlepszy_czas_slowa_sekundy', 99.0)
        czas_tekst = f"{czas:.2f} s" if czas != 99.0 else "Brak rekordu"

        tekst = (
            "📊 TWOJE ŻYCIOWE STATYSTYKI:\n\n"
            f"Rozegrane pełne gry: {stats.get('rozegrane_gry', 0)}\n"
            f"Wpisane słowa ogółem: {stats.get('wpisane_slowa_ogolem', 0)}\n"
            f"✅ Poprawne słowa: {stats.get('poprawne_slowa', 0)}\n"
            f"❌ Błędne słowa: {stats.get('bledne_slowa', 0)}\n"
            f"🔥 Najlepsza seria bez błędu: {stats.get('najlepsza_seria_bez_bledu', 0)}\n"
            f"⏱️ Najlepszy czas słowa: {czas_tekst}\n\n"
            "Rozbicie na poziomy:\n"
            f"Łatwe: {stats.get('poprawne_latwe', 0)} | "
            f"Średnie: {stats.get('poprawne_srednie', 0)} | "
            f"Trudne: {stats.get('poprawne_trudne', 0)}\n"
            f"Rozsypanka: {stats.get('poprawne_rozsypanka', 0)}"
        )
        messagebox.showinfo("Statystyki", tekst)

    def pokaz_questy(self):
        stats = data_manager.wczytaj_dane_json('stats.json')
        questy = data_manager.wczytaj_dane_json('quests.json')
        odblokowane = stats.get("odblokowane_questy", [])
        
        opisy_questow = {
            "pierwsze_starcie": "Rozegraj swoją pierwszą grę",
            "rozgrzewka": "Wpisz poprawnie 30 łatwych słów",
            "zloty_srodek": "Wpisz poprawnie 30 średnich słów",
            "twardziel": "Wpisz poprawnie 30 trudnych słów",
            "mistrz_ortografii": "Wpisz poprawnie 50 słów",
            "maszyna_do_pisania": "Wpisz 200 słów ogółem",
            "niezatrzymany": "Osiągnij serię 10 słów bez błędu",
            "perfekcjonista": "Osiągnij serię 30 słów bez błędu",
            "szybki_bill": "Wpisz słowo w mniej niż 2 sekundy",
            "flash": "Wpisz słowo w mniej niż 1 sekundę",
            "wymiatacz": "Odgadnij 10 słów w Rozsypance",
            "pan_chaosu": "Odgadnij 30 słów w Rozsypance",
            "maratonczyk": "Rozegraj 20 pełnych gier",
            "weteran": "Rozegraj 50 pełnych gier",
            "tragiczny_pisarz": "Popełnij 30 błędów"
        }
        
        tekst = "🏆 TWOJE OSIĄGNIĘCIA:\n\n"
        for id_q, dane_q in questy.items():
            status = "✅" if id_q in odblokowane else "❌"
            opis = opisy_questow.get(id_q, "Ukryty wymóg")
            
            tekst += f"{status} {dane_q['nazwa']}\n      ➔ {opis}\n"
            
        messagebox.showinfo("Lista Questów", tekst)

    def start_gry(self, poziom, tryb):
        self.aktualny_poziom = poziom
        self.aktualny_tryb = tryb
        self.talia = game_logic.pobierz_talie_slow(poziom)
        self.indeks_slowa = 0
        
        self.wyczysc_okno()
        
        self.lbl_stoper = tk.Label(self.root, text="", font=("Helvetica", 14, "bold"), fg="blue")
        if tryb != "nauka":
            self.lbl_stoper.pack(pady=5)
            
        self.lbl_slowo = tk.Label(self.root, text="", font=("Helvetica", 20, "bold"))
        self.lbl_slowo.pack(pady=20)
        
        self.pole_wpisywania = tk.Entry(self.root, font=("Helvetica", 16), justify="center")
        self.pole_wpisywania.pack(pady=10)
        self.pole_wpisywania.bind("<Return>", self.sprawdz_odpowiedz)
        
        self.lbl_komunikat = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.lbl_komunikat.pack(pady=10)
        
        tk.Button(self.root, text="Exit", command=self.zakoncz_gre_awaryjnie, bg="red", fg="white").pack(side="bottom", pady=20)
        
        self.nastepne_slowo()
        
        if tryb != "nauka":
            self.aktualizuj_stoper()

    def aktualizuj_stoper(self):
        if hasattr(self, 'lbl_stoper') and self.lbl_stoper.winfo_exists():
            uplynelo = time.time() - self.czas_startu
            self.lbl_stoper.config(text=f"Czas: {uplynelo:.1f} s")
            self.root.after(100, self.aktualizuj_stoper)

    def nastepne_slowo(self):
        if self.indeks_slowa >= len(self.talia):
            self.zakoncz_runde_sukcesem()
            return
            
        slowo = self.talia[self.indeks_slowa]
        if self.aktualny_tryb == "rozsypanka":
            slowo = game_logic.wymieszaj_litery(slowo)
            
        self.lbl_slowo.config(text=slowo)
        self.pole_wpisywania.delete(0, tk.END)
        self.pole_wpisywania.focus()
        self.czas_startu = time.time()
        
    def sprawdz_odpowiedz(self, event):
        wpisane = self.pole_wpisywania.get()
        prawidlowe = self.talia[self.indeks_slowa]
        
        czas_wpisywania = time.time() - self.czas_startu
        
        czy_poprawne = game_logic.sprawdz_wpis(prawidlowe, wpisane)
        
        if czy_poprawne:
            self.lbl_komunikat.config(text="Dobrze!", fg="green")
        else:
            self.lbl_komunikat.config(text="Źle!", fg="red")
            
        zdobyte_questy = game_logic.aktualizuj_statystyki_i_sprawdz_questy(
            czy_poprawne, czas_wpisywania, self.aktualny_poziom, self.aktualny_tryb
        )
        
        for q in zdobyte_questy:
            messagebox.showinfo("🏆 Osiągnięcie!", f"Gratulacje!\nOdblokowano quest: {q}")
            
        self.indeks_slowa += 1
        self.root.after(500, lambda: self.lbl_komunikat.config(text=""))
        self.nastepne_slowo()
        
    def zakoncz_runde_sukcesem(self):
        game_logic.aktualizuj_statystyki_i_sprawdz_questy(False, 0, self.aktualny_poziom, self.aktualny_tryb, czy_koniec_gry=True)
        messagebox.showinfo("Koniec rundy", "Gratulacje! Przerobiłeś całą talię słów.")
        self.pokaz_menu_glowne()
        
    def zakoncz_gre_awaryjnie(self):
        self.pokaz_menu_glowne()