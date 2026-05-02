# Klasyfikator działający na danych zaszyfrowanych homomorficznie

## 1. Cel projektu

Celem projektu jest zaprojektowanie i zaimplementowanie demonstracyjnego systemu klasyfikacji danych, w którym:

1. właściciel danych szyfruje próbkę wejściową,
2. zaszyfrowana próbka jest wysyłana do serwera,
3. serwer wykonuje obliczenia klasyfikatora bez odszyfrowywania danych,
4. serwer zwraca zaszyfrowany wynik,
5. właściciel danych odszyfrowuje wynik i poznaje predykcję klasyfikatora.

Projekt ma pokazać praktyczne połączenie kryptografii homomorficznej z analizą danych oraz porównać poprawność i wydajność rozwiązania względem klasyfikatora działającego na danych jawnych.

---

## 2. Krótki opis scenariusza

Przyjmujemy scenariusz klient-serwer:

- **Klient / właściciel danych** posiada dane wejściowe oraz klucz prywatny.
- **Serwer obliczeniowy** posiada wytrenowany model klasyfikacyjny i wykonuje predykcję na zaszyfrowanych danych.
- **Serwer nie ma dostępu do danych jawnych** ani do klucza prywatnego.
- **Wynik obliczeń po stronie serwera pozostaje zaszyfrowany**.
- **Ostateczna interpretacja wyniku** następuje dopiero po odszyfrowaniu przez klienta.

---

## 3. Rekomendowany zakres projektu

### 3.1. Zakres podstawowy — MVP

Projekt powinien obejmować:

1. wybór prostego problemu klasyfikacji binarnej,
2. przygotowanie danych i baseline'u bez szyfrowania,
3. wytrenowanie prostego modelu klasyfikacyjnego,
4. implementację szyfrowania danych wejściowych,
5. wykonanie predykcji na zaszyfrowanych danych,
6. odszyfrowanie wyniku przez klienta,
7. porównanie wyniku z klasyfikacją na danych jawnych,
8. pomiar czasu działania i narzutu szyfrowania.

Rekomendowany model dla MVP:

- regresja logistyczna bez nieliniowej funkcji sigmoid po stronie serwera,
- ewentualnie klasyfikator liniowy / perceptron / SVM liniowy w uproszczonej wersji.

Najprostsza wersja działania:

```text
encrypted_input = encrypt(x)

encrypted_score = encrypted_input · weights + bias

score = decrypt(encrypted_score)

class = 1 if score >= 0 else 0
```

W tym wariancie serwer zwraca zaszyfrowany wynik decyzyjny, np. logit albo score. Klient po odszyfrowaniu stosuje próg decyzyjny i poznaje klasę.

### 3.2. Zakres rozszerzony — opcjonalny

Jeżeli wystarczy czasu, można dodać:

1. przybliżenie funkcji sigmoid wielomianem,
2. zwracanie zaszyfrowanego prawdopodobieństwa zamiast samego score'u,
3. batch prediction dla wielu próbek naraz,
4. prosty interfejs CLI lub web demo,
5. porównanie dwóch bibliotek, np. TenSEAL i Concrete ML,
6. klasyfikację wieloklasową metodą one-vs-rest,
7. eksperyment z różnymi parametrami szyfrowania,
8. wykresy czasu działania i dokładności.

### 3.3. Poza zakresem projektu

Projekt nie zakłada:

1. trenowania modelu na zaszyfrowanych danych,
2. budowy produkcyjnego systemu bezpieczeństwa,
3. obsługi dużych modeli głębokich,
4. pełnego ukrywania modelu przed klientem,
5. wykonywania porównań logicznych bezpośrednio na ciphertextach,
6. implementacji kryptografii homomorficznej od zera,
7. gwarancji odporności na wszystkie ataki bocznokanałowe.

---

## 4. Proponowany stos technologiczny

### 4.1. Język

- Python 3.10+ albo Python 3.11.

### 4.2. Biblioteki

Rekomendowany wariant główny:

