import csv
import os
import time
from psychopy import visual, core, event, sound, gui, data
from psychopy.visual import ButtonStim
import random

# Ustawienie okna (bez fullscreena, bo na macu nie dziala)
win = visual.Window(size=(1440, 900), color='silver', units='pix')  # do zmiany fullscr=True
slider_duration = 8.0  # maksymalny czas na odpowiedź

# Tekst
text_stim = visual.TextStim(win=win, text='', color='black', height=40, wrapWidth=1000)


# Funkcja ktora, prezentuje tekst (i czeka na klawisz)
def show_text_and_wait(text):
    text_stim.text = text
    text_stim.draw()
    win.flip()
    event.waitKeys()


# Dane uczestnika
info = {'ID': '', 'Wiek': '', 'Plec': ''}

dlg = gui.DlgFromDict(info, title='Eksperyment OSPAN_Click')
if not dlg.OK:
    core.quit()

participant_id = info['ID']


# punkt fiksacji
def show_fixation_cross(win, duration=5.0):
    fixation = visual.TextStim(
        win, text='+', height=50, color='black', pos=(0, 0))
    fixation.draw()
    win.flip()
    core.wait(duration)


# PLIKI CSV Z DANYMI
output_file_k = 'klik_data.csv'
output_file_o = "ospan_wyniki.csv"

# plik do dźwięku
# block_type to eksperyment/trial, dur_t to czas trwania dźwięku, resp to odpowiedz
if not os.path.exists(output_file_k):
    with open(output_file_k, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'id', 'trial', 'block_type',
            'dur_t', 'resp', 'rt'
        ])

# plik do ospan
if not os.path.exists(output_file_o):
    with open(output_file_o, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["blok", "set_size", "poprawne_litery", "poprawne_dzialania (%)", "sredni_rt (s)"])

# INSTRUKCJE
instrukcja_skala_dzwieki = visual.TextStim(win, text="Oszacuj czas trwania dźwięków:", pos=(0, 0.3), color='black')

# ELEMENTY CZĘŚĆI DŹWIĘKOWEJ

# Skala do oszacowania czasu
time_slider = visual.Slider(
    win, ticks=(2, 3, 4, 5, 6, 7, 8),
    labels=['2s', '3s', '4s', '5s', '6s', '7s', '8s'],
    size=(1000, 60), pos=(0, -200),
    granularity=0.1, style='rating', color='black',
    labelColor='black', markerColor='black', units='pix')

# Dźwięk
klik_dzwiek = sound.Sound("s8.wav")




def tylko_dzwiek1():
    # Odtwarzanie klików w pierwszej prezentacji bodźca
    klik_dzwiek.setVolume(0.5)
    klik_dzwiek.play()
    show_fixation_cross(win, duration=10.0)
    core.wait(1.0)
    win.flip()
    klik_dzwiek.stop()

def tylko_dzwiek2():
        # Odtwarzanie klików przed każdą serią ospan
        klik_dzwiek.setVolume(0.5)
        klik_dzwiek.play()
        show_fixation_cross(win, duration=5.0)
        core.wait(0.5)
        win.flip()
        klik_dzwiek.stop()

# Funkcja: jedna próba klikowa
def jedna_proba_click(seria_num, duration_s, output_file_k, block_type):
    # Odtwarzanie klików
    klik_dzwiek.setVolume(0.5)
    klik_dzwiek.play()
    show_fixation_cross(win, duration=5.0)
    core.wait(0.5)
    win.flip()
    klik_dzwiek.stop()

    # Skala odpowiedzi
    # Zdecydowałyśmy się ponieważ będzie bardziej zrozumiała i czytelna dla uczestnika
    time_slider.reset()
    instrukcja_skala_dzwieki.draw()
    time_slider.draw()
    win.flip()

    timer = core.Clock()
    rt = None
    response = None

    while timer.getTime() < slider_duration:
        if event.getKeys(['escape']):
            core.quit()
        time_slider.draw()
        instrukcja_skala_dzwieki.draw()
        win.flip()
        if time_slider.getRating() is not None and rt is None:
            rt = timer.getTime()
            response = time_slider.getRating()
            break

    # Zapis do CSV
    with open(output_file_k, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            participant_id, seria_num, block_type,
            duration_s, response, rt
        ])

    # Przerwa między próbami
    core.wait(0.5)


# ELEMENTY CZĘŚCI OSPAN

