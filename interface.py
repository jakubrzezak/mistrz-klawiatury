import tkinter as tk
from tkinter import messagebox
import time
import game_logic
import data_manager

class MistrzKlawiaturyUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mistrz Klawiatury")
        self.root.geometry("600x400")
        
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
        tytul.pack(pady=20)
        
        ramka_przyciski = tk.Frame(self.root)
        ramka_przyciski.pack(pady=10)
        
        tk.Button(ramka_przyciski, text="Łatwy", width=20, command=lambda: self.start_gry("latwy", "normalny")).grid(row=0, column=0, pady=5)
        tk.Button(ramka_przyciski, text="Średni", width=20, command=lambda: self.start_gry("sredni", "normalny")).grid(row=1, column=0, pady=5)
        tk.Button(ramka_przyciski, text="Trudny", width=20, command=lambda: self.start_gry("trudny", "normalny")).grid(row=2, column=0, pady=5)
        
        tk.Button(ramka_przyciski, text="Nauka (bez czasu)", width=20, bg="lightblue", command=lambda: self.start_gry("latwy", "nauka")).grid(row=3, column=0, pady=5)
        tk.Button(ramka_przyciski, text="Rozsypanka", width=20, bg="lightcoral", command=lambda: self.start_gry("sredni", "rozsypanka")).grid(row=4, column=0, pady=5)
        
        tk.Button(self.root, text="🏆 Podgląd Questów", command=self.pokaz_questy).pack(pady=20)

    def pokaz_questy(self):
        stats = data_manager.wczytaj_dane_json('stats.json')
        questy = data_manager.wczytaj_dane_json('quests.json')
        odblokowane = stats.get("odblokowane_questy", [])
        
        tekst = "Twoje Osiągnięcia:\n\n"
        for id_q, dane_q in questy.items():
            status = "✅" if id_q in odblokowane else "❌"
            tekst += f"{status} {dane_q['nazwa']}\n"
            
        messagebox.showinfo("Lista Questów", tekst)

    def start_gry(self, poziom, tryb):
        self.aktualny_poziom = poziom
        self.aktualny_tryb = tryb
        self.talia = game_logic.pobierz_talie_slow(poziom)
        self.indeks_slowa = 0
        
        self.wyczysc_okno()
        
        # UI Ekranu Gry
        self.lbl_stoper = tk.Label(self.root, text="Czas leci! (Skup się)", font=("Helvetica", 12))
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