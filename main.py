import streamlit as st

# Restart

def restart():
    canvas.delete("all")
    for widget in frameResult.winfo_children():
        widget.pack_forget()


# Turing Machine State

def action(inputSymbol, inputReplace, movement, nextState):
    global head, state, tape
    if tape[head] == inputSymbol:
        tape[head] = inputReplace
        state = nextState
        if movement == 'R':
            head += 1
        elif movement == 'L':
            head -= 1
        return True
    return False



# Tkinter GUI
window = Tk()
window.title("Simulator Turing Machine")
window.geometry('600x750')

title = Label(window, text="Simulator Turing Machine",
              width=700, anchor=N, background="#D3AB9E")
title.config(font=("Times New Roman", 20), foreground="white", padx=10, pady=10)
title.pack(pady=(0, 20))

# Bagian Input 
frameInput = st.LabelFrame(window, text="Pilih operasi yang akan digunakan lalu masukkan angka")
frameInput.pack(padx=10, pady=10)

# Variabel Input 1 
input1 = StringVar(window)
input1.set("")

# Variabel Pilihan Operasi
operand = StringVar(window)
operand.set("")

# Variabel Input 2
input2 = StringVar(window)
input2.set("")

# Frame Input
entry1 = st.Entry(frameInput, textvariable=input1)
entry1.pack(padx=20, pady=20, side=LEFT, anchor=CENTER)
entry2 = st.Entry(frameInput, textvariable=input2)
entry2.pack(padx=20, pady=20, side=LEFT, anchor=CENTER)

# Frame Operasi
def opt(event):
    global warning
    if operand.get() == "log(2)" or operand.get() == "!" or operand.get() == "C to K":
        entry2.pack_forget()
        input2.set(0)
    else:
        entry2.pack(padx=20, pady=20, side=LEFT, anchor=CENTER)
        input1.set("")
        input2.set("")
    if operand.get() == "-":
        warning = st.Label(frameWarning, text="Masukkan tanda").pack(
            pady=10, side=BOTTOM)
    if operand.get() == "/" or operand.get() == "*":
        warning = st.Label(frameWarning, text="Masukkan tanda positif (+) atau negatif (-) di setiap angka").pack(
            pady=10, side=BOTTOM)
    else:
        for widget in frameWarning.winfo_children():
            widget.destroy()


# Pilihan Operasi
option = st.OptionMenu(frameInput, operand, "+", "+",
                        "-", "*", "/", "!", "%", "^", "log(2)", "C to K", command=opt)
option.pack(padx=20, pady=20, side=LEFT, anchor=CENTER)


# Frame Warning
frameWarning = st.Frame(window)
frameWarning.pack()

# Frame Output
frameOutput = st.LabelFrame(window, text="Hasil", width=600)

# Scrollbar
v = Scrollbar(frameOutput)
h = Scrollbar(frameOutput, orient=HORIZONTAL)
v.pack(side=RIGHT, fill=Y)
h.pack(side=BOTTOM, fill=X)

# Frame Canvas Output Tabel 
canvas = Canvas(frameOutput, width=550, height=400,
                yscrollcommand=v.set, xscrollcommand=h.set)
canvas.pack()

# Canvas Scrollbar
v.config(command=canvas.yview)
h.config(command=canvas.xview)

frameOutput.pack()

# Frame Output Result
frameResult = Frame(window)
frameResult.pack(anchor=CENTER)




# Membuat tabel tapes
def drawInline(inputLength, x1, x2, y1, y2, counter, tape, head):
    for j in range(inputLength):
        x1 += 20
        x2 += 20
        box = canvas.create_rectangle(x1, y1, x2+20, y2, fill="white smoke")
        label = canvas.create_text((x1+x2)/2 + 10, (y1+y2)/2, text=tape[j])
        if head == j:
            canvas.itemconfig(box, fill="yellow")

        canvas.config(scrollregion=(0, 0, x1+40, y1+40))
        canvas.pack(expand=YES, fill=BOTH)
        counter += 1


# TURING MACHINE

