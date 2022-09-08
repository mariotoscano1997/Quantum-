# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 13:30:29 2022

@author: tosca
"""

import Matrix
import numpy as np 
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
from qiskit.tools.visualization import circuit_drawer
import matplotlib.pyplot as plt
from qiskit.quantum_info import random_statevector
from qiskit.extensions import Initialize
from random import randint
#si devono implementare i vari oracle
def q0_():
    circuit=QuantumCircuit(3)
    return circuit
def balanced_oracle(n):
    circuit= QuantumCircuit(n+1)
    s = []
    for i in range(n):
        s.append(randint(0,1))
    for i in range(n):
        if(s[i]==1):
            circuit.x(i)
        
    print(s)
    circuit.barrier()
    for i in range(n):
        circuit.cx(i,n)
    circuit.barrier()
    for i in range(n):
        if(s[i]==1):
            circuit.x(i)
    circuit.barrier()
    return circuit
def constant_oracle_0(n):
    circuit= QuantumCircuit(n+1)   
    return circuit
def constant_oracle_1(n):
    circuit= QuantumCircuit(n+1)   
    circuit.x(n)
    return circuit
def constant_oracle_random(n):
    circuit= QuantumCircuit(n+1)   
    if(randint(0,1)==1):
        circuit.x(n)
    return circuit
def DJ(oracle,n):
    circuit = QuantumCircuit(n+1, n)
    circuit.x(n)
    circuit.barrier()
    for i in range(n+1):
        circuit.h(i)
    circuit.barrier()
    circuit=circuit.compose(oracle,list(range(n+1)))
    circuit.barrier()
    for i in range(n):
        circuit.h(i)
    circuit.barrier()
    for i in range(n):
        circuit.measure(i,i)
    circuit.barrier()
    #Effettua la simulazione 
    simulator=QasmSimulator()

    compiled_circuit = transpile(circuit,simulator)
    #Compilazione
    job=simulator.run(compiled_circuit, shot=1000)

    #ottiene i risulatati
    results = job.result()
    counts=results.get_counts(circuit)    
    #disegna il circuito
    circuit.draw(output='mpl')
    print(counts)