# In __init__.py, replace this:
# from .qubit import Qubit

# With this:
from quantum_computing.qubit import Qubit
from quantum_computing.gates import QuantumGate, CNOTGate, PhaseGate, TGate, ControlledGate
from quantum_computing.circuit import QuantumCircuit
from quantum_computing.algorithms import GroverCircuit, QFTCircuit
from quantum_computing.quantum_language import QuantumLanguage
