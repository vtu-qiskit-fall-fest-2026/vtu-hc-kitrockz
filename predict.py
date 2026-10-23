import pickle, numpy as np, quantum as Q, signs
M=pickle.load(open("model.pkl","rb"))
def enc(t): return np.arctan(M["sc"].transform(M["svd"].transform(M["vec"].transform(t))))+np.pi/2
def analyze(text):
    pc=float(M["clf"].predict_proba(M["vec"].transform([text]))[0,1]); pq=Q.p_scam(enc([text])[0],M["theta"]); ph=(pc+pq)/2
    return dict(text=text,classical=pc,quantum=pq,hybrid=ph,label="HIGH RISK" if ph>=.7 else "SUSPICIOUS" if ph>=.4 else "LOW RISK",signs=signs.warning_signs(text),features=[float(v) for v in enc([text])[0]])