- `tenseal` — operacje homomorficzne na wektorach,
- `scikit-learn` — trening baseline'owego klasyfikatora,
- `numpy` — obliczenia numeryczne,
- `pandas` — obsługa danych tabelarycznych,
- `matplotlib` / `plotly` — wykresy,
- `pytest` — testy.

Alternatywny wariant:

- `concrete-ml` — framework do privacy-preserving machine learning.

### 4.3. Schemat szyfrowania

Rekomendowany schemat:

- CKKS, ponieważ dobrze nadaje się do przybliżonych obliczeń na liczbach rzeczywistych.

Uzasadnienie:

- klasyfikatory liniowe operują głównie na liczbach rzeczywistych,
- CKKS pozwala wykonywać dodawanie i mnożenie na zaszyfrowanych wartościach przy zachowaniu przybliżonej precyzji,
- niewielki błąd numeryczny jest akceptowalny, jeżeli predykcja po odszyfrowaniu zgadza się z baseline'em z danych jawnych.

---

## 5. Dane

### 5.1. Wymagania wobec zbioru danych

Zbiór danych powinien:

1. dotyczyć klasyfikacji binarnej,
2. mieć cechy numeryczne albo łatwe do przekształcenia na numeryczne,
3. mieć umiarkowaną liczbę cech,
4. pozwalać szybko trenować model baseline'owy,
5. umożliwiać przeprowadzenie porównania: plaintext vs encrypted.

### 5.2. Rekomendowane zbiory danych

Możliwe zbiory:

1. Breast Cancer Wisconsin — klasyfikacja zmian łagodnych/złośliwych,
2. Iris w wariancie binarnym — np. jedna klasa kontra reszta,
3. Wine w wariancie binarnym,
4. syntetyczny zbiór wygenerowany przez `make_classification`.

Rekomendacja dla projektu:

- użyć Breast Cancer Wisconsin albo syntetycznego zbioru danych.

Breast Cancer Wisconsin jest dobrym wyborem, ponieważ ma dane numeryczne i naturalnie pasuje do scenariusza prywatnej klasyfikacji medycznej.

---

## 6. Wymagania funkcjonalne

### FR-01 — Wczytanie danych

System musi umożliwiać wczytanie zbioru danych używanego do trenowania i testowania klasyfikatora.

### FR-02 — Podział danych

System musi dzielić dane na zbiór treningowy i testowy, np. w proporcji 80/20.

### FR-03 — Preprocessing

System musi wykonywać preprocessing danych, w szczególności:

- obsługę cech numerycznych,
- skalowanie lub standaryzację cech,
- zapis parametrów preprocessingu potrzebnych do przekształcania nowych próbek.

### FR-04 — Model baseline bez szyfrowania

System musi trenować klasyfikator na danych jawnych i mierzyć jego jakość na zbiorze testowym.

Minimalne metryki:

- accuracy,
- precision,
- recall,
- F1-score,
- confusion matrix.

### FR-05 — Przygotowanie modelu do predykcji homomorficznej

System musi wyeksportować parametry modelu potrzebne do wykonania predykcji na danych zaszyfrowanych, np.:

- wektor wag,
- bias/intercept,
- parametry skalowania danych.

### FR-06 — Generowanie kluczy

System musi generować kontekst kryptograficzny oraz klucze potrzebne do działania schematu homomorficznego.

Wymaganie bezpieczeństwa:

- klucz prywatny pozostaje po stronie klienta,
- serwer nie otrzymuje klucza prywatnego.

### FR-07 — Szyfrowanie danych wejściowych

System musi umożliwiać zaszyfrowanie pojedynczej próbki wejściowej albo małej paczki próbek.

### FR-08 — Predykcja na danych zaszyfrowanych

System musi wykonać predykcję na zaszyfrowanych danych bez ich odszyfrowywania po stronie serwera.

Minimalna operacja:

```text
encrypted_score = encrypted_features · weights + bias
```

### FR-09 — Zwrócenie zaszyfrowanego wyniku

Serwer musi zwracać wynik w postaci zaszyfrowanej.

Minimalnie:

- zaszyfrowany score/logit.

