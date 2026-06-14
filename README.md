\# ⌨️ Mistrz Klawiatury



Mistrz Klawiatury to desktopowa aplikacja edukacyjna napisana w języku Python, wykorzystująca bibliotekę graficzną Tkinter. Celem gry jest poprawa szybkości i bezbłędności pisania na klawiaturze, z wykorzystaniem elementów rywalizacji (osiągnięcia, statystyki).



\## 🚀 Główne funkcjonalności



\* \*\*Trzy poziomy trudności:\*\* Łatwy, Średni oraz Trudny – dostosowane do poziomu zaawansowania gracza.

\* \*\*Tryb Nauka:\*\* Bezstresowy tryb bez ukrytego stopera, idealny do nauki układu klawiatury.

\* \*\*Tryb Rozsypanka (Anagramy):\*\* Tryb logiczny, w którym gracz musi ułożyć i poprawnie wpisać słowo z wymieszanych losowo liter.

\* \*\*System Osiągnięć (Questy):\*\* 15 unikalnych zadań nagradzających gracza za bicie rekordów czasowych, osiąganie serii bez błędów czy rozegranie odpowiedniej liczby gier.

\* \*\*Zaawansowane Statystyki:\*\* Aplikacja na żywo śledzi i zapisuje postępy gracza, w tym najlepszy czas, współczynnik poprawności oraz najdłuższą serię bez błędu.



\## 🏗️ Architektura Projektu



Projekt został zrealizowany z zachowaniem inżynierskich dobrych praktyk, dzieląc kod na niezależne moduły:



\* `main.py` – Główny punkt wejścia aplikacji.

\* `interface.py` – Warstwa prezentacji (Frontend) oparta na Tkinter.

\* `game\_logic.py` – Silnik gry (Backend) odpowiadający za walidację, tasowanie słów i przydzielanie nagród.

\* `data\_manager.py` – Moduł obsługujący bezpieczny odczyt i zapis danych.

\* `words.json`, `stats.json`, `quests.json` – Lokalne, bezserwerowe bazy danych.



\## 💻 Wymagania i Uruchomienie



Gra nie wymaga instalacji żadnych zewnętrznych bibliotek. Wykorzystuje wyłącznie standardową bibliotekę języka Python.



\*\*Wymagania:\*\*

\* Python 3.x lub nowszy



\*\*Instrukcja uruchomienia:\*\*

1\. Sklonuj repozytorium na swój komputer.

2\. Otwórz terminal w folderze projektu.

3\. Wykonaj polecenie:

&#x20;  ```bash

&#x20;  python main.py

