# Can I eat this?

**Poufny klasyfikator grzybów (FHE):** serwer liczy *jadalny / trujący* na **zaszyfrowanych cechach**; wynik też wraca zaszyfrowany — **odszyfrowuje go tylko klient**. Zbiór: **UCI Secondary Mushroom** (edible vs poisonous). Trening w plaintext, inferencja pod FHE (np. Concrete ML; opcjonalnie TenSEAL / CKKS).

```text
cechy → szyfr → serwer (model na ciphertextach) → zaszyfrowany wynik → deszyfr → decyzja
```

**Dokumenty:** [temat.md](temat.md) (uzasadnienie, MVP, demo) · [requirements.md](requirements.md) (specyfikacja). Kod i setup — wraz z implementacją.