# Dzialania matematyczne
def generate_math_problem():
    while True:
        op1 = random.choice(['*', '/'])
        op2 = random.choice(['+', '-'])
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        try:
            if op1 == '*':
                first = a * b
            else:
                if b == 0 or a % b != 0:
                    continue
                first = a // b
            if op2 == '+':
                result = first + c
            else:
                result = first - c
            if 1 <= result <= 9:
                is_correct = random.choice([True, False])
                displayed_result = result
                if not is_correct:
                    offset = random.choice([-2, -1, 1, 2])
                    displayed_result = max(1, min(9, result + offset))
                    if displayed_result == result:
                        continue
                expression = f"({a} {op1} {b}) {op2} {c} ="
                result_only = f"{displayed_result}"
                return expression, result_only, is_correct
        except ZeroDivisionError:
            continue


# wyświetlanie zadania matematycznego
def show_math_problem(win, expression, result_only, is_result_correct):
    # Tekst działania matematycznego
    eq_text = visual.TextStim(win, text=expression, height=40, color='black', pos=(0, 0))
    eq_text.draw()
    win.flip()
    core.wait(2.0)

    # wynik i przyciski P F
    result_text = visual.TextStim(win, text=result_only, height=40, color='black', pos=(0, 100))
    true_button = ButtonStim(
        win, text="Prawda", pos=(-150, -50), size=(200, 80),
        letterHeight=30, color='white', fillColor='dimgray', borderColor='white')
    false_button = ButtonStim(
        win, text="Falsz", pos=(150, -50), size=(200, 80),
        letterHeight=30, color='white', fillColor='dimgray', borderColor='white')

    mouse = event.Mouse()

    while True:
        result_text.draw()
        true_button.draw()
        false_button.draw()
        win.flip()

        if mouse.getPressed()[0]:
            if true_button.contains(mouse):
                return is_result_correct is True
            elif false_button.contains(mouse):
                return is_result_correct is False


# litery
letters = list("FHJKLNPQRSTY")

# Litery do wyboru
letters_k = ["F", "H", "J", "K", "L", "N", "P", "Q", "R", "S", "T", "Y"]
response = ""

# Pozycje przycisków
button_grid = []
button_size = (100, 60)
start_x = -150
start_y = 100
cols = 3
rows = 4

# Tworzenie przycisków z literami
for i in range(len(letters)):
    row = i // cols
    col = i % cols
    x = start_x + col * 150
    y = start_y - row * 100
    button = ButtonStim(win, text=letters[i], pos=(x, y), letterHeight=30, color='black',
                        size=button_size, fillColor='dimgray', borderColor='black')
    button_grid.append((button, letters_k[i]))

    # znak zapytania
    question_button = ButtonStim(win, text="?", pos=(start_x + 150, start_y - 4 * 100),
                                 letterHeight=30, color='black', size=button_size,
                                 fillColor='dimgray', borderColor='black')
    # przycisk delete
    delete_button = ButtonStim(
        win, text="DEL", pos=(start_x + 3 * 150, start_y - 3 * 100),
        letterHeight=30, color='black',
        size=button_size, fillColor='dimgray', borderColor='white')

# Tekst pokazujący odpowiedź
response_text = visual.TextStim(win, text="", pos=(0, 250), color='black', height=30)

# Instrukcja
instr = visual.TextStim(win,
                        text="Zaznacz litery w kolejności, w jakiej je widziałeś/widziałaś. Jeżeli nie pamiętasz którejś z liter, wstaw w jej miejsce znak zapytania. \nAby zatwierdzić, naciśnij ENTER.",
                        pos=(0, 300), color='black', height=20, wrapWidth=700)


