# Projekt-infa
Test AOSPAN to narzędzie służące do pomiaru pojemności pamięci roboczej. Jego wykonanie polega na jednoczesnym rozwiązywaniu prostych równań matematycznych i zapamiętywaniu pokazywanych liter. Test pozwala na ocenę zdolność do równoczesnego przetwarzania i przechowywania informacji. . Obecnie używaną wersją testu jest AOSPAN (zautomatyzowany Test Ospan) opracowany przez Unsworth, Heitz, Schrock i Engle (2005).Jest on łatwy w obsłudze, samodzielnie ocenia wyniki i wymaga minimalnego wkładu eksperymentatora, ma dobrą wewnętrzną spójność (α = 0,78), wysoką rzetelność test-retest (0,83), a także koreluje z innymi miarami pamięci roboczej oraz zdolnościami poznawczymi (Unsworth i in., 2005). W niniejszym badaniu zadanie to zostało wykorzystane do oceny wpływu manipulacji percepcją czasu (za pomocą dźwięków) na zakres pamięci roboczej. Pytanie badawcze, na które ma pomóc odpowiedzieć procedura brzmi: “Czy przyspieszenie wewnętrznego zegara zwiększa pojemność pamięci roboczej ?”.

## Instalacja i uruchomienie

1. Sklonuj repozytorium:

    ```bash
    git clone https://github.com/EmiWojdylo/Projekt-infa/
    cd Projekt-infa
    ```

2. (Opcjonalnie) Utwórz wirtualne środowisko:

    ```bash
    python -m venv venv
    ```

3. Aktywuj środowisko:

    - **Windows**:

      ```bash
      venv\Scripts\activate
      ```

    - **macOS / Linux**:

      ```bash
      source venv/bin/activate
      ```

4. Zainstaluj wymagane biblioteki:

    Jeśli masz plik `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    Lub zainstaluj ręcznie:

    ```bash
    pip install psychopy
    ```

5. Uruchom projekt:

    ```bash
    python main.py
    ```

📁 Upewnij się, że plik konfiguracyjny (np. `psychopy-env.yml`) znajduje się w katalogu głównym projektu.


## Instrukcja
Po uruchomieniu procedury pojawią się następujące komunikaty:
"W tej części eksperymentu twoim zadaniem będzie wykonywanie prostych obliczeń oraz zapamiętywanie wyświetlanych po nich liter. Następnie zazanczysz litery w takiej kolejności, w jakiej zostały pokazane. Jeżeli zapomnisz którejśz liter, wstaw w jej miejsce znak zapytania. Staraj się wykonywać zadanie tak szybko i dokładnie jak potrafisz. Równania rozwiązuj w myślach zanim jeszcze przejdziesz do ekranu na którym określisz, czy podany wynik jest prawdziwy czy fałszywy. Naciśnij spację, aby przejść dalej. 
Po każdym równaniu zobaczysz literę. Zapamiętaj ją. Po serii kilku takich równań zosatniesz poproszony o przywołanie liter w poprawnej kolejności. Klikaj we właściwe litery. Jeżwli którejś zapomnisz, kliknij zank zapytania. 
To już wszystkie potrzebne Ci informacje. Naciśnij spację, aby przejść do serii treningowej."

Po serii treningowej wyświetli się komunikat do serii oszacowania czasu:
"W następnej części eksperymentu będziesz słuchać serii dżwięków. Słuchaj ich uważnie. Utrzymój wzrok na punkcie fiksacji. 
Naciśnij spację, aby  przejść do zadania."

Przed właściwą sesją oszacowania czasu:
"W następnej części będziesz słuchać dżwięków a następnie oszacowywać, ile sekund trwały. Aby odpowiedzieć, kliknij na klawiaturze od 1 do 8. Odpowiadaj tak, jak Ci się wydaje.
Naciśnij spację, aby przejść do zadania"

Przed główną częścią:
"Teraz nadszedł czas na ostatnie zadanie. Będziesz rozwiązywaćrównania praz zapamiętywać litery.
Przed każdą swrią równań pojawiają się dźwięki. Przysłuchuj się im uważnie, utrzymując wzrok na punkcie fiksacji.
Naciśnij spację, aby przejść do zadania"
## Autorki
Emilia Wojdyło,

Aleksandra Olszanowska,

Olga Śmieja
