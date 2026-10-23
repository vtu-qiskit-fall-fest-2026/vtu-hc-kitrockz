"""Synthetic scam/safe message generator (demo dataset). Train and test use DIFFERENT phrasing banks."""
import random
BANKS=["HDFC","SBI","ICICI","Axis Bank","PayPal","Amazon","Netflix","Paytm"]
def pick(r,l): return r.choice(l)
TRAIN = dict(
 imp=["Dear customer, your {b} account","Alert from {b}: your account","{b} Security: your card","Your {b} KYC"],
 urg=["has been blocked. Verify immediately","will be suspended within 24 hours","needs urgent verification","is locked due to suspicious activity"],
 act=["Click {l} to restore access.","Share the OTP you receive to confirm.","Update your details at {l} now.","Send your PIN and password to reopen it."],
 prize=["Congratulations! You have won {a} in our lucky draw. Pay a small fee to claim your prize at {l}.","You are selected for a free gift card worth {a}. Claim now: {l}","Earn {a} daily from home! No experience needed. Message us today.","Limited offer: double your money in 2 days with crypto. Invest now at {l}"],
 deliv=["Your parcel is held. Pay a customs fee of {a} at {l} to release it.","Delivery failed. Update your address within 12 hours: {l}","Courier alert: confirm your address and pay {a} at {l}"],
 safe=["Hey, are we still meeting for lunch at 1 pm tomorrow?","Your order #{n} has shipped and will arrive on Friday.","Reminder: team meeting moved to 3 pm in room {n}.","Your {b} statement for this month is ready in the app. Never share your OTP with anyone.","Thanks for your payment of {a}. Receipt attached.","Happy birthday! Hope you have a great day.","Can you send me the notes from yesterday's class?","Your appointment is confirmed for Monday at 10 am.","Your OTP is {n}. Do not share it with anyone. Valid for 10 minutes.","Mom: please call me when you reach home.","Your package was delivered to the front desk today.","The project report is due on Friday, let me know if you need help."])
TEST = dict(
 imp=["Notice from {b} support: your profile","{b} Team here. Your wallet","Official {b} message: your login"],
 urg=["is at risk and must be confirmed in the next few hours","shows unusual access, act now or lose it","will be closed today unless you respond"],
 act=["Log in through {l} and enter your password.","Reply with your one-time code to cancel the charge.","Transfer {a} to our safe account to protect your funds."],
 prize=["You are our lucky winner of {a}! Reply with your bank details to receive the reward.","Exclusive job offer: make {a} per week, pay a registration fee at {l}","Your lottery ticket won {a}. Contact us and pay the processing charge."],
 deliv=["We could not deliver your item. Reschedule and pay {a} here: {l}","Post office notice: your parcel will be returned unless you click {l}"],
 safe=["Lunch at the usual place today? I'll book a table.","Your {b} order has been dispatched. Track it in the official app.","Class notes are uploaded to the shared folder.","Your electricity bill of {a} is due next week. Pay via the official app or website.","Verification code {n}. Do not share this code with anyone, including {b} staff.","See you at the gym at 6 pm!","The cab is arriving in 5 minutes, license plate ends in {n}.","Your library book is due on Monday."])
def _fill(r,s):
    return s.format(b=pick(r,BANKS),l=pick(r,["http://bit.ly/x7Qa2","http://secure-login-verify.example/acc","https://tinyurl.com/k9d2","http://bank-update.example/kyc"]),
                    a=pick(r,["Rs 50,000","$1,000","Rs 499","Rs 25 lakh","$250"]),n=r.randint(1000,99999))
def make(bank,n,seed):
    r=random.Random(seed); X=[];y=[]
    for _ in range(n):
        if r.random()<0.5:
            k=r.random()
            if k<0.5: s=f"{pick(r,bank['imp'])} {pick(r,bank['urg'])}. {pick(r,bank['act'])}"
            elif k<0.78: s=pick(r,bank['prize'])
            else: s=pick(r,bank['deliv'])
            X.append(_fill(r,s)); y.append(1)
        else:
            X.append(_fill(r,pick(r,bank['safe']))); y.append(0)
    return X,y
def train_set(n=500): return make(TRAIN,n,1)
def test_in(n=200): return make(TRAIN,n,2)
def test_unseen(n=200): return make(TEST,n,3)