Opcjonalnie:

- zaszyfrowane przybliżone prawdopodobieństwo klasy pozytywnej.

### FR-10 — Odszyfrowanie wyniku przez klienta

Klient musi odszyfrować wynik i zamienić go na końcową klasę.

Dla klasyfikatora liniowego:

```text
class = 1 if decrypted_score >= 0 else 0
```

### FR-11 — Porównanie z baseline'em

System musi porównać wyniki predykcji homomorficznej z wynikami modelu działającego na danych jawnych.

Minimalne porównanie:

- zgodność predykcji na próbkach testowych,
- różnica wartości score'u między plaintext i encrypted,
- liczba przypadków, w których predykcja się różni.

### FR-12 — Pomiar wydajności

System musi mierzyć:

- czas predykcji bez szyfrowania,
- czas generowania kluczy,
- czas szyfrowania próbki,
- czas predykcji na zaszyfrowanych danych,
- czas odszyfrowania wyniku,
- całkowity czas obsługi jednej próbki.

Opcjonalnie:

- rozmiar ciphertextu,
- zużycie pamięci,
- czas batch prediction dla wielu próbek.

### FR-13 — Raportowanie wyników

System musi generować wyniki w formie czytelnej dla raportu.

Minimalne artefakty:

- tabela metryk klasyfikacji,
- tabela czasów działania,
- wykres porównujący czas plaintext vs encrypted,
- opis różnic numerycznych,
- komentarz dotyczący ograniczeń rozwiązania.

### FR-14 — Testy poprawności

System musi zawierać testy sprawdzające, że:

- szyfrowanie i odszyfrowanie zachowują przybliżoną wartość liczbową,
- predykcja zaszyfrowana daje wynik zgodny albo prawie zgodny z predykcją jawną,
- serwer nie używa klucza prywatnego,
- preprocessing dla danych treningowych i testowych jest spójny.

---

## 7. Wymagania niefunkcjonalne

### NFR-01 — Prostota uruchomienia

Projekt powinien dać się uruchomić jedną lub kilkoma prostymi komendami, np.:

```bash
python -m src.train
python -m src.demo_encrypted_prediction
python -m src.benchmark
```

### NFR-02 — Powtarzalność wyników

Projekt musi używać ustalonego ziarna losowości, np.:

```python
random_state = 42
```

### NFR-03 — Czytelność kodu

Kod powinien być podzielony na moduły:

- dane,
- model,
- kryptografia,
- predykcja,
- benchmark,
- wizualizacja.

### NFR-04 — Dokumentacja

Repozytorium musi zawierać:

- `README.md`,
- `requirements.md`,
- instrukcję uruchomienia,
- krótki opis architektury,
- opis eksperymentów,
- opis ograniczeń.

### NFR-05 — Bezpieczeństwo demonstracyjne

Projekt ma być poprawny koncepcyjnie, ale nie musi być produkcyjnym systemem bezpieczeństwa.

W raporcie należy wyraźnie zaznaczyć, że:

- jest to demonstracja akademicka,
- parametry kryptograficzne należy dobrać ostrożnie w zastosowaniach produkcyjnych,
- model i metadane mogą ujawniać pewne informacje,
- nie analizujemy pełnego modelu zagrożeń.

---

## 8. Wymagania kryptograficzne

### CR-01 — Schemat szyfrowania

System powinien używać schematu CKKS.

### CR-02 — Klucze

System musi rozdzielać role kluczy:

- klient posiada klucz prywatny,
- serwer posiada tylko dane potrzebne do wykonywania obliczeń na ciphertextach,
- serwer nie może odszyfrować danych wejściowych ani wyniku.

### CR-03 — Parametry CKKS

W kodzie należy jawnie zdefiniować i opisać parametry, np.:

- `poly_modulus_degree`,
- `coeff_mod_bit_sizes`,
- `global_scale`.

Przykładowe wartości startowe:

```python
poly_modulus_degree = 8192
coeff_mod_bit_sizes = [60, 40, 40, 60]
global_scale = 2 ** 40
```

