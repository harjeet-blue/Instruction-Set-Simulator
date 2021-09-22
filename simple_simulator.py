# HARJEET SINGH YADAV 
# IIIT - DELHI
# ROLL NO - 2020561
# BRANCH - CSAI

# uncomment these 2 lines for taking a file as an input through console
# import sys                                    
# code = sys.stdin.read().splitlines()


# uncomment these 2 lines if you want to read your own ( custom )input file
with open('sample_test_case.txt') as f:  # here test_case1.txt is an input file with BINARY CODE
    code = f.read().splitlines()


# ACTUAL CODE STARTS FORM HERE  

# dictionaries to map codes with inst & registers

op_mapping={
    "00000":["add","A"],
    "00001":["sub","A"],
    "00010":["mov","B"],
    "00011":["mov","C"],
    "00100":["ld","D"],
    "00101":["st","D"],
    "00110":["mul","A"],
    "00111":["div","C"],
    "01000":["rs","B"],
    "01001":["ls","B"],
    "01010":["xor","A"],
    "01011":["or","A"],
    "01100":["and","A"],
    "01101":["not","C"],
    "01110":["cmp","C"],
    "01111":["jmp","E"],
    "10000":["jlt","E"],
    "10001":["jgt","E"],
    "10010":["je","E"],
    "10011":["hlt","F"]
}
reg_map={
    "000":0,
    "001":1,
    "010":2,
    "011":3,
    "100":4,
    "101":5,
    "110":6,
    "111":7
}

# falgs 
flags=[0,0,0,0]
registers=[0,0,0,0,0,0,0,flags]


halted = False

# this function handles all operations of type A

def type_a(instr,op1,op2):
    if instr=="add":
        res=op1+op2
        res=overflow(res)
        return res

    elif instr=="sub":
        res=op1-op2
        res=overflow(res)
        return res

    elif instr=="mul":
        res = op1 * op2
        res=overflow(res)
        return res

    elif instr=="xor":
        res=op1^op2
        return res

    elif instr=="or":
        res=op1 | op2
        return res

    elif instr=="and":
        res=op1&op2
        return res

# this function handles all operations of type B

def type_b(instr,imm,reg):
    if instr=="mov":
        return imm

    elif instr=="rs":
        return reg>>imm

    elif instr=="ls":
        return reg<<imm

# this function handles all operations of type C

def type_c(instr,update,op):
    if instr=="mov":
        if op== flags:
            op=int(flag_converter(),2)
        flag_reset()
        return op

    elif instr=="div":
        registers[0]=update/op
        registers[1]=update%op
        return update

    elif instr=="not":
        return op^65535

    elif instr=="cmp":
        if update==op:
            flags[3]=1
        elif update<op:
            flags[1]=1
        else:
            flags[2]=1

        return update

# this function handles all operations of type D

def type_d(instr,mem,reg):
    if instr=="ld":
        return int(memo[mem], 2)

    elif instr=="st":
        memo[mem]=converter_16(reg)
        return reg

# this function handles all operations of type E

def type_e(instr,mem):
    global pc
    if instr=="jmp":
        pc=mem-1
       
    elif instr=="jlt":
        if flags[1]==1:
            pc=mem-1
            
    elif instr=="jgt":
        if flags[2]==1:
            pc=mem-1 

    elif instr=="je":
        if flags[3]==1:
            pc=mem-1
    flag_reset()

# this function handles all operations of type F

def type_f():
    global halted
    halted=True

# this function idefies the type of instruction and calls corresponding function

def reg_alloc(type,line,instr):
    check_for_reset(instr,type)
    if type=="A":
        op1=registers[reg_map[line[10:13]]]
        op2=registers[reg_map[line[13:]]]

        registers[reg_map[line[7:10]]]=type_a(instr,op1,op2)

    elif type=="B":
        imm=int(line[8:],2)
        reg=registers[reg_map[line[5:8]]]

        registers[reg_map[line[5:8]]]=type_b(instr,imm,reg)

    elif type=="C":
        updated=registers[reg_map[line[10:13]]]
        op = registers[reg_map[line[13:]]]

        registers[reg_map[line[10:13]]]=type_c(instr,updated,op)

    elif type=="D":
        mem = int(line[8:], 2)
        y_axis.append(mem)
        x_axis.append(cycle_counter)
        reg = registers[reg_map[line[5:8]]]

        registers[reg_map[line[5:8]]]=type_d(instr,mem,reg)


    elif type=="E":
        mem = int(line[8:], 2)
        type_e(instr,mem)

    else:
        type_f()

# this functions checks the overflow's in the calculations

def overflow(reg):
    if(reg<0):
        reg=0
        flags[0]=1
    
    if(reg>65535):
        flags[0]=1
        reg=lower_16(reg)
    return reg

# A util function for overflow ( takes lower 16 bits in case of an overflow )
def lower_16(n):
    b=bin(n)[2:]
    l=len(b)-16
    n=int(b[l:],2)
    return n

# this function reset the flags after every instruction
def check_for_reset(ins,typ):
    if(ins=="jlt" or ins=="jgt" or ins=="je"):
        return
    if(ins=="mov" and typ=="C"):
        return
    else:
        flag_reset()

# util function for reset flags
def flag_reset():
    for i in range(4):
        flags[i]=0

# util fucntion for print 
def converter_16(num):
    a=bin(int(num))[2:]
    b=(16-len(a))*"0" + a
    return b

#util function for print
def converter_8(num):
    a=bin(int(num))[2:]
    b=(8-len(a))*"0" + a
    return b

#util function for print 
def flag_converter():
    f=12*"0"

    for i in flags:
        f=f+str(i)
    return f

# print the state of registers after execution of every instruction
def write(pc):
    print(converter_8(pc)+" "+converter_16(registers[0])+" "+converter_16(registers[1])+" "+converter_16(registers[2])
          +" "+converter_16(registers[3])+" "+converter_16(registers[4])+" "+converter_16(registers[5])+" "+
          converter_16(registers[6])+" "+flag_converter())


lst="0"*16
memo=[lst]*256

# intialize all 256 memory to 0 at the start of the execution
i=0
for line in code:
    memo[i]=line
    i+=1


pc=0   # this is progrma counter

cycle_counter=0
memory=[]
cycle=[]
y_axis=[]
x_axis=[]


# this loop reads the file line by line and executes
while halted == False:
    opcode=code[pc][:5]
    instr=op_mapping[opcode][0]
    type=op_mapping[opcode][1]
    current = pc
    reg_alloc(type,code[pc],instr)

    cycle.append(cycle_counter)
    memory.append(current)
    cycle_counter+=1

    write(current)
    pc+=1

c=0
# to print the memory dump execution has finshed
for i in memo:
    print(i)
    c+=1

#to plot the graph between the cycle no and corresponding memory address that was being accessed at that time
# #****plotting part***************************
import matplotlib.pyplot as plt
import numpy as np
cycle.extend(x_axis)
memory.extend(y_axis)
plt.scatter(np.array(cycle),np.array(memory),marker="*")
plt.xlabel("cycle")
plt.ylabel("memory")
plt.show()