def caller():
    global temp1, temp2, head, state, tape, cells
    temp1, temp2 = "", ""

    # Convert Input dari GUI ke CLI
    for i in range(abs(int(input1.get()))):
        temp1 += "0"
    for i in range(abs(int(input2.get()))):
        temp2 += "0"

    # OPERASI +
    if operand.get() == "+":
        inputString = temp1 + "a" + temp2
        inputLength = len(inputString) * 2
        tape = ['B'] * inputLength
        i = 1
        head = 1
        x1, x2 = 0, 0
        y1, y2 = 20, 40
        for char in inputString:
            tape[i] = char
            i += 1
        state = 0
        oldHead = -1
        acc = False
        # Simbol TM
        X, R, L, B = 'X', 'R', 'L', 'B'
        # Simbol Pertambahan
        a = 'a'
        increment = 0
        # Perpindahan State 
        while(oldHead != head):
            oldHead = head
            print(tape, ", head di index ", head, " pada state ", state)
            drawInline(inputLength, x1, x2, y1+increment,
                       y2+increment, 0, tape, head)
            increment += 40
            if state == 0:
                if action('0', X, R, 1) or action(a, B, L, 5):
                    pass

            elif state == 1:
                if action('0', '0', R, 1) or action(a, a, R, 2):
                    pass

            elif state == 2:
                if action('0', '0', R, 2) or action(B, '0', L, 3):
                    pass

            elif state == 3:
                if action('0', '0', L, 3) or action(a, a, L, 4):
                    pass

            elif state == 4:
                if action('0', '0', L, 4) or action(X, X, R, 0):
                    pass

            elif state == 5:
                if action(X, B, L, 5):
                    acc = True
                    pass

        # Menghitung jumlah 0 pada final state untuk Hasil
        elements_count = collections.Counter(tape)
        if acc:
            print("Input halt dan diterima di state : ", state,
                  " dengan hasil: ", elements_count['0'])
            # RESULT | labels
            st.Label(frameResult, text="Hasil : ").pack(pady=10)
            st.Label(frameResult, text=elements_count['0']).pack()
        else:
            print("Input tidak diterima di state : ", state)
            st.Label(frameResult, text="Input tidak diterima di state: ").pack(
                pady=10)
            st.Label(frameResult, text=state).pack()

    # Operasi -
    elif operand.get() == "-":
        if temp1 != "" and temp2 != "" and int(input1.get()) >= int(input2.get()):
            inputString = temp1 + "X" + temp2
            inputLength = len(inputString) * 2
            tape = ['B'] * inputLength
            i = 1
            head = 1
            x1, x2 = 0, 0
            y1, y2 = 20, 40
            for char in inputString:
                tape[i] = char
                i += 1
            state = 0
            oldHead = -1
            acc = False
            # Simbol TM
            X, Y, R, L, B = 'X', 'Y', 'R', 'L', 'B'
            increment = 0
            # Perpindahan state
            while(oldHead != head):
                oldHead = head
                print(tape, ", head di index ", head, " pada state ", state)
                drawInline(inputLength, x1, x2, y1+increment,
                           y2+increment, 0, tape, head)
                increment += 40
                if state == 0:
                    if action('0', '0', R, 0) or action(X, X, R, 1):
                        pass

                elif state == 1:
                    if action('0', '0', R, 1) or action(B, B, L, 2):
                        pass

                elif state == 2:
                    if action('0', B, L, 3) or action(X, B, L, 6):
                        pass

                elif state == 3:
                    if action('0', '0', L, 3) or action(X, X, L, 4):
                        pass

                elif state == 4:
                    if action('0', '0', L, 4) or action(B, B, R, 5):
                        pass

                elif state == 5:
                    if action('0', B, R, 0):
                        pass

                elif state == 6:
                    acc = True

            # Menghitung jumlah 0 pada final state untuk Hasil
            elements_count = collections.Counter(tape)
            if acc:
                print("Input halt dan diterima di state: ", state,
                      " dengan hasil: ", elements_count['0'])
                # RESULT | labels
                st.Label(frameResult, text="Result: ").pack(pady=10)
                st.Label(frameResult, text=elements_count['0']).pack()
            else:
                print("Input tidak diterima di state: ", state)
                st.Label(frameResult, text="Input declined on state: ").pack(
                    pady=10)
                st.Label(frameResult, text=state).pack()
        else:
            print("Input tidak bisa diproses")
            st.Label(frameResult, text="Input can't be processed").pack(pady=10)

     # Operasi *
    elif operand.get() == "*":
        # Mengambil tanda positif dan negatif
        int1 = str(input1.get())
        int2 = str(input2.get())

        inputString = int1[0] + temp1 + "m" + int2[0] + temp2 + "m"
        inputLength = len(inputString) * 3
        tape = ['B'] * inputLength
        i = 1
        head = 0
        x1, x2 = 0, 0
        y1, y2 = 20, 40
        for char in inputString:
            tape[i] = char
            i += 1
        state = 0
        oldHead = -1
        acc = False
        
        # Simbol TM
        X, R, L, B= 'X', 'R', 'L', 'B'
        # Simbol *
        m = 'm'

        increment = 0
        # Perpindahan state
        while(oldHead != head and head != -1):
            oldHead = head
            print(tape, ", head di index ", head, " pada state ", state)
            drawInline(inputLength, x1, x2, y1+increment,
                       y2+increment, 0, tape, head)
            increment += 40
            if state == 0:
                if action('+', B, R, 1) or action(B, B, R, 0) or action('-', B, R, 5):
                    pass

            elif state == 1:
                if action('0', '0', R, 1) or action(m, m, R, 1) or action('+', m, R, 2) or action('-', m, R, 4):
                    pass

            elif state == 2:
                if action('0', '0', R, 2) or action(m, m, R, 2) or action(B, '+', L, 3):
                    pass

            elif state == 3:
                if action('0', '0', L, 3) or action(m, m, L, 3) or action(B, B, R, 6):
                    pass

            elif state == 4:
                if action('0', '0', R, 4) or action(m, m, R, 4) or action(B, '-', L, 3):
                    pass

            elif state == 5:
                if action('0', '0', R, 5) or action(m, m, R, 5) or action('-', m, R, 2) or action('+', m, R, 4):
                    pass

            elif state == 6:
                if action('0', B, R, 7) or action(m, B, R, 15):
                    pass

            elif state == 7:
                if action('0', '0', R, 7) or action(m, m, R, 8):
                    pass

            elif state == 8:
                if action(m, m, R, 8) or action('0', X, R, 9):
                    pass

            elif state == 9:
                if action('0', '0', R, 9) or action(m, m, R, 10):
                    pass

            elif state == 10:
                if action('0', '0', R, 10) or action(B, '0', L, 11) or action('-', '-', R, 10) or action('+', '+', R, 10):
                    pass

            elif state == 11:
                if action('0', '0', L, 11) or action(m, m, L, 12) or action('-', '-', L, 11) or action('+', '+', L, 11):
                    pass

            elif state == 12:
                if action(X, '0', L, 14) or action('0', '0', L, 13):
                    pass

            elif state == 13:
                if action('0', '0', L, 13) or action(X, X, R, 8):
                    pass

            elif state == 14:
                if action(X, '0', L, 14) or action(m, m, L, 14) or action('0', '0', L, 14) or  action(B, B, R, 6):
                    pass

            elif state == 15:
                if action('0', B, R, 15) or action(m, B, R, 16):
                    pass

            elif state == 16:
                if action('0', B, R, 16) or action(m, B, R, 17) or action('-', '-', R, 16) or action('+', '+', R, 16):
                    pass

            elif state == 17:
                    acc = True

        #Menghitung jumlah 0 pada final state untuk Hasil
        elements_count = collections.Counter(tape)
        if acc:
            # Mengambil tanda negatif atau positif dari final state
            for tapes in tape:
                if tapes == '+':
                    operator = '+'
                elif tapes == '-':
                    operator = '-'

            print("Input halt dan diterima di state: ", state,
                " dengan hasil: ", operator, elements_count['0'])
            # RESULT | labels
            st.Label(frameResult, text="Result: ").pack(pady=5)
            st.Label(frameResult, text=operator).pack(side=LEFT)
            st.Label(frameResult, text=elements_count['0']).pack()
        else:
            print("Input tidak diterima di state: ", state)
            st.Label(frameResult, text="Input declined on state: ").pack(
                pady=10)
            st.Label(frameResult, text=state).pack()


    # OPERASI /
    elif operand.get() == "/":
        # Ambil tanda positif dan negatif dari input
        int1 = str(input1.get())
        int2 = str(input2.get())

        inputString = int2[0] + temp2 + "d" + int1[0] + temp1 + "d"
        inputLength = len(inputString) * 2
        tape = ['B'] * inputLength
        i = 1
        head = 1
        x1, x2 = 0, 0
        y1, y2 = 20, 40
        for char in inputString:
            tape[i] = char
            i += 1
        state = 0
        oldHead = -1
        acc = False
        # Simbol TM
        X, R, L, B = 'X', 'R', 'L', 'B'
        # Simbol Pembagian
        d = 'd'
        increment = 0
        # Perpindahan state
        while(oldHead != head):
            oldHead = head
            print(tape, ", head di index ", head, " pada state ", state)
            drawInline(inputLength, x1, x2, y1+increment,
                       y2+increment, 0, tape, head)
            increment += 40
            if state == 0:
                if action('+', B, R, 1) or action('-', B, R, 5):
                    pass 

            elif state == 1:
                if action('0', '0', R, 1) or action(d, d, R, 1) or action('+', X, R, 2) or action('-', X, R, 4):
                    pass

            elif state == 2:
                if action('0', '0', R, 2) or action(d, d, R, 2) or action(B, '+', L, 3):
                    pass

            elif state == 3:
                if action('0', '0', L, 3) or action(d, d, L, 3) or action(X, X, L, 3) or action(B, B, R, 6):
                    pass

            elif state == 4:
                if action('0', '0', R, 4) or action(d, d, R, 4) or action(B, '-', L, 3):
                    pass

            elif state == 5:
                if action('0', '0', R, 5) or action(d, d, R, 5) or action('-', X, R, 2) or action('+', X, R, 4):
                    pass
            
            elif state == 6:
                if action('0', B, R, 7) or action(d, d, R, 10):
                    pass

            elif state == 7:
                if action('0', '0', R, 7) or action(d, d, R, 8):
                    pass

            elif state == 8:
                if action('0', X, L, 9) or action(X, X, R, 8) or action(d, B, L, 12):
                    pass

            elif state == 9:
                if action(X, X, L, 9) or action(d, d, L, 9) or action('0', '0', L, 9) or action(B, '0', R, 6):
                    pass

            elif state == 10:
                if action('0', '0', R, 10) or action(d, d, R, 10) or  action(X, X, R, 10) or  action('-', '-', R, 10) or  action('+', '+', R, 10) or action(B, '0', L, 11):
                    pass

            elif state == 11:
                if action('0', '0', L, 11) or action(d, d, L, 11) or  action(X, X, L, 11)  or  action('-', '-', L, 11) or  action('+', '+', L, 11) or action(B, B, R, 6):
                    pass

            elif state == 12:
                if action(X, B, L, 12) or action(d, B, L, 12) or action('0', B, L, 12) or action(B, B, R, 13):
                    pass

            elif state == 13:
                acc = True

        # Menghitung jumlah 0 pada final state untuk Result
        elements_count = collections.Counter(tape)
        if acc:
            # Mengambil operator pada Final State
            for tapes in tape:
                if tapes == '+':
                    operator = '+'
                elif tapes == '-':
                    operator = '-'

            print("Input halt dan diterima di state: ", state,
                  " dengan hasil: ", elements_count['0'])
            # RESULT | labels
            st.Label(frameResult, text="Result: ").pack(pady=5)
            st.Label(frameResult, text=operator).pack(side=LEFT)
            st.Label(frameResult, text=elements_count['0']).pack()
        else:
            print("Input tidak diterima di state: ", state)
            st.Label(frameResult, text="Input declined on state: ").pack(
                pady=10)
            st.Label(frameResult, text=state).pack()

     # Operasi !
    elif operand.get() == "!":
        if temp1 != "":
            inputString = temp1
            inputLength = len(inputString*3) * 10
            tape = ['B'] * inputLength
            i = 1
            head = 1
            x1, x2 = 0, 0
            y1, y2 = 20, 40
            for char in inputString:
                tape[i] = char
                i += 1
            state = 0
            oldHead = -1
            acc = False
            # TM Simbol
            X, Y, R, L, B = 'X', 'Y', 'R', 'L', 'B'
            increment = 0
            # Perpindahan state
            while(oldHead != head):
                oldHead = head
                print(tape, ", head di index ", head, " pada state ", state)
                drawInline(inputLength, x1, x2, y1+increment,
                           y2+increment, 0, tape, head)
                increment += 40
                if state == 0:
                    if action('0', '0', R, 0) or action(B, '1', L, 1):
                        pass

                elif state == 1:
                    if action('0', '0', L, 1) or action('1', '1', L, 1) or action(B, B, R, 2):
                        pass

                elif state == 2:
                    if action('0', X, R, 3) or action('1', '1', R, 5):
                        pass

                elif state == 3:
                    if action('0', '0', R, 3) or action('1', '1', R, 3) or action(B, '0', L, 4):
                        pass

                elif state == 4:
                    if action('0', '0', L, 4) or action('1', '1', L, 4) or action(X, X, R, 2):
                        pass

                elif state == 5:
                    if action('0', '0', R, 5) or action(B, '1', L, 7):
                        pass

                elif state == 6:
                    if action('0', '0', L, 6) or action('1', '1', L, 6) or action(X, X, L, 6) or action(B, B, R, 16):
                        pass

                elif state == 7:
                    if action('0', '0', L, 7) or action('1', '1', L, 7) or action(X, '0', L, 7) or action(B, B, R, 8):
                        pass

                elif state == 8:
                    if action('0', B, R, 9):
                        pass

                elif state == 9:
                    if action('0', X, R, 10) or action('1', '1', L, 6):
                        pass

                elif state == 10:
                    if action('0', '0', R, 10) or action('1', '1', R, 11):
                        pass

                elif state == 11:
                    if action('0', X, R, 12) or action('1', '1', L, 14):
                        pass

                elif state == 12:
                    if action('0', '0', R, 12) or action('1', '1', R, 12) or action(B, '0', L, 13):
                        pass

                elif state == 13:
                    if action('0', '0', L, 13) or action('1', '1', L, 13) or action(X, X, R, 11):
                        pass

                elif state == 14:
                    if action(X, '0', L, 14) or action('1', '1', L, 15):
                        pass

                elif state == 15:
                    if action('0', '0', L, 15) or action('1', '0', L, 15) or action(X, X, R, 9):
                        pass

                elif state == 16:
                    if action(X, B, R, 17) or action('1', B, R, 25):
                        pass

                elif state == 17:
                    if action('0', B, R, 18) or action('1', B, R, 18) or action(X, X, R, 19) :
                        pass

                elif state == 18:
                    if action('0', B, R, 18) or action(X, X, R, 22) or action('1', B, L, 24):
                        pass

                elif state == 19:
                    if action('0', '0', R, 19) or action(X, X, R, 19) or action('1', '1', R, 20):
                        pass

                elif state == 20:
                    if action('0', '0', R, 20) or action(X, X, R, 20) or action('1', '1', L, 21):
                        pass

                elif state == 21:
                    if action(X, X, L, 21) or action('0', X, L, 6) or action('1', X, L, 6):
                        pass

                elif state == 22:
                    if action('0', '0', R, 22) or action('1', '1', R, 22) or action(X, X, R, 22) or action(B, '1', L, 23):
                        pass

                elif state == 23:
                    if action('0', '0', L, 23) or action('1', '1', L, 23) or action(X, '0', R, 23) or action(B, B, R, 9):
                        pass

                elif state == 24:
                    acc = True
                    pass

                elif state == 25:
                    if action('0', '0', R, 25) or action('1', B, R, 25) or action(B, B, L, 24):
                        pass
            # Menghitung jumlah 0 pada final state untuk Hasil
            elements_count = collections.Counter(tape)
            if acc:
                print("Input halt dan diterima di state: ", state,
                      " dengan hasil: ", elements_count['0'])
                # RESULT | labels
                st.Label(frameResult, text="Result: ").pack(pady=10)
                st.Label(frameResult, text=elements_count['0']).pack()
            else:
                print("Input tidak diterima di state: ", state)
                st.Label(frameResult, text="Input declined on state: ").pack(
                    pady=10)
                st.Label(frameResult, text=state).pack()
        else:
            print("Input tidak bisa diproses")
            st.Label(frameResult, text="Input can't be processed").pack(pady=10)


    # Operasi %
    elif operand.get() == "%":
        if temp1 != "" and temp2 != "":
            inputString = temp1 + "m" + temp2
            inputLength = len(inputString) * 2
            tape = ['B'] * inputLength
            i = 1
            head = 1
            x1, x2 = 0, 0
            y1, y2 = 20, 40
            for char in inputString:
                tape[i] = char
                i += 1
            state = 0
            oldHead = -1
            acc = False
            # Simbol TM
            X, Y, R, L, B = 'X', 'Y', 'R', 'L', 'B'
            # Simbol Modulo
            m = 'm'
            increment = 0
            # Perpindahan state
            while(oldHead != head):
                oldHead = head
                print(tape, ", head di index ", head, " pada state ", state)
                drawInline(inputLength, x1, x2, y1+increment,
                           y2+increment, 0, tape, head)
                increment += 40
                if state == 0:
                    if action('0', '0', R, 0) or action(m, m, R, 1):
                        pass

                elif state == 1:
                    if action('0', '0', R, 1) or action(B, m, L, 2):
                        pass

                elif state == 2:
                    if action(m, m, R, 7) or action('0', X, L, 3):
                        pass

                elif state == 3:
                    if action('0', '0', L, 3) or action(m, m, L, 4):
                        pass

                elif state == 4:
                    if action(B, B, R, 8) or action(Y, Y, L, 4) or action('0', Y, R, 5):
                        pass

                elif state == 5:
                    if action(Y, Y, R, 5) or action(m, m, R, 6):
                        pass

                elif state == 6:
                    if action('0', '0', R, 6) or action(X, X, L, 2):
                        pass

                elif state == 7:
                    if action(m, m, L, 2) or action(X, '0', R, 7):
                        pass

                elif state == 8:
                    if action(Y, B, R, 8) or action(m, B, R, 9):
                        pass

                elif state == 9:
                    if action('0', B, R, 9) or action(X, '0', R, 9) or action(m, B, L, 10):
                        pass

                elif state == 10:
                    if action('0', B, L, 11):
                        pass

                elif state == 11:
                    acc = True

            # Menghitung jumlah 0 pada final state untuk Hasil
            elements_count = collections.Counter(tape)
            if acc:
                print("Input halt dan diterima di state: ", state,
                      " dengan hasil: ", elements_count['0'])
                # RESULT | labels
                st.Label(frameResult, text="Result: ").pack(pady=10)
                st.Label(frameResult, text=elements_count['0']).pack()
            else:
                print("Input tidak diterima di state: ", state)
                st.Label(frameResult, text="Input declined on state: ").pack(
                    pady=10)
                st.Label(frameResult, text=state).pack()
        else:
            print("Input tidak bisa diproses")
            st.Label(frameResult, text="Input can't be processed").pack(pady=10)

   
    # Operasi ^
    elif operand.get() == "^":
        inputString = temp1 
        inputLength = len(inputString) ** 2
        tape = ['B'] * inputLength
        i = 1
        head = 1
        x1, x2 = 0, 0
        y1, y2 = 20, 40
        for char in inputString:
            tape[i] = char
            i += 1
        state = 0
        oldHead = -1
        acc = False
        # TM Simbol
        X, R, L, B, C = 'X', 'R', 'L', 'B', 'C'
        increment = 0
        # Perpindahan state
        while(oldHead != head):
            oldHead = head
            print(tape, ", head di index ", head, " pada state ", state)
            drawInline(inputLength, x1, x2, y1+increment,
                       y2+increment, 0, tape, head)
            increment += 40
            if state == 0:
                if action(C, B, R, 31) or action('0', X, R, 1):
                    pass

            elif state == 1:
                if action(C, C, R, 1) or action('0', '0', R, 1) or action(B, C, L, 2):
                    pass

            elif state == 2:
                if action(C, C, L, 2) or action('0', '0', L, 2) or action(X, X, R, 3):
                    pass

            elif state == 3:
                if action(C, B, L, 13) or action('0', X, R, 4):
                    pass

            elif state == 4:
                if action(C, C, R, 5) or action('0', '0', R, 4):
                    pass

            elif state == 5:
                if action(C, C, R, 9) or action('0', Y, R, 6) or action(Y, Y, R, 5):
                    pass

            elif state == 6:
                if action(C, C, R, 7) or action('0', '0', R, 6):
                    pass

            elif state == 7:
                if action(C, C, R, 7) or action('0', '0', R, 7) or action(B, '0', L, 8):
                    pass

            elif state == 8:
                if action(C, C, L, 8) or action('0', '0', L, 8) or action(Y, Y, R, 5):
                    pass

            elif state == 9:
                if action(C, C, R, 9) or action('0', '0', R, 9) or action(B, C, L, 10):
                    pass

            elif state == 10:
                if action(C, C, L, 10) or action('0', '0', L, 10) or action(Y, '0', L, 11):
                    pass

            elif state == 11:
                if action(C, C, L, 12) or action(Y, '0', L, 11):
                    pass

            elif state == 12:
                if action('0', '0', L, 12) or action(X, X, R, 2):
                    pass

            elif state == 13:
                if action(X, B, L, 13) or action(B, B, R, 14):
                    pass

            elif state == 14:
                if action('0', X, R, 15) or action(B, B, R, 14):
                    pass

            elif state == 15:
                if action(C, C, R, 16) or action('0', '0', R, 15):
                    pass

            elif state == 16:
                if action(C, C, L, 20) or action('0', Y, R, 17) or action(Y, Y, R, 16) or action(B, B, L, 29):
                    pass

            elif state == 17:
                if action(C, C, R, 18) or action('0', '0', R, 17):
                    pass

            elif state == 18:
                if action(C, C, R, 18) or action('0', '0', R, 18) or action(B, '0', L, 19):
                    pass

            elif state == 19:
                if action(C, C, L, 19) or action('0', '0', L, 19) or action(Y, Y, R, 16):
                    pass

            elif state == 20:
                if action(C, C, L, 21) or action(Y, '0', L, 20):
                    pass

            elif state == 21:
                if action('0', '0', L, 22) or action(X, B, L, 23):
                    pass

            elif state == 22:
                if action('0', '0', L, 22) or action(X, X, R, 14):
                    pass

            elif state == 23:
                if action(X, B, L, 23) or action(B, B, R, 24):
                    pass

            elif state == 24:
                if action(C, B, R, 25) or action(B, B, R, 24):
                    pass

            elif state == 25:
                if action(C, B, R, 26) or action('0', B, R, 25):
                    pass

            elif state == 26:
                if action(C, C, R, 27) or action('0', '0', R, 26) or action(B, B, L, 32):
                    pass

            elif state == 27:
                if action(C, C, R, 27) or action('0', '0', R, 27) or action(B, C, L, 28):
                    pass

            elif state == 28:
                if action(C, C, L, 28) or action('0', '0', L, 28) or action(B, B, R, 14):
                    pass

            elif state == 29:
                if action(C, '0', L, 30):
                    pass

            elif state == 30:
                if action('0', '0', L, 30) or action(X, B, R, 26):
                    pass

            elif state == 31:
                if action('0', B, R, 31) or action(B, '0', R, 26):
                    pass

            elif state == 32:
                acc = True

        # Menghitung jumlah 0 pada final state untuk Hasil
        elements_count = collections.Counter(tape)
        if acc:
            print("Input halt dan diterima di state: ", state,
                  " dengan hasil: ", elements_count['0'])
            # RESULT | labels
            st.Label(frameResult, text="Result: ").pack(pady=10)
            st.Label(frameResult, text=elements_count['0']).pack()
        else:
            print("Input tidak diterima di state: ", state)
            st.Label(frameResult, text="Input declined on state: ").pack(
                pady=10)
            st.Label(frameResult, text=state).pack()

    # Operasi log(2)
    elif operand.get() == "log(2)":
        if temp1 != "" and int(input1.get()) % 2 == 0:
            inputString = temp1
            inputLength = len(inputString) * 2
            tape = ['B'] * inputLength
            i = 1
            head = 1
            x1, x2 = 0, 0
            y1, y2 = 20, 40
            for char in inputString:
                tape[i] = char
                i += 1
            state = 0
            oldHead = -1
            acc = False
            # Simbol TM
            X, Y, R, L, B = 'X', 'Y', 'R', 'L', 'B'
            increment = 0
            # Perpindahan state
            while(oldHead != head):
                oldHead = head
                print(tape, ", head di index ", head, " pada state ", state)
                drawInline(inputLength, x1, x2, y1+increment,
                           y2+increment, 0, tape, head)
                increment += 40
                if state == 0:
                    if action('0', '0', R, 1) or action(B, B, R, 12):
                        pass

                elif state == 1:
                    if action('0', '0', R, 2) or action(B, B, L, 11):
                        pass

                elif state == 2:
                    if action('0', X, R, 3) or action(B, B, L, 11):
                        pass

                elif state == 3:
                    if action(X, X, R, 3) or action('0', X, L, 4) or action(B, B, L, 7):
                        pass

                elif state == 4:
                    if action(Y, Y, L, 4) or action('0', '0', L, 4) or action(X, X, L, 4) or action(B, B, R, 5):
                        pass

                elif state == 5:
                    if action('0', Y, R, 5) or action(Y, '0', R, 6) or action(X, '0', R, 6):
                        pass

                elif state == 6:
                    if action(Y, Y, R, 6) or action('0', '0', R, 6) or action(X, X, R, 3):
                        pass

                elif state == 7:
                    if action(Y, Y, L, 7) or action('0', '0', L, 7) or action(X, B, L, 7) or action(B, B, R, 8):
                        pass

                elif state == 8:
                    if action(Y, '0', R, 8) or action('0', '0', R, 9):
                        pass

                elif state == 9:
                    if action(Y, '0', R, 9) or action('0', '0', R, 10) or action(B, B, L, 11):
                        pass

                elif state == 10:
                    if action(Y, '0', R, 10) or action('0', '0', R, 10) or action(B, B, R, 12):
                        pass

                elif state == 11:
                    if action('0', B, R, 12):
                        pass

                elif state == 12:
                    acc = True

            # Menghitung jumlah 0 pada final state untuk Hasil
            elements_count = collections.Counter(tape)
            if acc:
                print("Input halt dan diterima di state: ", state,
                      " dengan hasil: ", elements_count['0'])
                # RESULT | labels
                st.Label(frameResult, text="Result: ").pack(pady=10)
                st.Label(frameResult, text=elements_count['0']).pack()
            else:
                print("Input tidak diterima di state: ", state)
                st.Label(frameResult, text="Input declined on state: ").pack(
                    pady=10)
                st.Label(frameResult, text=state).pack()
        else:
            print("Input tidak bisa diproses")
            st.Label(frameResult, text="Input can't be processed").pack(pady=10)


    # Operasi Celcius ke Kelvin
    elif operand.get() == "C to K":
        if temp1 != "":
            inputString = temp1
            inputLength = len(inputString*3) * 10
            tape = ['B'] * inputLength
            i = 1
            head = 1
            x1, x2 = 0, 0
            y1, y2 = 20, 40
            for char in inputString:
                tape[i] = char
                i += 1
            state = 0
            oldHead = -1
            acc = False
            # TM Simbol
            X, Y, R, L, B, K = 'X', 'Y', 'R', 'L', 'B', 'K'
            increment = 0
            # Perpindahan state
            while(oldHead != head):
                oldHead = head
                print(tape, ", head di index ", head, " pada state ", state)
                drawInline(inputLength, x1, x2, y1+increment,
                        y2+increment, 0, tape, head)
                increment += 40
                if state == 0:
                    if action('0', '0', R, 0) or action(B, K, R, 1):
                        pass

                elif state == 1:
                        acc = True

            # Menghitung jumlah 0 pada final state untuk Hasil
            if acc:
                for i in range(273):
                    tape.append('0')
                elements_count = collections.Counter(tape)
                print("Input halt dan diterima di state: ", state,
                    " dengan hasil: ", elements_count['0'])
                # RESULT | labels
                st.Label(frameResult, text="Result: ").pack(pady=10)
                st.Label(frameResult, text=elements_count['0']).pack()
            else:
                print("Input tidak diterima di state: ", state)
                st.Label(frameResult, text="Input declined on state: ").pack(
                    pady=10)
                st.Label(frameResult, text=state).pack()


st.Style().configure("TButton", padding=5, relief="flat")
submit = st.Button(frameInput, text="run", command=caller, width=7)
reset = st.Button(frameInput, text="reset", command=restart, width=7)
reset.pack(side=RIGHT, anchor=CENTER, padx=10)
submit.pack(side=RIGHT, anchor=CENTER, padx=10)


window.mainloop()
