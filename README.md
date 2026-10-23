# ScamShield AI – hybrid classical + quantum demo module
Files: data.py (synthetic dataset), signs.py (warning signs), quantum.py (4-qubit Qiskit circuit),
train.py (trains classical + quantum models, writes results.json/model.pkl), predict.py (analyze(text)).
Run:  pip install qiskit scikit-learn scipy numpy
      python train.py      # ~1-2 min on CPU
      python -c "import predict; print(predict.analyze('URGENT: your account is blocked, share the OTP'))"
Notes: trained on a SMALL SYNTHETIC dataset; the quantum circuit is run on a classical simulator.
Accuracy on real-world messages is NOT measured. The quantum model is compact (12 params) but less accurate than the classical one here.