Ostateczne wartości powinny zostać dobrane eksperymentalnie i opisane w raporcie.

### CR-04 — Precyzja

System musi mierzyć różnicę między wynikiem obliczonym na danych jawnych i zaszyfrowanych:

```text
absolute_error = abs(plaintext_score - decrypted_encrypted_score)
```

### CR-05 — Brak odszyfrowania po stronie serwera

Kod demonstracyjny powinien jasno rozdzielać klienta i serwer.

W szczególności:

- funkcje serwerowe nie powinny mieć dostępu do secret key,
- odszyfrowanie powinno występować tylko po stronie klienta.

---

## 9. Wymagania uczenia maszynowego

### ML-01 — Model

Minimalny model:

- regresja logistyczna albo klasyfikator liniowy.

Model powinien być prosty, ponieważ operacje homomorficzne dobrze obsługują dodawanie i mnożenie, ale gorzej radzą sobie z nieliniowościami, porównaniami i rozgałęzieniami.

### ML-02 — Dane wejściowe

Dane wejściowe do modelu powinny być numeryczne i przeskalowane.

### ML-03 — Baseline

Należy najpierw uruchomić pełny pipeline bez szyfrowania.

Baseline powinien podawać:

- metryki jakości,
- czas predykcji,
- przykładowe wyniki predykcji.

### ML-04 — Zgodność predykcji

Dla zbioru testowego należy obliczyć:

```text
encrypted_agreement = liczba_zgodnych_predykcji / liczba_wszystkich_predykcji
```

Minimalny oczekiwany wynik:

- zgodność predykcji encrypted vs plaintext: co najmniej 95% dla sensownie dobranych parametrów i danych.

### ML-05 — Obsługa błędów numerycznych

Należy opisać przypadki, w których wynik encrypted różni się od plaintext.

Szczególnie ważne są próbki blisko granicy decyzyjnej, gdzie mały błąd przybliżenia może zmienić klasę.

---

## 10. Architektura systemu

### 10.1. Komponenty

System powinien zawierać następujące komponenty:

1. `DataLoader` — wczytanie i przygotowanie danych.
2. `PlainModelTrainer` — trening modelu bez szyfrowania.
3. `CryptoContextFactory` — konfiguracja CKKS i generowanie kontekstu.
4. `Client` — szyfrowanie danych i odszyfrowanie wyniku.
5. `EncryptedInferenceServer` — predykcja na ciphertextach.
6. `BenchmarkRunner` — pomiar czasu działania.
7. `ReportGenerator` — zapis tabel i wykresów do raportu.

### 10.2. Przepływ danych

```text
[Client]
  raw sample
      |
      v
  preprocessing
      |
      v
  encryption
      |
      v
 encrypted sample
      |
      v
[Server]
  encrypted inference
      |
      v
 encrypted score
      |
      v
[Client]
  decryption
      |
      v
  class decision
```

---

## 11. Proponowana struktura repozytorium

```text
encrypted-classifier/
├── README.md
├── requirements.md
├── requirements.txt
├── pyproject.toml                  # opcjonalnie
├── data/
│   └── README.md
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── __init__.py
│   ├── data.py
│   ├── model.py
│   ├── crypto.py
│   ├── client.py
│   ├── server.py
│   ├── benchmark.py
│   ├── plots.py
│   └── main.py
├── tests/
│   ├── test_crypto_roundtrip.py
│   ├── test_plain_vs_encrypted.py
│   └── test_server_no_secret_key.py
├── results/
│   ├── metrics.csv
│   ├── benchmark.csv
│   └── plots/
└── report/
    └── report.md
```

---

## 12. Minimalne komendy uruchomieniowe

Projekt powinien umożliwiać uruchomienie przynajmniej takich kroków:

```bash
# 1. Instalacja zależności
pip install -r requirements.txt

# 2. Trening modelu jawnego
python -m src.train

# 3. Demo jednej predykcji zaszyfrowanej
python -m src.demo

# 4. Benchmark
python -m src.benchmark
```

Jeżeli projekt będzie prostszy, dopuszczalna jest jedna komenda:

