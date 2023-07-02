from PIL import Image
from tkinter import *
from tkinter import ttk
import collections

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
window.geometry('700x850')

title = Label(window, text="≪•◦ ❈ Simulator Turing Machine ❈ ◦•≫",
              width=700, anchor=N, background="#135589")

title.config(font=("Courier", 20, "bold"), foreground="#3ddad7", padx=10, pady=10)
title.pack(pady=(0, 20))

# Bagian Input 
frameInput = ttk.LabelFrame(window, text="Masukkan angka")
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
entry1 = ttk.Entry(frameInput, textvariable=input1)
entry1.pack(padx=20, pady=20, side=LEFT, anchor=CENTER)
entry2 = ttk.Entry(frameInput, textvariable=input2)
entry2.pack(padx=20, pady=20, side=LEFT, anchor=CENTER)

# Bagian Input simulate
frameInput = ttk.LabelFrame(window, text="Pilih operasi")
frameInput.pack(padx=10, pady=10)

# Frame Operasi
def opt(event):
    global warning
    if operand.get() == "Binary Log" or operand.get() == "!" or operand.get() == "C to K":
        entry2.pack_forget()
        input2.set(0)
    else:
        entry2.pack(padx=20, pady=20, side=LEFT, anchor=CENTER)
        input1.set("")
        input2.set("")
    if operand.get() == "Substraction":
        warning = ttk.Label(frameWarning, text="Masukkan tanda").pack(
            pady=10, side=BOTTOM)
    if operand.get() == "Division" or operand.get() == "Multiplication" or operand.get() == "Addition":
        warning = ttk.Label(frameWarning, text="Masukkan tanda positif (+) atau negatif (-) di setiap angka").pack(
            pady=10, side=BOTTOM)
    else:
        for widget in frameWarning.winfo_children():
            widget.destroy()


# Pilihan Operasi
# option = ttk.OptionMenu(frameInput, operand, "+", "+","-", "*", "/", "!", "%", "^", "log(2)", "C to K", command=opt)
option = ttk.OptionMenu(frameInput, operand, "Addition", "Substraction",
                        "Multiplication", "Division", "Factorial", "Power", "Square Root", "Binary Log", command=opt)
option.pack(padx=20, pady=20, side=LEFT, anchor=CENTER)


# Frame Warning
frameWarning = ttk.Frame(window)
frameWarning.pack()

# Frame Output
frameOutput = ttk.LabelFrame(window, text="Output Tape", width=600, height=   1000,)

# Scrollbar
v = Scrollbar(frameOutput)
h = Scrollbar(frameOutput, orient=HORIZONTAL)
v.pack(side=RIGHT, fill=Y)
h.pack(side=BOTTOM, fill=X)

