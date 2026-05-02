# Postęp projektu — klasyfikator FHE (grzyby)

Śledzenie zadań względem [requirements.md](./requirements.md) i [temat.md](./temat.md).  
Zaznaczaj `- [x]` po ukończeniu pozycji.

---

## Plan na 3 tygodnie (checkboxy)

### Tydzień 1 — Dane, baseline, struktura

- [ ] Repozytorium: struktura modułów (dane, model, krypto, predykcja, benchmark zgodnie z NFR-03)
- [ ] `requirements.txt` / `pyproject.toml`, ustalenie Pythona 3.10+ i ziarna (`random_state = 42`, NFR-02)
- [ ] Pobranie zbioru UCI Secondary Mushroom (lub mirror), wczytanie (FR-01)
- [ ] Podział train/test, np. 80/20 (FR-02)
- [ ] Preprocessing: cechy numeryczne, skalowanie/standaryzacja, zapis parametrów dla nowych próbek (FR-03)
- [ ] One-hot (lub ustalone kodowanie) cech kategorycznych
- [ ] Trening modelu baseline w plaintext (regresja logistyczna / liniowy SVM — ML-01, FR-04)
- [ ] Metryki jawne: accuracy, precision, recall, F1, confusion matrix (FR-04)
- [ ] Eksport wag, biasu, parametrów skalowania pod inferencję FHE (FR-05)
- [ ] Krótki wpis w README: jak uruchomić trening

### Tydzień 2 — FHE: klucze, szyfrowanie, inferencja

- [ ] Wybór ścieżki: Concrete ML (start) i/lub TenSEAL + CKKS (bonus) — zgodnie z tematem
- [ ] Kontekst HE, klucz publiczny / prywatny — prywatny tylko po stronie „klienta” (FR-06, CR-02)
- [ ] Jawne parametry HE w kodzie i komentarz (CKKS: `poly_modulus_degree`, `coeff_mod_bit_sizes`, `global_scale` — CR-03)
- [ ] Szyfrowanie pojedynczej próbki (wektora cech) po preprocessingu (FR-07)
- [ ] Serwer: predykcja na ciphertextach bez deszyfracji wejścia (FR-08, CR-05)
- [ ] Serwer zwraca wynik w postaci zaszyfrowanej (score/logit) (FR-09)
- [ ] Klient: odszyfrowanie i próg decyzyjny (np. `score >= 0`) (FR-10)
- [ ] Porównanie predykcji encrypted vs plaintext na zbiorze testowym; zgodność ≥ 95% po dostrojeniu (FR-11, ML-04)
- [ ] Pomiar `absolute_error` score jawny vs po deszyfracji (CR-04)
- [ ] Rozdzielenie w kodzie: moduły klient vs serwer (brak secret key po stronie serwera)

### Tydzień 3 — Benchmarki, testy, raport, demo

- [ ] Pomiary czasu: predykcja plaintext, generowanie kluczy, szyfrowanie, inferencja FHE, deszyfracja, end-to-end (FR-12)
- [ ] Opcjonalnie: rozmiar ciphertextu, batch (z requirements — zakres rozszerzony)
- [ ] Tabele metryk i czasów; wykres plaintext vs encrypted (FR-13)
- [ ] Opis różnic numerycznych i przypadków brzegowych (granica decyzyjna — ML-05)
- [ ] Testy: szyfrowanie/deszyfracja ~zachowanie wartości; zgodność predykcji; brak użycia klucza prywatnego na serwerze; spójny preprocessing (FR-14)
- [ ] `pytest` w pipeline lub dokumentacja uruchomienia testów
- [ ] Proste uruchomienie: np. `python -m src.train`, `demo`, `benchmark` (NFR-01)
- [ ] README: architektura, eksperymenty, ograniczenia, disclaimer akademicki (NFR-04, NFR-05)
- [ ] CLI lub mini-demo (jak w temat.md — scenariusz „Encrypting sample… → Decrypted result”)
- [ ] Szkic raportu / slajdów na obronę

---

## Checklista ogólna (MVP vs requirements)

### Zakres podstawowy (MVP)

- [ ] Problem klasyfikacji binarnej (jadalny / trujący)
- [ ] Dane + baseline bez szyfrowania
- [ ] Prosty model (regresja logistyczna / liniowy)
- [ ] Szyfrowanie wejścia
- [ ] Predykcja na zaszyfrowanych danych
- [ ] Odszyfrowanie wyniku po stronie klienta
- [ ] Porównanie z modelem jawnym
- [ ] Pomiar czasu i narzutu szyfrowania

### Wymagania funkcjonalne (skrót)

- [ ] FR-01 — Wczytanie danych
- [ ] FR-02 — Podział danych
- [ ] FR-03 — Preprocessing + zapis parametrów
- [ ] FR-04 — Model baseline + metryki
- [ ] FR-05 — Eksport parametrów modelu pod FHE
- [ ] FR-06 — Generowanie kluczy (prywatny u klienta)
- [ ] FR-07 — Szyfrowanie próbki
- [ ] FR-08 — Predykcja na ciphertextach
- [ ] FR-09 — Zaszyfrowany wynik z serwera
- [ ] FR-10 — Deszyfracja i klasa po stronie klienta
- [ ] FR-11 — Porównanie z baseline
- [ ] FR-12 — Pomiar wydajności (czasy)
- [ ] FR-13 — Artefakty pod raport (tabele, wykresy, opis)
- [ ] FR-14 — Testy poprawności

### Kryptografia i ML (skrót)

- [ ] CR-01 — Schemat CKKS (lub uzasadnione odstępstwo w raporcie, jeśli Concrete ML)
- [ ] CR-02 — Rozdział ról kluczy
- [ ] CR-03 — Udokumentowane parametry HE
- [ ] CR-04 — Pomiar błędu score jawny vs po HE
- [ ] CR-05 — Serwer bez secret key, deszyfracja tylko u klienta
- [ ] ML-01 — Model prosty (liniowy)
- [ ] ML-02 — Wejście numeryczne i przeskalowane
- [ ] ML-03 — Baseline przed FHE
- [ ] ML-04 — Zgodność predykcji encrypted/plaintext ≥ 95%
- [ ] ML-05 — Opis rozjazdów numerycznych

### Niefunkcjonalne

- [ ] NFR-01 — Proste komendy uruchomienia
- [ ] NFR-02 — Powtarzalność (`random_state`)
- [ ] NFR-03 — Modułowa struktura kodu
- [ ] NFR-04 — README + dokumentacja
- [ ] NFR-05 — Jasny zakres demonstracyjny (nie produkcja)

### Opcjonalnie (zakres rozszerzony)

- [ ] Przybliżenie sigmoidy wielomianem / zaszyfrowane prawdopodobieństwo
- [ ] Batch prediction
- [ ] Web demo lub bogatszy CLI
- [ ] Porównanie TenSEAL vs Concrete ML
- [ ] One-vs-rest wieloklasa
- [ ] Eksperymenty z parametrami HE
- [ ] Wykresy czasu i dokładności

---

## Notatki (data / decyzje)

<!-- Tu możesz dopisywać krótkie wpisy, np. „2026-05-02: wybrano Concrete ML na start”. -->