```bash
python -m src.main
```

Wtedy `main.py` powinien wykonać pełny pipeline:

1. wczytanie danych,
2. trening modelu,
3. test plaintext,
4. konfigurację szyfrowania,
5. encrypted inference,
6. porównanie wyników,
7. zapis rezultatów.

---

## 13. Benchmark

### 13.1. Co mierzymy

Należy porównać wersję jawną i zaszyfrowaną.

Minimalne pomiary:


| Metryka                            | Opis                                     |
| ---------------------------------- | ---------------------------------------- |
| `plaintext_prediction_time_ms`     | czas predykcji bez szyfrowania           |
| `key_generation_time_ms`           | czas wygenerowania kontekstu i kluczy    |
| `encryption_time_ms`               | czas szyfrowania danych wejściowych      |
| `encrypted_inference_time_ms`      | czas predykcji na zaszyfrowanych danych  |
| `decryption_time_ms`               | czas odszyfrowania wyniku                |
| `total_encrypted_pipeline_time_ms` | pełny czas pipeline'u encrypted          |
| `encrypted_vs_plaintext_slowdown`  | ile razy wolniej działa wersja encrypted |


### 13.2. Liczba eksperymentów

Minimalnie:

- benchmark dla 1 próbki,
- benchmark dla 10 próbek,
- benchmark dla 100 próbek.

Opcjonalnie:

- 1000 próbek,
- porównanie batch vs pojedyncze próbki.

### 13.3. Prezentacja wyników

W raporcie należy zawrzeć:

1. tabelę czasów,
2. wykres słupkowy porównujący plaintext i encrypted,
3. komentarz, która część pipeline'u jest najwolniejsza,
4. wniosek, czy rozwiązanie nadaje się do małych demonstracji, a czy do dużej skali.

---

## 14. Kryteria akceptacji

Projekt można uznać za wykonany, jeżeli spełnia wszystkie poniższe punkty:

1. istnieje działający klasyfikator baseline bez szyfrowania,
2. istnieje działająca predykcja na zaszyfrowanych danych,
3. serwer nie odszyfrowuje danych wejściowych,
4. wynik zwracany przez serwer jest zaszyfrowany,
5. klient potrafi odszyfrować wynik i wyznaczyć klasę,
6. wyniki encrypted są porównane z plaintext,
7. zmierzono wydajność obu wersji,
8. w raporcie opisano ograniczenia rozwiązania,
9. repozytorium zawiera instrukcję uruchomienia,
10. kod da się uruchomić od początku do końca.

---

## 15. Proponowany podział pracy w zespole 2-3 osobowym

### Osoba 1 — Machine Learning i dane

Odpowiedzialność:

- wybór datasetu,
- preprocessing,
- trening baseline,
- metryki jakości,
- analiza wyników klasyfikacji.

### Osoba 2 — Kryptografia i encrypted inference

Odpowiedzialność:

- konfiguracja CKKS,
- szyfrowanie i odszyfrowanie,
- implementacja predykcji na ciphertextach,
- testy poprawności kryptograficznej.

### Osoba 3 — Benchmark, raport i integracja

Odpowiedzialność:

- benchmark wydajności,
- wykresy,
- README,
- raport końcowy,
- integracja pipeline'u.

Dla zespołu 2-osobowego:

- osoba 1: ML + dane + metryki,
- osoba 2: kryptografia + inference + benchmark,
- raport pisany wspólnie.

---

## 16. Plan konsultacji

Ponieważ wymagane są co najmniej 4 obecności na konsultacjach, można zaplanować je następująco:

### Konsultacja 1 — zatwierdzenie scope'u

Do pokazania:

- temat,
- wybrany dataset,
- plan architektury,
- decyzja: CKKS + klasyfikator liniowy.

### Konsultacja 2 — baseline ML

Do pokazania:

- działający model bez szyfrowania,
- metryki jakości,
- preprocessing,
- pierwsze wyniki predykcji.

### Konsultacja 3 — encrypted inference

Do pokazania:

