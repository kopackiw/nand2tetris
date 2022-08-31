// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(START)

(CALCULATE_MAX_SCREEN_OFFSET)
    @8191 // 256 rows with 32 registers
    D=A
    @screen_max
    M=D
    @SCREEN
    D=A
    @screen_max
    M=M+D

(CHECK_FOR_KEY_PRESS)
    @KBD
    D=M
    @FILL_WHITE
    D;JEQ
    @FILL_BLACK
    D;JGT

(FILL_WHITE)
    @color
    M=0
    @INIT_ITERATOR
    D;JEQ

(FILL_BLACK)
    @color
    M=-1
    @INIT_ITERATOR
    D;JEQ

(INIT_ITERATOR)
    @screen_max
    D=M
    @iterator
    M=D

(ITERATE)
(CHECK_ITERATOR_BOUNDS)
    @iterator
    D=M
    @SCREEN
    D=D-A
    @END_ITERATION
    D;JLT

(FILL_REGISTER)
    @color
    D=M
    @iterator
    A=M
    M=D

(DECREMENT_ITERATOR)
    @iterator
    M=M-1

(LOOP_ITERATION)
    @ITERATE
    0;JMP
(END_ITERATION)

(END)
    @START
    0;JMP
