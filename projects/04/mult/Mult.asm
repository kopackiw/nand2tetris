// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

(START)

(INIT_ITERATOR)
    @R0
    D=M
    @iterator
    M=D

(INIT_DATA)
    @R1
    D=M
    @data
    M=D

(INIT_ACCUMULATOR)
    @accumulator
    M=0

(ITERATE)
(CHECK_ITERATOR_BOUNDS)
    @iterator
    D=M
    @END_ITERATION
    D;JLE

(INCREMENT_ACCUMULATOR)
    @data
    D=M
    @accumulator
    M=M+D

(DECREMENT_ITERATOR)
    @iterator
    M=M-1

(LOOP_ITERATION)
    @ITERATE
    0;JMP
(END_ITERATION)

(SET_VALUE)
    @accumulator
    D=M
    @R2
    M=D

(END)
    @END
    0;JMP
