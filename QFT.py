# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:28:25 2022

@author: tosca
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
import matplotlib
import matplotlib.pyplot as plt
import qiskit.result
def QFT(n):
    qc = QuantumCircuit(n)
    for t in range (n):
        qc.h(t)
        i=1
        for c in range(t+1,n):
            phase = np.pi/(2**i)
            qc.cp(phase,c,t)
            i=i*2
        qc.barrier()
    for q in range (int(n/2)):
        qc.swap(q,n-1-q)
    qc.draw(output='mpl')