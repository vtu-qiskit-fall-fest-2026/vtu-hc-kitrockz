import json, time, numpy as np
from scipy.optimize import minimize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle, data, quantum as Q
Xtr,ytr=data.train_set(500); Xa,ya=data.test_in(200); Xb,yb=data.test_unseen(200)
vec=TfidfVectorizer(ngram_range=(1,2),min_df=2,sublinear_tf=True); T=vec.fit_transform(Xtr)
clf=LogisticRegression(C=3,max_iter=1000).fit(T,ytr)
svd=TruncatedSVD(Q.NQ,random_state=0).fit(T); sc=StandardScaler().fit(svd.transform(T))
def enc(texts): return np.arctan(sc.transform(svd.transform(vec.transform(texts))))+np.pi/2   # -> (0, pi)
Ftr=enc(Xtr); rng=np.random.RandomState(0); idx=rng.choice(len(Xtr),120,replace=False)
ytr=np.array(ytr)
def loss(th):
    p=np.array([Q.p_scam(Ftr[i],th) for i in idx]); p=np.clip(p,1e-4,1-1e-4)
    return -np.mean(ytr[idx]*np.log(p)+(1-ytr[idx])*np.log(1-p))
best=None
t0=time.time()
for seed in range(2):
    th0=np.random.RandomState(seed).uniform(0,2*np.pi,Q.N_PARAMS)
    r=minimize(loss,th0,method="COBYLA",options={"maxiter":220})
    print("seed",seed,"loss",r.fun,time.time()-t0,flush=True)
    if best is None or r.fun<best.fun: best=r
theta=best.x
def predict(texts):
    T=vec.transform(texts); pc=clf.predict_proba(T)[:,1]
    F=enc(texts); pq=np.array([Q.p_scam(f,theta) for f in F]); return pc,pq,(pc+pq)/2
def metrics(y,p): 
    yh=(np.array(p)>=.5).astype(int); return dict(acc=accuracy_score(y,yh),prec=precision_score(y,yh),rec=recall_score(y,yh),f1=f1_score(y,yh))
res={}
for name,(X,y) in {"in_dist":(Xa,ya),"unseen":(Xb,yb)}.items():
    pc,pq,ph=predict(X); res[name]={"classical":metrics(y,pc),"quantum":metrics(y,pq),"hybrid":metrics(y,ph),"n":len(y)}
res["params"]={"quantum":Q.N_PARAMS,"classical":int(clf.coef_.size+1),"qubits":Q.NQ}
json.dump(res,open("results.json","w"),indent=1); print(json.dumps(res,indent=1))
pickle.dump(dict(vec=vec,clf=clf,svd=svd,sc=sc,theta=theta),open("model.pkl","wb"))
