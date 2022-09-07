# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 11:26:12 2022

@author: tosca
"""

""" QUANTUM """
import numpy as np
"""NOT"""
X = np.array([[0,1],[1,0]])
"""Pauli"""
Z = np.array([[1,0],[0,-1]])
"""Identità"""

I=np.array([[1,0],[0,1]])

def Idt(n):
    if (n==1):
        return I
    else :
        return np.kron(I,Idt(n-1))
    
"""Toffoli"""
Tof = Idt(3)
Tof[6,7]= Tof[7,6] = 1
Tof[6,6]= Tof[7,7] = 0



"""Hadmard"""
H = 1/np.sqrt(2)*np.array([[1,1],[1,-1]])

def Had(n):
    if(n==1):
        return H
    else:
        return np.kron(H,Had(n-1))
    
"""per normalizzare"""
def normalizza(v):
        return v/np.linalg.norm(v) 
"""linalg.norm torna la norma del vettore"""

"""ottenere uno stato tramite bstring, vettore oppure ottenere uno stato randomico"""
def get_state(bstr):
    if(type(bstr)==str):
        n = len(bstr)
        N = 2**n
        state = [0]*N
        pos = int(bstr,2)
        state[pos] = 1
        return np.array(state)
    """ottenere stato da un vettore"""
    if(type(bstr)==list):
        state = list(bstr)   
        return normalizza(np.array(state))
    """ottenere stato randomico"""
    if(type(bstr)==int):
        state = np.random.rand(bstr)
        return normalizza(np.array(state))
'''controlled NOT'''
CX = Idt(2)
crow = CX[2].copy()
trow = CX[3].copy()
CX[2]=trow
CX[3]=crow

'''Reversed controlled NOT'''
RCX = Idt(2)
crow = RCX[1].copy()
trow = RCX[3].copy()
RCX[1]=trow
RCX[3]=crow

"""Misurazione di un vettore"""
def counts(vec):
    print("COUNTS:")
    N=len(vec)
    n=int(np.log2(N))
    formatstr = "{:0>"+str(n)+"b}"
    for i in range(N):
        if(vec[i]**2>0):
            print(" -",formatstr.format(i),np.around((vec[i]**2)*100,decimals=2),"%")
"""Multi Controlled CX"""            
def mcx(n):
    N = 2**n
    M = Idt(n)
    M[-2],M[-1]=M[-1].copy(),M[-2].copy()
    return M
            

def gcx(c,t,n):
    mat = Idt(n)
    formatstr="{:0>"+str(n)+"b}"
    for q in range(2**n):
        v=formatstr.format(q)
        if(v[c]=="0" and v[t]=="0"):
            b=[c for c in v]
            b[c]="1"
            control=int(''.join(b),2)
            b[t]="1"
            target=int(''.join(b),2)
            trow=mat[target].copy()
            crow=mat[control].copy()
            mat[control]=trow
            mat[target]=crow
    return mat
            
def gccx(c1,c2,t,n):
    mat = Idt(n)
    formatstr="{:0>"+str(n)+"b}"
    for q in range(2**n):
        v=formatstr.format(q)
        if(v[c1]=="0" and v[c2]=="0" and v[t]=="0"):
            b = [c for c in v]
            b[c1]="1"
            b[c2]="1"
            control=int(''.join(b),2)
            b[t]="1"
            target=int(''.join(b),2)
            trow=mat[target].copy()
            crow=mat[control].copy()
            mat[control]=trow
            mat[target]=crow
    return mat
            
SWAP = Idt(2)
SWAP[1],SWAP[2]=SWAP[2].copy(),SWAP[1].copy()

def gSwap(r1,r2,n):
    CX1=gcx(r2,r1,n)
    CX2=gcx(r1,r2,n)
    CX3=gcx(r2,r1,n)
    M = np.matmul(CX1,CX2)
    M = np.matmul(M,CX3)
    return M
"""tensor product"""
def tp(ql):
    v=ql[0]
    for q in ql[1::]:
        v=np.kron(v,q)
    return v
def halfAdder(b0,b1):
    inp0 = get_state(str(b0))
    inp1 = get_state(str(b1))
    out0 = get_state("0")
    out1 = get_state("0")
    a1=tp((inp0,inp1,out0,out1))
    """prima barriera"""
    a2=np.matmul(gcx(0,2,4),a1)
    a3=np.matmul(gcx(1,2,4),a2)
    a4=np.matmul(gccx(0,1,3,4),a3)
    """configurazione finale e misuazione"""
    counts(a4)
   
    
    
    
    