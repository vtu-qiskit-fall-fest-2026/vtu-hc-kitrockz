import re
RULES=[("Urgent or threatening language",r"urgent|immediately|within \d+ hours|suspend|blocked|locked|act now|closed today|at risk|unless you"),
("Suspicious or shortened link",r"bit\.ly|tinyurl|http://|verify.*\.example|secure-login"),
("Requests OTP, PIN or password",r"\botp\b|one-time code|\bpin\b|password"),
("Requests money or fees",r"pay a|fee|processing charge|transfer .* to our|registration fee|invest"),
("Too-good-to-be-true reward",r"won|winner|prize|lottery|lucky|free gift|earn .* daily|double your money|per week"),
("Impersonates a trusted brand",r"dear customer|security:|official .* message|team here|support:|kyc")]
SAFE_NOTE=re.compile(r"(do not|never) share",re.I)
def warning_signs(t):
    out=[n for n,p in RULES if re.search(p,t,re.I)]
    if SAFE_NOTE.search(t) and "Requests OTP, PIN or password" in out and len(out)==1: out=[]
    return out