# funkcja - działanie ospan
def ospan_blok(block_num, set_size, output_file_o, block_label):
    sequence = []
    response = ""
    math_correct_count = 0
    math_rts = []

    for i in range(set_size):
        # Litera
        show_fixation_cross(win, duration=1.0)
        letter = random.choice(letters)
        sequence.append(letter)
        text_stim.text = letter
        text_stim.draw()
        win.flip()
        core.wait(0.8)

        # Działanie matematyczne
        expression, result_only, is_result_correct = generate_math_problem()
        start_time = time.time()
        is_answer_correct = show_math_problem(win, expression, result_only, is_result_correct)
        rt = time.time() - start_time
        math_rts.append(rt)
        if is_answer_correct:
            math_correct_count += 1

    # Ekran odpowiedzi
    while True:
        instr.draw()
        response_text.text = "Odpowiedź: " + response
        response_text.draw()

        for btn, _ in button_grid:
            btn.draw()
        question_button.draw()
        delete_button.draw()
        win.flip()

        mouse = event.Mouse()
        keys = event.getKeys()

        if "return" in keys or "enter" in keys:
            break

        if mouse.getPressed()[0]:
            for btn, letter in button_grid:
                if btn.contains(mouse):
                    response += letter
                    core.wait(0.2)
            if question_button.contains(mouse):
                response += "?"
                core.wait(0.2)
            if delete_button.contains(mouse) and len(response) > 0:
                response = response[:-1]
                core.wait(0.2)

    # Poprawność odpowiedzi i zapis
    correct_letters = sum([1 for i in range(len(sequence)) if i < len(response) and response[i] == sequence[i]])
    math_accuracy = round((math_correct_count / set_size) * 100)
    avg_rt = round(sum(math_rts) / len(math_rts), 3)

    with open(output_file_o, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([block_label, block_num, set_size, correct_letters, math_accuracy, avg_rt])

    feedback_text = f"Poprawnie przywołane litery: {correct_letters}/{set_size}\n" \
                    f"Poprawność działań matematycznych: {math_accuracy}%\n" \
                    "Naciśnij SPACJĘ, aby przejść dalej."
    show_text_and_wait(feedback_text)


# odpowiedź (litery)
response_text = visual.TextStim(win, text="", pos=(0, 250), color='black', height=30)
instr = visual.TextStim(win, text="""Zaznacz litery w kolejności, w jakiej je widziałeś/widziałaś. \
    Jeżeli nie pamiętasz którejś z liter, wstaw w jej miejsce znak zapytania. \
    \nAby zatwierdzić, naciśnij ENTER.""",
                        pos=(0, 300), color='black', height=20, wrapWidth=700)

# PĘTLA TRENINGOWA
# kliki


show_text_and_wait(
    "Ta część eksperymentu polega wysłuchaniu krótkiej serii dzwiękow. Zapoznaj się z nimi. Przysłuchuj się uważnie oraz wpatruj się w krzyżyk na ekranie. \nNaciśnij SPACJĘ, aby przejść dalej.")
tylko_dzwiek1()


show_text_and_wait(
    "Ta część eksperymentu polega na oszacowaniu długości trwania dźwięku. Za chwilę usłyszysz dźwięk. Potem zostaniesz poproszony o oszacowanie, jak długo go słyszałeś. Staraj się odpowiadać tak, jak ci się wydaje. \nNaciśnij SPACJĘ, aby przejść dalej.")
for i in range(20):
    losowa_dl = random.choice([2, 3, 4, 5, 6, 7, 8])
    jedna_proba_click(seria_num=i + 1, duration_s=losowa_dl, output_file_k=output_file_k, block_type='trening')

# trening ospan
# Instrukcja wstepna
show_text_and_wait(
    "W tej części eksperymentu Twoim zadaniem będzie wykonywanie prostych obliczeń oraz zapamiętywanie wyświetlonych po nich liter. Następnie zaznacz litery w takiej kolejności, w jakiej zostały pokazane. Jeżeli zapomnisz którąś z liter, wstaw w jej miejsce znak zapytania. Staraj się wykonywać zadanie tak szybko i dokładnie, jak potrafisz. Równania rozwiązuj w myślach zanim przejdziesz do ekranu, na którym określisz, czy podany wynik jest prawdziwy czy fałszywy. \nNaciśnij SPACJĘ, aby przejść dalej.")

def trening_ospan():
    trials_amount_t = [2, 3, 3]
    for block_num in range(1, len(trials_amount_t) + 1):
        set_size_t = trials_amount_t[block_num - 1]
        ospan_blok(block_num, set_size_t, output_file_o, "Trening")


show_text_and_wait(
    "Teraz przejdziesz do krótkiej serii treningowej. Naciśnij SPACJĘ, aby rozpocząć."
)
trening_ospan()

# SESJA EKSPERYMENTALNA
def glowny_ospan():
    trials_amount_e = [4, 6, 3, 5, 7, 6, 5, 3, 4, 5, 7, 4, 4, 7, 5]
    for block_num in range(1, len(trials_amount_e) + 1):
        set_size_e = trials_amount_e[block_num - 1]
        tylko_dzwiek2()
        ospan_blok(block_num, set_size_e, output_file_o, "Eksperyment")


# Instrukcja wstepna
show_text_and_wait(
    "Teraz nadszedł czas na ostatnie zadanie. Będziesz rozwiązywać równania oraz zapamiętywać litery. Przed każdą serią równań pojawią się dźwięki. Przysłuchuj się im uważnie, utrzymując wzrok na punkcie fiksacji. \n Naciśnij spację, aby przejść do zadania.")


glowny_ospan()

show_text_and_wait("To już koniec eksperymentu. Dziękujemy za udział! Naciśnij SPACJĘ, aby opuścić eksperyment.")
win.close()
core.quit()
