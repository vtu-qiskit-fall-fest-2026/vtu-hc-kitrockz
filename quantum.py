import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Statevector, SparsePauliOp
NQ=4; LAYERS=2
def build():
    x=ParameterVector("x",NQ); th=ParameterVector("t",NQ*(LAYERS+1))
    qc=QuantumCircuit(NQ)
    for i in range(NQ): qc.ry(x[i],i); qc.rz(x[i],i)          # angle-encode features
    k=0
    for l in range(LAYERS):
        for i in range(NQ): qc.ry(th[k],i); k+=1
        for i in range(NQ): qc.cx(i,(i+1)%NQ)                    # entangle
    for i in range(NQ): qc.ry(th[k],i); k+=1
    return qc,x,th
QC,X,TH=build(); OBS=SparsePauliOp("IIIZ")
N_PARAMS=len(TH)
def p_scam(feat,theta):
    b=QC.assign_parameters({**dict(zip(X,feat)),**dict(zip(TH,theta))})
    ez=Statevector(b).expectation_value(OBS).real
    return float((1-ez)/2)