# Frame Canvas Output Tabel 
canvas = Canvas(frameOutput, width=550, height=200,
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
        box = canvas.create_rectangle(x1, y1, x2+20, y2, fill="#cac7cd")
        label = canvas.create_text((x1+x2)/2 + 10, (y1+y2)/2, text=tape[j])
        if head == j:
            canvas.itemconfig(box, fill="#3ddad7")

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

    #ADDITION SINGLETRACK
    if operand.get() == "Addition":
        # Mengambil tanda positif dan negatif
        int1 = str(input1.get())
        int2 = str(input2.get())
        
        if int1 == '0':
            inputString = "1" + int2[0] + temp2

        elif int2 == '0':
            inputString = int1[0] + temp1 + "1"
        

        else:
            inputString = int1[0] + temp1 + "1" + int2[0] + temp2

        # inputString = int1[0] + temp1 + "a" + int2[0] +temp2
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
        R, L, B = 'R', 'L', 'B'
        # Simbol Pertambahan
        a = '1'
        increment = 0
        # Perpindahan State 
        while(oldHead != head):
            oldHead = head
            print(tape, ", head di index ", head, " pada state ", state)
            drawInline(inputLength, x1, x2, y1+increment,
                       y2+increment, 0, tape, head)
            increment += 40
            if state == 0:
                if action('+',B, R, 1) or action('-', B, R, 7) or action(a,B,R,23):
                    pass

            elif state == 1:
                if action('0', B, R, 2) or action(a,B,R,23):
                    pass

            elif state == 2:
                if action('0','0', R, 2) or action('+','+', R, 2) or action(a,a, R, 2) or action(B,'0',L,3) or action('-','-',R,18):
                    pass

            elif state == 3:
                if action('0', '0', L, 3) or action('-','-', L, 3) or action(a,a,L,3) or action('+','+',L,3) or action(B,B,R,4):
                    pass

            elif state == 4:
                if action('0', B, R, 2) or action(a,a, R, 5):
                    pass

            elif state == 5:
                if action(a, B, L, 23) or action('+','+',L,5) or action('-','-',L,5) or action('0','0',L,6):
                    pass

            elif state == 6:
                if action(a, '+', L, 23):
                    pass
            
            elif state == 7:
                if action('0',B, R,8):
                    pass

            elif state == 8:
                if action(a, a, R, 8) or action('0','0', R, 8) or action('+','+',R,8) or action(B,B,L,9) or action('-','-',R,14):
                    pass
            
            elif state == 9:
                if action('+', B, L, 25) or action('0',B, L, 10) or action(a,'0',L,26):
                    pass
            
            elif state == 10:
                if action('0', '0', L, 10) or action(a,a, L, 10) or action ('+','+',L,10) or action(B,B,R,11):
                    pass
            
            elif state == 11:
                if action('0', B,R, 8) or action(a,a, R, 11) or action('+','+',R,12):
                    pass
            
            elif state == 12:
                if action('0', '0', L, 24) or action(B,B, L, 13):
                    pass
            
            elif state == 13:
                if action(a, B, L, 13) or action('0','0', L, 13) or action('+',B,L,13) or action(B,'-',L,23):
                    pass
            
            elif state == 14:
                if action('0', '0', R, 14) or action(a,a, R, 14) or action (B,'0',L,15) or action('-','-',R,14):
                    pass
            
            elif state == 15:
                if action('-', '-', L, 15) or action('0','0', L, 15) or action(B,B,R,16) or action(a,a,L,15):
                    pass
            
            elif state == 16:
                if action(a, B, L, 23) or action('0',B,R,14):
                    pass

            elif state == 17:
                if action(B, '-', L, 23) or action('0','0',L,17):
                    pass
            
            elif state == 18:
                if action('0', '0', R, 18) or action(B,B,L,19):
                    pass
            
            elif state == 19:
                if action('0', B, L, 20):
                    pass
            
            elif state == 20:
                if action('0', '0', L, 21) or action('-',B,L,22):
                    pass
            
            elif state == 21:
                if action('0', '0', L, 21) or action('-','-',L,21) or action(a,a,L,21) or action(B,B,R,1):
                    pass

            elif state == 22:
                if action(a, B, L, 22) or action('0','0',L,22) or action(B,'+',L,23):
                    pass

            elif state == 23:
                    acc = True
                    pass
            
            elif state == 24:
                if action('+', '+', L, 24) or action(a,B,L,23):
                    pass

            elif state == 25:
                if action(a, '0', L, 17):
                    pass
            
            elif state == 26:
                if action('0', '0', L, 26) or action(B,'-',R,23):
                    pass
        #Menghitung jumlah 0 pada final state untuk Hasil
            # elements_count = collections.Counter(tape)
            if acc:
                # Mengambil tanda negatif atau positif dari final state
                for tapes in tape:
                    if tapes == '+':
                        operator = '+'
                    elif tapes == '-':
                        operator = '-'

                if elements_count['0'] == 0:
                    print("Input halt dan diterima di state: ", state,
                    " dengan hasil: 0")

                    # RESULT | labels
                    ttk.Label(frameResult, text="Result: 0").pack(pady=5)

                else:
                    print("Input halt dan diterima di state: ", state,
                    " dengan hasil: ", operator, elements_count['0'])

        
    # Operasi -
    elif operand.get() == "Substraction":
            int1 = str(input1.get())
            int2 = str(input2.get())

            if int1 == '0':
                inputString = "1" + int2[0] + temp2

            elif int2 == '0':
                inputString = int1[0] + temp1 + "1"

            else:
                inputString = int1[0] + temp1 + "1" + int2[0] + temp2
            
            inputLength = len(inputString) * 3
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
            R, L, B = 'R', 'L', 'B'

            increment = 0
            # Perpindahan state
            while(oldHead != head):
                oldHead = head
                print(tape, ", head di index ", head, " pada state ", state)
                drawInline(inputLength, x1, x2, y1+increment,
                           y2+increment, 0, tape, head)
                increment += 40
                if state == 0:
                    if action('1', 'B', R, 1) or action('+', '+', R, 2) or action('-', '-', R, 5):
                        pass

                elif state == 1:
                    if action('+', '-', R, 1) or action('-', '+', R, 1):
                        acc = True

                elif state == 2:
                    if action('0', '0', R, 2) or action('1', '1', R, 2) or action('+', '+', R, 6) or action('-', '-', R, 23) or action(B, B, L, 3):
                        pass

                elif state == 3:
                    if action('1', 'B', L, 4):
                        pass

                elif state == 4:
                    acc = True

                elif state == 5:
                    if action('0', '0', R, 5) or action('1', '1', R, 5) or action('+', '+', R, 23) or action('-', '-', R, 6) or action(B, B, L, 3):
                        pass

                elif state == 6:
                    if action('0', '0', R, 6) or action('1', '1', R, 6) or action('+', '+', R, 6) or action('-', '-', R, 6) or action(B, B, L, 7):
                        pass

                elif state == 7:
                    if action('0', 'B', L, 14) or action('1', 'B', L, 8) or action('+', 'B', L, 7) or action('-', 'B', L, 7):
                        pass

                elif state == 8:
                    if action('0', '0', L, 8) or action('+', 'B', R, 9) or action('-', 'B', R, 12) or action(B, B, L, 8):
                        pass

                elif state == 9:
                    if action('0', '0', L, 10) or action(B, B, R, 9):
                        pass

                elif state == 10:
                    if action(B, '+', L, 11):
                        pass

                elif state == 11:
                    acc = True

                elif state == 12:
                    if action('0', '0', L, 13) or action(B, B, R, 12):
                        pass

                elif state == 13:
                    if action(B, '-', L, 11):
                        pass

                elif state == 14:
                    if action('0', '0', L, 14) or action('1', '1', L, 14) or action('+', '+', L, 14) or action('-', '-', L, 14) or action(B, B, R, 15):
                        pass

                elif state == 15:
                    if action('0', 'B', R, 16) or action('+', '+', R, 15) or action('-', '-', R, 15):
                        pass

                elif state == 16:
                    if action('0', '0', R, 6) or action('1', 'B', R, 17):
                        pass

                elif state == 17:
                    if action('0', '0', L, 18) or action('+', '+', R, 17) or action('-', '-', R, 17) or action(B, B, L, 21):
                        pass

                elif state == 18:
                    if action('+', '-', L, 22) or action('-', '+', L, 19):
                        pass

                elif state == 19:
                    if action('-', 'B', L, 20) or action(B, B, L, 19):
                        pass

                elif state == 20:
                    acc = True

                elif state == 21:
                    if action('+', 'B', L, 22) or action('-', 'B', L, 19):
                        pass

                elif state == 22:
                    if action('+', 'B', L, 20) or action(B, B, L, 22):
                        pass

                elif state == 23:
                    if action('0', '0', R, 23) or action('1', '1', R, 23) or action('+', '+', R, 23) or action('-', '-', R, 23) or action(B, '0', L, 24):
                        pass

                elif state == 24:
                    if action('0', '0', L, 24) or action('1', '1', L, 24) or action('+', '+', L, 24) or action('-', '-', L, 24) or action(B, B, R, 25):
                        pass

                elif state == 25:
                    if action('0', 'B', R, 26) or action('+', 'B', R, 25) or action('-', 'B', R, 25):
                        pass

                elif state == 26:
                    if action('0', '0', R, 23) or action('1', 'B', R, 27):
                        pass

                elif state == 27:
                    if action('+', '-', L, 28) or action('-', '+', L, 28):
                        pass

                elif state == 28:
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

                if elements_count['0'] == 0:
                    print("Input halt dan diterima di state: ", state,
                    " dengan hasil: 0")

                    # RESULT | labels
                    ttk.Label(frameResult, text="Result: 0").pack(pady=5)

                else:
                    print("Input halt dan diterima di state: ", state,
                    " dengan hasil: ", operator, elements_count['0'])

                    # RESULT | labels
                    ttk.Label(frameResult, text="Result: ").pack(pady=5)
                    ttk.Label(frameResult, text=operator).pack(side=LEFT)
                    ttk.Label(frameResult, text=elements_count['0']).pack()

            else:
                print("Input tidak diterima di state: ", state)
                ttk.Label(frameResult, text="Input declined on state: ").pack(
                    pady=10)
                ttk.Label(frameResult, text=state).pack()

            

    # Operasi MULTIPLICATION SINGLETTRACK
    elif operand.get() == "Multiplication":
        # Mengambil tanda positif dan negatif
        int1 = str(input1.get())
        int2 = str(input2.get())

        inputString = int1[0] + temp1 + "1" + int2[0] + temp2 + "1"
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
        X, R, L, B,= 'X', 'R', 'L', 'B'
        # Simbol *
        m = '1'

        increment = 0
        # Perpindahan state
        

        while(oldHead != head and head != -1):
            oldHead = head
            print(tape, ", head di index ", head, " pada state ", state)
            drawInline(inputLength, x1, x2, y1+increment,
                       y2+increment, 0, tape, head)
            increment += 40
            if state == 0:
                if action(B, B, R, 1):
                    pass

            if state == 1:
                if action('-', B, R, 2) or action(m, m, R, 16) or action('+', B, R, 14):
                    pass

            elif state == 2:
                if action('0', '0', R, 2) or action(m, m, R, 2) or action('+', m, R, 3) or action('-', m, R, 15) or action(B, B, L, 18):
                    pass

            elif state == 3:
                if action('0', '0', R, 3) or action(m, m, R, 3) or action(B, '-', L, 4):
                    pass

            elif state == 4:
                if action('0', '0', L, 4) or action('1', '1', L, 4) or action(B, B, R, 5):
                    pass

            elif state == 5:
                if action('0', B, R, 6) or action(m, B, R, 21):
                    pass

            elif state == 6:
                if action('0', '0', R, 6) or action(m, m, R, 7):
                    pass

            elif state == 7:
                if action('0', X, R, 8) or action(m, m, R, 7):
                    pass

            elif state == 8:
                if action('0', '0', R, 8) or action(m, m, R, 9):
                    pass

            elif state == 9:
                if action('0', '0', R, 9) or action('+', "+", R, 9) or action('-', "-", R, 9) or action(B, "0", L, 10):
                    pass

            elif state == 10:
                if action('0', '0', L, 10) or action('+', '+', L, 10) or action('-', '-', L, 10) or action(m, m, L, 11):
                    pass

            elif state == 11:
                if action('0', '0', L, 12) or action(X, '0', L, 13):
                    pass

            elif state == 12:
                if action('0', '0', L, 12) or action(X, X, R, 7):
                    pass

            elif state == 13:
                if action(X, '0', L, 13) or action('0', '0', L, 13) or action(m, m, L, 13) or action(B, B, R, 5):
                    pass

            elif state == 14:
                if action('0', '0', R, 14) or action(m, m, R, 14) or action('-', m, R, 3) or action(B, B, L, 18) or action('+', m, R, 15):
                    pass

            elif state == 15:
                if action('0', '0', R, 15) or action(m, m, R, 15) or action(B, '+', L, 4):
                    pass

            elif state == 16:
                if action('0', '0', R, 16) or action('+', '+', R, 16) or action('-', '-', R, 16) or action(m, m, R, 17):
                    pass

            elif state == 17:
                if action(m, m, R, 17) or action(B, B, L, 18):
                    pass
            
            elif state == 18:
                if action('0', '0', L, 18) or action(m, m, L, 18) or action('+', '+', L, 18) or action('-', '-', L, 18) or action(B, B, R, 19):
                    pass
            
            elif state == 19:
                if action('0', B, R, 19) or action(m, B, R, 19) or action('+', B, R, 19) or action('-', B, R, 19) or action(B, 1, L, 20):
                    pass

            elif state == 20:
                    acc = True

            elif state == 21:
                if action(m, B, R, 22):
                    pass    

            elif state == 22:
                if action('0', B, R, 22) or action(m, B, R, 23):
                    pass     

            elif state == 23:
                if action('0', '0', R, 23) or action('+', '+', R, 23) or action('-', '-', R, 23) or action('B', B, L, 24):
                    pass 

            elif state == 24:
                    acc = True

    # OPERASI /
    elif operand.get() == "Division":
        # Ambil tanda positif dan negatif dari input
        int1 = str(input1.get())
        int2 = str(input2.get())

        inputString = int2[0] + temp2 + "1" + int1[0] + temp1 + "1"
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
        d = '1'
        increment = 0
        # Perpindahan state
        while(oldHead != head):
            oldHead = head
            print(tape, ", head di index ", head, " pada state ", state)
            drawInline(inputLength, x1, x2, y1+increment,
                       y2+increment, 0, tape, head)
            increment += 40
            if state == 0:
                # if action('+', B, R, 1) or action('-', B, R, 5):
                    # pass
                if action('0', '0', R, 0) or action(d, d, R, 0) or action('+', '+', R, 0) or action('-', '-', R, 0) or action(B, B, L, 1):
                    pass 

            elif state == 1:
                # if action('0', '0', R, 1) or action(d, d, R, 1) or action('+', X, R, 2) or action('-', X, R, 4):
                    # pass
                if action('0', '0', L, 1) or action(d, d, L, 1) or action('+', '+', L, 1) or action('-', '-', L, 1) or action(B, B, R, 2):
                    pass

            elif state == 2:
                # if action('0', '0', R, 2) or action(d, d, R, 2) or action(B, '+', L, 3):
                    # pass
                if action('0', B, R, 11) or action('+', B, R, 4) or action('-', B, R, 3) or action(d, d, R, 8):
                    pass

            elif state == 3:
                # if action('0', '0', L, 3) or action(d, d, L, 3) or action(X, X, L, 3) or action(B, B, R, 6):
                    # pass
                if action(d, d, R, 3) or action('0', '0', R, 3) or action('+', B, R, 5) or action('-', B, R, 6):
                    pass

            elif state == 4:
                # if action('0', '0', R, 4) or action(d, d, R, 4) or action(B, '-', L, 3):
                   # pass
                if action('0', '0', R, 4) or action(d, d, R, 4) or action('+', B, R, 6) or action('-', B, R, 5):
                    pass

            elif state == 5:
                # if action('0', '0', R, 5) or action(d, d, R, 5) or action('-', X, R, 2) or action('+', X, R, 4):
                  #  pass
                if action('0', '0', R, 5) or action(d, d, R, 5) or action(B, '-', L, 7):
                    pass
            
            elif state == 6:
                # if action('0', B, R, 7) or action(d, d, R, 10):
                  #  pass
                if action('0', '0', R, 6) or action(B, '+', L, 7) or action(d, d, R, 6):
                    pass

            elif state == 7:
                # if action('0', '0', R, 7) or action(d, d, R, 8):
                  #  pass
                if action('0', '0', L, 7) or action(d, d, L, 7) or action(B, B, L, 1):
                    pass

            elif state == 8:
                # if action('0', X, L, 9) or action(X, X, R, 8) or action(d, B, L, 12):
                  #  pass
                if action('0', '0', R, 8) or action(d, d, R, 8) or action(B, B, R, 8) or action(X, X, R, 8) or action('-', '-', R, 9) or action('+', '+', R, 9):
                    pass

            elif state == 9:
                # if action(X, X, L, 9) or action(d, d, L, 9) or action('0', '0', L, 9) or action(B, '0', R, 6):
                  #  pass
                if action('0', '0', R, 9) or action(B, '0', L, 10):
                    pass

            elif state == 10:
                # if action('0', '0', R, 10) or action(d, d, R, 10) or  action(X, X, R, 10) or  action('-', '-', R, 10) or  action('+', '+', R, 10) or action(B, '0', L, 11):
                  #  pass
                if action('0', '0', L, 10) or action(d, d, L, 10) or action(B, B, L, 1) or action(X, X, L, 10) or action('-', '-', L, 10) or action('+', '+', L, 10):
                    pass

            elif state == 11:
                # if action('0', '0', L, 11) or action(d, d, L, 11) or  action(X, X, L, 11)  or  action('-', '-', L, 11) or  action('+', '+', L, 11) or action(B, B, R, 6):
                  #  pass
                if action('0', '0', R, 11) or action(d, d, R, 12):
                    pass

            elif state == 12:
                # if action(X, B, L, 12) or action(d, B, L, 12) or action('0', B, L, 12) or action(B, B, R, 13):
                  #  pass
                if action('0', X, L, 13) or action(B, B, R, 12) or action(X, X, R, 12) or action(d, d, R, 15):
                    pass

            elif state == 13:
                # if action(X, B, L, 12) or action(d, B, L, 12) or action('0', B, L, 12) or action(B, B, R, 13):
                  #  pass
                if action(B, B, L, 14) or action(X, X, L, 13):
                    pass

            elif state == 14:
                if action('0', '0', L, 14) or action(B, '0', R, 2) or action(d, d, L, 14):
                    pass
        
            elif state == 15:
                if action('-', '-', L, 16) or action('+', '+', L, 16):
                    pass
        
            elif state == 16:
                if action(d, B, L, 17) or action('0', B, L, 18):
                    pass
        
            elif state == 17:
                # if action(X, B, L, 17) or action(B, B, L, 18):
                  #  pass
                # if action(X, B, L, 17) or action(B, B, L, 17) or action(d, B, L, 17) or action('0', B, L, 18):
                  #  pass
                if action('0', B, L, 18) or action(X, B, L, 17) or action(B, B, L, 16):
                    pass
        
            elif state == 18:
                # if action(d, B, L, 18) or action('0', B, L, 18) or action(B, B, L, 18):
                  #  pass
                if action('0', B, L, 18) or action(B, B, L, 19):
                   pass
        
            elif state == 19:
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
            ttk.Label(frameResult, text="Result: ").pack(pady=5)
            ttk.Label(frameResult, text=operator).pack(side=LEFT)
            ttk.Label(frameResult, text=elements_count['0']).pack()
        else:
            print("Input tidak diterima di state: ", state)
            ttk.Label(frameResult, text="Input declined on state: ").pack(
                pady=10)
            ttk.Label(frameResult, text=state).pack()

        
     # Operasi !
    elif operand.get() == "Factorial":
        if temp1 != "":
            inputString = temp1 + "1"
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
            X, R, L, B = 'X', 'R', 'L', 'B'
            d = 1
            increment = 0
            # Perpindahan state
            while(oldHead != head):
                oldHead = head
                print(tape, ", head di index ", head, " pada state ", state)
                drawInline(inputLength, x1, x2, y1+increment,
                           y2+increment, 0, tape, head)
                increment += 40
                if state == 0:
                    if action('0', 'X', R, 1) or action('1', '1', R, 3):
                        pass

                elif state == 1:
                    if action('0', '0', R, 1) or action('1', '1', R, 1) or action(B, '0', L, 2):
                        pass

                elif state == 2:
                    if action('1', '1', L, 2) or action('0', '0', L, 2) or action(X, X, R, 0):
                        pass

                elif state == 3:
                    if action('0', '0', R, 3) or action('B', '1', L, 4):
                        pass

                elif state == 4:
                    if action('0', '0', L, 4) or action('1', '1', L, 4) or action(X, '0', L, 4) or action(B, B, R, 5):
                        pass

                elif state == 5:
                    if action('0', B, R, 6):
                        pass

                elif state == 6:
                    if action('1', '1', L, 13) or action('0', X, R, 7):
                        pass

                elif state == 7:
                    if action('1', '1', R, 8) or action('0', '0', R, 7):
                        pass

                elif state == 8:
                    if action('0', X, R, 9) or action('1', '1', L, 11):
                        pass

                elif state == 9:
                    if action('0', '0', R, 9) or action('1', '1', R, 9) or action(B, '0', L, 10):
                        pass

                elif state == 10:
                    if action('1', '1', L, 10) or action('0', '0', L, 10) or action(X, X, R, 8):
                        pass

                elif state == 11:
                    if action('1', '1', L, 12) or action(X, '0', L, 11):
                        pass

                elif state == 12:
                    if action('0', '0', L, 12) or action('1', '1', L, 12) or action(X, X, R, 6):
                        pass

                elif state == 13:
                    if action('1', '1', L, 13) or action('0', '0', L, 13) or action(X, X, L, 13) or action(B, B, R, 14):
                        pass

                elif state == 14:
                    if action(X, B, R, 15) or action('1', B, R, 22):
                        pass

                elif state == 15:
                    if action(X, X, R, 16) or action('1', B, R, 19):
                        pass

                elif state == 16:
                    if action('1', '1', R, 17) or action(X, X, R, 16) or action('0', '0', R, 16):
                        pass

                elif state == 17:
                    if action(X, X, R, 17) or action('1', '1', L, 18) or action('0', '0', R, 17):
                        pass

                elif state == 18:
                    if action('0', X, L, 13) or action(X, X, L, 18) or action('1', X, L, 13):
                        pass

                elif state == 19:
                    if action('1', B, R, 23) or action(X, X, R, 20) or action('0', B, R, 19):
                        pass

                elif state == 20:
                    if action(X, X, R, 20) or action('0', '0', R, 20) or action('1', '1', R, 20) or action(B, '1', L, 21):
                        pass

                elif state == 21:
                    if action(X, '0', R, 21) or action('0', '0', L, 21) or action('1', '1', L, 21) or action(B, B, R, 6):
                        pass

                elif state == 22:
                    if action('1', B, R, 22) or action('0', '0', R, 22) or action(B, B, L, 23):
                        pass

                elif state == 23:
                    acc = True
                    pass

            # Menghitung jumlah 0 pada final state untuk Hasil
            elements_count = collections.Counter(tape)
            if acc:
                print("Input halt dan diterima di state: ", state,
                      " dengan hasil: ", elements_count['0'])
                # RESULT | labels
                ttk.Label(frameResult, text="Result: ").pack(pady=10)
                ttk.Label(frameResult, text=elements_count['0']).pack()
            else:
                print("Input tidak diterima di state: ", state)
                ttk.Label(frameResult, text="Input declined on state: ").pack(
                    pady=10)
                ttk.Label(frameResult, text=state).pack()
        else:
            print("Input tidak bisa diproses")
            ttk.Label(frameResult, text="Input can't be processed").pack(pady=10)
            

    # Operasi %
    elif operand.get() == "Square Root":
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

           
   
    # Operasi ^
    elif operand.get() == "Power":
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

        

    # Operasi LOG(2) SINGLETRACK
    elif operand.get() == "Binary Log":
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
                    if action('0', '0', R, 0) or action(B, B, L, 1):
                        pass

                elif state == 1:
                    if action('0', '0', L, 2) or action(B, B, L, 13):
                        pass

                elif state == 2:
                    if action('0', '0', L, 3) or action(B, B, R, 12):
                        pass

                elif state == 3:
                    if action('0', X, L, 4) or action(B, B, R, 12):
                        pass

                elif state == 4:
                    if action('0',X, R, 5) or action(X, X, L, 4) or action(B, B, R, 8):
                        pass

                elif state == 5:
                    if action(X, X, R, 5) or action(Y, Y, R, 5) or action('0', '0', R, 5) or action(B,B,L,6):
                        pass

                elif state == 6:
                    if action('0', Y, L, 6) or action(X, '0', L, 7) or action(Y, '0', L, 7):
                        pass

                elif state == 7:
                    if action(Y, Y, L, 7) or action('0', '0', L, 7) or action(X, X, L, 4):
                        pass

                elif state == 8:
                    if action(X, B, R, 8) or action('0', '0', R, 8) or action(Y,Y,R,8) or action(B,B,L,9):
                        pass

                elif state == 9:
                    if action(Y, '0', L, 9) or action('0', '0', L, 10):
                        pass

                elif state == 10:
                    if action(Y, '0', L, 10) or action('0', '0', L, 11) or action(B, B, R, 12):
                        pass

                elif state == 11:
                    if action('0', '0', L, 11) or action(Y,'0',L,11) or action(B,B,R,13):
                        pass

                elif state == 12:
                    if action('0',B, R, 13):
                        pass

                elif state == 13:
                    acc = True

            
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

            

ttk.Style().configure("TButton", padding=5, relief="flat")
submit = ttk.Button(frameInput, text="Simulate", command=caller, width=9)
reset = ttk.Button(frameInput, text="Reset", command=restart, width=7)
reset.pack(side=RIGHT, anchor=CENTER, padx=10,)
submit.pack(side=RIGHT, anchor=CENTER, padx=10,)

window.mainloop()
