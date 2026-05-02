# Wybór tematu projektu: poufna klasyfikacja toksyczności grzybów (FHE)

## Tytuł roboczy

**Poufna klasyfikacja toksyczności grzybów z użyciem szyfrowania homomorficznego**

Alternatywnie (wariant „prezentacyjny”):

**Can I eat this? — homomorficzny klasyfikator jadalności grzybów bez ujawniania danych wejściowych**

W skrócie: **Encrypted Mushroom Toxicity Classifier** — klasyfikator binarny *jadalny / trujący* na cechach grzyba, przy czym inferencja odbywa się na danych zaszyfrowanych homomorficznie; serwer nie widzi opisu próbki ani jawnej decyzji końcowej.

---

## Dlaczego ten temat został wybrany

### 1. Balans: ciekawość, wykonalność, bezpieczeństwo techniczne

- **Connect-4** — atrakcyjny wizualnie, ale szybko rośnie złożoność (np. wieloklasa, argmax pod FHE).
- **Fashion-MNIST** — mocny wizualnie, lecz obrazy i większy wektor cech są **ciężkie kryptograficznie** (czas, pamięć, parametry HE).
- **Grzyby (UCI Secondary Mushroom)** — prosty do wyjaśnienia niefachowej publiczności, **dobrze mapuje się na modele liniowe** po one-hot encodingu i **realistycznie da się domknąć** w ramach zajęć.

### 2. Jasna historia projektowa (privacy by design)

Scenariusz klient–serwer:

> Użytkownik chce ocenić, czy znaleziony grzyb jest jadalny czy trujący, **bez ujawniania opisu próbki** zewnętrznemu serwerowi. Klient szyfruje cechy, serwer liczy predykcję na ciphertextach i zwraca **zaszyfrowany wynik**; tylko użytkownik odszyfrowuje decyzję.

To jest czytelniejsze i bardziej „projektowe” niż abstrakcyjne zbiory typu income czy spam — nadal jednak **klasyfikacja binarna** i **metryki standardowe** (accuracy, F1, macierz pomyłek).

### 3. Dopasowanie do homomorficznej inferencji

Po kodowaniu cech (np. one-hot):

- regresja logistyczna lub **liniowy SVM**,
- ewentualnie niewielki MLP z aktywacją aproksymowaną wielomianem,
- lub **Concrete ML** z modelem zgodnym ze scikit-learn.

**Rekomendowany tryb pracy (najmniej ryzykowny na termin):**

> **Trening w plaintext**, **inferencja pojedynczej próbki pod FHE** — serwer nigdy nie potrzebuje jawnych wektorów cech użytkownika ani jawnej etykiety wyniku po swojej stronie.

### 4. Benchmarki zgodne z typowymi wymaganiami prowadzących

| Wariant | Co mierzyć |
|--------|------------|
| model jawny | accuracy, F1, czas predykcji |
| model FHE | zgodność predykcji po deszyfracji z baseline, czas szyfrowania, inferencji, deszyfracji |
| parametry HE | wpływ na czas i rozmiar ciphertextu |

Porównanie **poprawności + kosztu obliczeniowego** względem rozwiązania bez szyfrowania jest naturalnym zamknięciem raportu.

---

## Zbiór danych i formuła zadania

- **Zbiór:** [UCI Secondary Mushroom Dataset](https://archive.ics.uci.edu/ml/datasets/Secondary+Mushroom+Dataset) (lub aktualny mirror UCI).
- **Zadanie:** klasyfikacja binarna — **edible** vs **poisonous** (lub równoważne etykiety w pliku danych).

---

## Proponowany stos techniczny

| Priorytet | Narzędzie | Uwagi |
|-----------|-----------|--------|
| start | **Concrete ML** | Szybsza droga do działającej inferencji FHE z modelem sklearn-owym. |
| rozszerzenie (bonus) | **TenSEAL + CKKS** | Bardziej „ręcznie” kryptograficznie; np. prosty iloczyn skalarowy wektor–wagi jako uzupełnienie opisu. |

---

## Minimalny zakres uznawany za kompletny (MVP)

1. Pobranie i preprocessing danych.
2. One-hot (lub inne ustalone kodowanie) cech kategorycznych.
3. Trening modelu w plaintext.
4. Ewaluacja jawna: accuracy, F1, confusion matrix.
5. Kompilacja / ścieżka inferencji FHE (zgodnie z wybraną biblioteką).
6. Klient: szyfrowanie próbki.
7. Serwer: predykcja bez dostępu do plaintextu.
8. Klient: odszyfrowanie wyniku.
9. Benchmark: plaintext vs encrypted (czasy, ewentualnie rozmiar ciphertextu).
10. Krótka analiza ograniczeń HE (szum, parametry, koszt).

---

## Demo (prezentacja)

Interfejs CLI (lub prosta mini-apka), np.:

```text
Cap shape: convex
Cap color: brown
Gill color: white
Stem height: medium
...

Encrypting sample...
Sending encrypted vector to cloud classifier...
Server prediction on encrypted data...
Encrypted result returned.

Decrypted result: POISONOUS
```

**Przekaz dla prowadzącego:** serwer **nie zna** jawnych cech wejściowych ani **ostatecznej interpretacji** wyniku — widzi wyłącznie operacje na ciphertextach i zwraca dane do odszyfrowania przez klienta.

---

## Podsumowanie

Temat **klasyfikacji toksyczności grzybów z FHE** został wybrany jako **główny kandydat** ze względu na najlepszy kompromis między wartością dydaktyczną a ryzykiem technicznym: czytelny problem, silna narracja prywatności, modele liniowe po preprocessingu oraz przewidywalne metryki i benchmarki — przy realistycznej szansie na **działający, dobrze opisany** projekt w limicie czasu zajęć.
