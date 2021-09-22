# Instruction-Set-Simulator
it mimics the behavior of a mainframe or microprocessor by "reading" instructions and maintaining internal variables which represent the processor's registers
and flags. This simulator has its own Instruction Set Architecture ( ISA )  and it follow VON NEUMANN ARCHITECTURE 
**************************************************************************************************************************************************************
A synopsis of the ISA is given below ( you can read the pdf for the complete discription of the ISA )

The ISA has 7 general purpose registers and 1 flag register. The ISA supports an address size
of 8 bits, which is double byte addressable. Therefore, each address fetches two bytes of
data. This results in a total address space of 512 bytes. This ISA only supports whole
number arithmetic. If the subtraction results in a negative number; for example “3 - 4”, the reg
value will be set to 0 and overflow bit will be set. All the representations of the number are
hence unsigned.
The registers in assembly are named as R0, R1, R2, ... , R6 and FLAGS. Each register is 16
bits.

**************************************************************************************************************************************************************
There is a sample test case input file, you can take a look how input file look like and there is the correspoindig output file for the same. 
The output file keeps track of flags and values stored in registers after execution of every instruction. At the end of the execution there is a memory dump 
of 256 lines. Memory dump describes how variables and program are stored in the same memory.
