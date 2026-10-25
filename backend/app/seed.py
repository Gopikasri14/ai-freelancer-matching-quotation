from .db import Base, engine, SessionLocal
from .models import Freelancer

FREELANCERS = [
("Arun Kumar","Full stack developer building responsive web apps.","React, Node.js, MongoDB, JavaScript, HTML, CSS",4,900,700),
("Priya S","Python and data science freelancer.","Python, FastAPI, Pandas, Scikit-learn, Machine Learning, SQL",3,850,650),
("Rahul Dev","Frontend specialist for modern product interfaces.","React, JavaScript, TypeScript, Tailwind, UI, CSS",5,1100,850),
("Meena AI","Machine learning engineer for predictive systems.","Python, XGBoost, Machine Learning, NLP, Pandas, SQL",4,1200,900),
("Karthik Web","WordPress and business website developer.","WordPress, PHP, HTML, CSS, JavaScript, SEO",6,750,550),
("Divya UX","UI/UX designer and frontend developer.","Figma, UI, UX, React, HTML, CSS, Design",4,1000,750),
("Vijay Mobile","Mobile and backend developer.","Flutter, Dart, Firebase, Python, REST API",5,1000,750),
("Nisha Data","Data analyst and dashboard specialist.","Python, SQL, Power BI, Excel, Pandas, Data Analysis",3,800,600),
("Sanjay Cloud","Cloud and DevOps engineer.","AWS, Docker, Kubernetes, Python, CI/CD, Linux",6,1300,1000),
("Anu NLP","NLP and chatbot developer.","Python, NLP, TF-IDF, Transformers, FastAPI, ML",3,1050,800),
]

def main():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    if db.query(Freelancer).count()==0:
        for n,b,s,e,r,m in FREELANCERS:
            db.add(Freelancer(name=n,bio=b,skills=s,experience_years=e,hourly_rate=r,minimum_rate=m))
        db.commit()
        print("Seeded freelancers.")
    else:
        print("Freelancers already exist.")
    db.close()

if __name__=="__main__":
    main()