- szyfrowanie próbki,
- predykcja na ciphertextach,
- odszyfrowanie wyniku,
- porównanie jednej lub kilku próbek z plaintext.

### Konsultacja 4 — benchmark i raport

Do pokazania:

- finalne wyniki,
- tabela czasów,
- wykresy,
- opis ograniczeń,
- demo końcowe.

---

## 17. Ryzyka i ograniczenia

### R-01 — Duży narzut czasowy

Operacje homomorficzne będą znacznie wolniejsze niż zwykła predykcja.

Mitigacja:

- użyć prostego modelu,
- użyć małej liczby cech,
- mierzyć czas dla małych paczek danych,
- nie próbować trenować modelu pod FHE.

### R-02 — Błędy przybliżenia w CKKS

CKKS daje wyniki przybliżone, więc wynik po odszyfrowaniu może minimalnie różnić się od plaintext.

Mitigacja:

- mierzyć absolute error,
- analizować próbki blisko granicy decyzyjnej,
- dobrać parametry CKKS eksperymentalnie.

### R-03 — Problem z funkcją sigmoid

Sigmoid nie jest naturalnie wygodna w FHE, ponieważ jest funkcją nieliniową.

Mitigacja:

- w MVP zwracać encrypted score,
- próg decyzyjny stosować po odszyfrowaniu,
- sigmoid wielomianowy potraktować jako rozszerzenie.

### R-04 — Złożoność bibliotek

Biblioteki FHE mogą mieć problemy instalacyjne.

Mitigacja:

- wcześnie przygotować środowisko,
- zapisać dokładne wersje pakietów,
- rozważyć Docker,
- mieć fallback na prostszy dataset i prostszy pipeline.

---

## 18. Deliverables

Na koniec projektu należy oddać:

1. kod źródłowy,
2. `README.md` z instrukcją uruchomienia,
3. `requirements.md` z zakresem i wymaganiami,
4. skrypt lub notebook z baseline'em ML,
5. skrypt z encrypted inference,
6. benchmark,
7. raport końcowy,
8. wykresy i tabele wyników,
9. krótkie demo działania.

---

## 19. Minimalny wynik końcowy demo

Minimalne demo powinno pokazywać coś w tym stylu:

```text
Plaintext sample:
[0.12, -1.45, 0.33, ...]

Plaintext model score:
1.2841

Plaintext class:
1

Encrypted prediction:
sample encrypted on client
server computes encrypted score
encrypted score returned to client

Decrypted encrypted score:
1.2840

Class after decryption:
1

Absolute error:
0.0001

Prediction match:
True

Plaintext inference time:
0.05 ms

Encrypted pipeline time:
120.50 ms

Slowdown:
2410x
```

---

## 20. Definicja ukończenia

Projekt jest ukończony, jeżeli można uruchomić pełny pipeline i odpowiedzieć na pytania:

1. Czy serwer widzi dane jawne?
  Nie.
2. Czy serwer może odszyfrować wynik?
  Nie.
3. Czy klient po odszyfrowaniu dostaje sensowną predykcję?
  Tak.
4. Czy predykcja encrypted zgadza się z plaintext?
  Tak, w większości przypadków; różnice należy opisać.
5. Ile kosztuje prywatność?
  Należy pokazać narzut czasowy i ewentualnie pamięciowy.
6. Jakie są ograniczenia?
  Prosty model, narzut obliczeniowy, problemy z nieliniowościami, przybliżony charakter CKKS.

---

## 21. Najważniejsza decyzja projektowa

Aby projekt był wykonalny i zgodny z tematem, przyjmujemy następującą interpretację:

> Serwer klasyfikuje dane bez znajomości ich jawnej postaci. Wynikiem zwracanym przez serwer jest zaszyfrowany score klasyfikatora. Właściciel danych po odszyfrowaniu score'u wyznacza końcową klasę.

Taka interpretacja spełnia wymaganie, że dane wejściowe są zaszyfrowane, obliczenia odbywają się bez odszyfrowywania danych, a właściciel danych dopiero po odszyfrowaniu poznaje wynik klasyfikacji.