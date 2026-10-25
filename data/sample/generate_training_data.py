from pathlib import Path
import random, csv
random.seed(42)
ROOT=Path(__file__).resolve().parent
types=["Website","E-commerce","Mobile App","Data Science","NLP","Dashboard","API"]
complexities=["Low","Medium","High"]
rows=[]
for i in range(500):
    t=random.choice(types); c=random.choice(complexities)
    base={"Low":1,"Medium":1.6,"High":2.5}[c]
    type_hours={"Website":25,"E-commerce":45,"Mobile App":55,"Data Science":35,"NLP":40,"Dashboard":30,"API":28}[t]
    exp=random.randint(1,8); deadline=random.randint(3,45); rev=random.randint(0,5)
    expected=round(type_hours*base*random.uniform(.75,1.25),1)
    hourly=random.choice([600,700,800,900,1000,1200,1500])
    minimum=max(400,hourly-random.choice([50,100,150]))
    budget=round(expected*hourly*random.uniform(.8,1.2),0)
    rush=1.2 if deadline<=7 else 1
    price=round(expected*hourly*rush*(1+0.05*max(0,rev-2))*random.uniform(.9,1.1),0)
    rows.append([t,c,expected,exp,deadline,rev,budget,hourly,minimum,expected,price])
with open(ROOT/"quotation_training.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["project_type","complexity","expected_hours","experience_years","deadline_days","revisions","budget","hourly_rate","minimum_rate","actual_effort_hours","actual_project_price"]); w.writerows(rows)
print("Generated",len(rows),"synthetic records.")
