from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rapidfuzz import process

# 🔐 DATABASE IMPORTS
from database import engine, SessionLocal, Base
from models import User, Chat
from passlib.context import CryptContext

app = FastAPI()

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

# ✅ PASSWORD HASHING
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ MODELS
class Message(BaseModel):
    message: str
    username: str   # 🔥 dynamic user

class UserCreate(BaseModel):
    username: str
    password: str

# ✅ FAQ DATA
faq = {
    "bc": {
        "income limit": "BC students income limit is up to ₹1.5 lakh per year.",
        "eligibility": "BC students must belong to backward class and meet income criteria.",
        "scholarship": "BC students can apply for post-matric scholarship through ePass.",
        "fee reimbursement": "BC students get partial or full fee reimbursement.",
        "renewal": "BC students must renew scholarship every academic year.",
        "documents": "Income certificate, caste certificate, Aadhaar required.",
        "amount": "Amount varies based on course and category.",
        "hostel": "Some BC students are eligible for hostel facilities.",
        "last date": "Last date is announced on Telangana ePass portal.",
        "apply online": "Apply through official Telangana ePass website."
    },

    "sc": {
        "scholarship": "SC students get full fee reimbursement under ePass.",
        "documents": "SC students need caste certificate, income certificate, Aadhaar.",
        "benefits": "SC students receive tuition fee + maintenance allowance.",
        "income limit": "Income limit for SC is usually ₹2 lakh per year.",
        "eligibility": "Must belong to SC category and studying in recognized institution.",
        "hostel": "SC students can apply for government hostels.",
        "renewal": "Renew every year with updated documents.",
        "amount": "Full tuition + additional benefits provided.",
        "status": "Check status using application ID.",
        "bank account": "Bank account must be linked with Aadhaar."
    },

    "st": {
        "benefits": "ST students receive full fee reimbursement.",
        "hostel": "ST students get hostel and accommodation facilities.",
        "documents": "Caste certificate, Aadhaar, income certificate required.",
        "income limit": "Income limit is ₹2 lakh per year.",
        "eligibility": "Must belong to ST category.",
        "scholarship": "ST students can apply via ePass portal.",
        "renewal": "Scholarship renewal required yearly.",
        "amount": "Includes tuition + maintenance allowance.",
        "status": "Track via application number.",
        "apply": "Apply through official Telangana ePass website."
    },

    "general": {
        "how to apply": "Go to Telangana ePass website → click Apply → fill form → submit.",
        "documents": "Aadhaar, income certificate, caste certificate, bank details required.",
        "status": "Check application status using your application number.",
        "login problem": "Use 'Forgot Password' option to reset password.",
        "helpline": "Call 1800-599-4977 for support.",
        "last date": "Check official portal for latest deadlines.",
        "renewal": "Students must renew every year.",
        "amount": "Scholarship depends on course and category.",
        "college verification": "College must verify your application.",
        "rejected": "Check reason in portal and reapply with correct documents.",
        "pending": "Wait for verification from college or officer.",
        "bank details": "Ensure bank account is active and Aadhaar linked.",
        "correction": "Login and edit your application before final submission.",
        "download receipt": "Download application receipt after submission.",
        "forgot password": "Use registered mobile/email to reset password.",
        "application id": "You will get ID after successful submission.",
        "approval time": "Usually takes few weeks after verification.",
        "eligibility": "Must be student in recognized institution.",
        "income certificate": "Must be issued by government authority.",
        "aadhaar required": "Yes, Aadhaar is mandatory.",
        "mobile number": "Must be active for OTP verification.",
        "email required": "Recommended for updates and alerts.",
        "update details": "You can update before final submission.",
        "multiple applications": "Only one application per student allowed.",
        "fee payment": "Paid directly to college or student account.",
        "track application": "Use application ID in portal.",
        "technical issue": "Try again or contact helpline.",
        "server problem": "Wait and try later.",
        "application correction": "Edit option available before approval.",
        "new registration": "Register first before applying.",
        "portal login": "Use username and password.",
        "college list": "Available on official portal.",
        "course eligibility": "Depends on course and institution.",
        "scholarship types": "Pre-matric and post-matric scholarships available.",
        "verification": "Documents verified by authorities.",
        "delay": "Due to verification or document issues.",
        "payment status": "Check in portal under payment section.",
        "bank rejected": "Update correct bank details.",
        "aadhaar mismatch": "Ensure Aadhaar details are correct.",
        "otp not received": "Check mobile network or try again.",
        "profile update": "Login and update details.",
        "document upload": "Upload scanned copies clearly.",
        "file size": "Ensure documents meet size requirements.",
        "photo upload": "Upload recent passport size photo.",
        "signature upload": "Upload clear signature.",
        "portal down": "Try after some time.",
        "help center": "Contact nearest help center.",
        "support email": "Use official email support.",
        "reset account": "Contact support team."
    }
}

# ✅ MEMORY
last_category = {"value": None}

# 💾 SAVE CHAT FUNCTION
def save_chat(username, message, reply):
    db = SessionLocal()

    chat = Chat(
        username=username,
        message=message,
        reply=reply
    )

    db.add(chat)
    db.commit()
    db.close()

# ✅ HOME
@app.get("/")
def home():
    return {"message": "Backend running successfully 🚀"}

# 🔐 SIGNUP API
@app.post("/signup")
def signup(user: UserCreate):
    db = SessionLocal()

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        return {"message": "User already exists"}

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User created successfully"}

# 🔐 LOGIN API
@app.post("/login")
def login(user: UserCreate):
    db = SessionLocal()

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        return {"message": "Invalid credentials"}

    return {"message": "Login successful"}

# 🤖 CHAT API
@app.post("/chat")
def chat(data: Message):
    user_msg = data.message.lower().strip()
    username = data.username

    # 🔥 CATEGORY BUTTON
    if user_msg in ["bc", "sc", "st"]:
        last_category["value"] = user_msg

        reply = f"📂 {user_msg.upper()} Category:\nChoose a topic:\n" + \
                "\n".join([f"- {q}" for q in faq[user_msg].keys()])

        save_chat(username, user_msg, reply)
        return {"reply": reply}

    # 🔹 DETECT CATEGORY
    category = None
    if "bc" in user_msg:
        category = "bc"
    elif "sc" in user_msg:
        category = "sc"
    elif "st" in user_msg:
        category = "st"

    # 🔥 USE MEMORY
    if not category and last_category["value"]:
        category = last_category["value"]

    # 🔹 CATEGORY SEARCH
    if category:
        for key in faq[category]:
            if key in user_msg:
                reply = faq[category][key]
                save_chat(username, user_msg, reply)
                return {"reply": reply}

        best_match = process.extractOne(user_msg, faq[category].keys())
        if best_match and best_match[1] > 60:
            reply = faq[category][best_match[0]]
            save_chat(username, user_msg, reply)
            return {"reply": reply}

    # 🔹 GENERAL SEARCH
    for key in faq["general"]:
        if key in user_msg:
            reply = faq["general"][key]
            save_chat(username, user_msg, reply)
            return {"reply": reply}

    best_match_general = process.extractOne(user_msg, faq["general"].keys())
    if best_match_general and best_match_general[1] > 60:
        reply = faq["general"][best_match_general[0]]
        save_chat(username, user_msg, reply)
        return {"reply": reply}

    reply = "🤖 Sorry, I didn't understand.\nTry:\n- how to apply\n- documents\n- sc scholarship"
    save_chat(username, user_msg, reply)

    return {"reply": reply}

# 📜 HISTORY API
@app.get("/history/{username}")
def get_history(username: str):
    db = SessionLocal()

    chats = db.query(Chat).filter(Chat.username == username).all()

    db.close()

    return chats



























































































































































































# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from rapidfuzz import process

# # 🔐 DATABASE IMPORTS
# from database import engine, SessionLocal, Base
# from models import User, Chat
# from passlib.context import CryptContext

# app = FastAPI()

# # ✅ CREATE TABLES
# Base.metadata.create_all(bind=engine)

# # ✅ PASSWORD HASHING
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# def hash_password(password):
#     return pwd_context.hash(password)

# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)

# # ✅ CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ MODELS
# class Message(BaseModel):
#     message: str

# class UserCreate(BaseModel):
#     username: str
#     password: str

# # ✅ FAQ DATA
# faq = {
#     "bc": {
#         "income limit": "BC students income limit is usually up to ₹1.5 lakh.",
#         "eligibility": "BC students must belong to backward class category and meet income criteria.",
#         "scholarship": "BC students can apply for post-matric scholarships through ePass."
#     },
#     "sc": {
#         "scholarship": "SC students get full fee reimbursement under ePass.",
#         "documents": "SC students need caste certificate, income certificate, and Aadhaar.",
#         "benefits": "SC students receive full tuition fee reimbursement and maintenance allowance."
#     },
#     "st": {
#         "benefits": "ST students receive full tuition fee reimbursement and maintenance allowance.",
#         "hostel": "ST students can apply for hostel facilities through welfare department.",
#         "documents": "ST students need caste certificate, Aadhaar, and income certificate."
#     },
#     "general": {
#         "how to apply": "Go to Telangana ePass website and click on Apply section.",
#         "documents": "You need Aadhaar card, income certificate, caste certificate, and bank details.",
#         "status": "Check your application status using your application number on ePass portal.",
#         "login problem": "Try resetting your password using 'Forgot Password' option.",
#         "helpline": "Contact Telangana ePass helpline for assistance."
#     }
# }

# # ✅ MEMORY
# last_category = {"value": None}

# # 💾 SAVE CHAT FUNCTION
# def save_chat(username, message, reply):
#     db = SessionLocal()

#     chat = Chat(
#         username=username,
#         message=message,
#         reply=reply
#     )

#     db.add(chat)
#     db.commit()
#     db.close()

# # ✅ HOME
# @app.get("/")
# def home():
#     return {"message": "Backend running successfully 🚀"}

# # 🔐 SIGNUP API
# @app.post("/signup")
# def signup(user: UserCreate):
#     db = SessionLocal()

#     existing = db.query(User).filter(User.username == user.username).first()
#     if existing:
#         return {"message": "User already exists"}

#     new_user = User(
#         username=user.username,
#         password=hash_password(user.password)
#     )

#     db.add(new_user)
#     db.commit()
#     db.close()

#     return {"message": "User created successfully"}

# # 🔐 LOGIN API
# @app.post("/login")
# def login(user: UserCreate):
#     db = SessionLocal()

#     db_user = db.query(User).filter(User.username == user.username).first()

#     if not db_user or not verify_password(user.password, db_user.password):
#         return {"message": "Invalid credentials"}

#     return {"message": "Login successful"}

# # 🤖 CHAT API
# @app.post("/chat")
# def chat(data: Message):
#     user_msg = data.message.lower().strip()

#     # 🔥 CATEGORY BUTTON
#     if user_msg in ["bc", "sc", "st"]:
#         last_category["value"] = user_msg
#         reply = f"📂 {user_msg.upper()} Category:\nChoose a topic:\n" + \
#                 "\n".join([f"- {q}" for q in faq[user_msg].keys()])

#         save_chat("devender", user_msg, reply)
#         return {"reply": reply}

#     # 🔹 DETECT CATEGORY
#     category = None
#     if "bc" in user_msg:
#         category = "bc"
#     elif "sc" in user_msg:
#         category = "sc"
#     elif "st" in user_msg:
#         category = "st"

#     # 🔥 USE MEMORY
#     if not category and last_category["value"]:
#         category = last_category["value"]

#     # 🔹 CATEGORY SEARCH
#     if category:
#         for key in faq[category]:
#             if key in user_msg:
#                 reply = faq[category][key]
#                 save_chat("devender", user_msg, reply)
#                 return {"reply": reply}

#         best_match = process.extractOne(user_msg, faq[category].keys())
#         if best_match and best_match[1] > 60:
#             reply = faq[category][best_match[0]]
#             save_chat("devender", user_msg, reply)
#             return {"reply": reply}

#     # 🔹 GENERAL SEARCH
#     for key in faq["general"]:
#         if key in user_msg:
#             reply = faq["general"][key]
#             save_chat("devender", user_msg, reply)
#             return {"reply": reply}

#     best_match_general = process.extractOne(user_msg, faq["general"].keys())
#     if best_match_general and best_match_general[1] > 60:
#         reply = faq["general"][best_match_general[0]]
#         save_chat("devender", user_msg, reply)
#         return {"reply": reply}

#     reply = "🤖 Sorry, I didn't understand.\nTry:\n- how to apply\n- documents\n- sc scholarship"
#     save_chat("devender", user_msg, reply)

#     return {"reply": reply}

# # 📜 HISTORY API
# @app.get("/history/{username}")
# def get_history(username: str):
#     db = SessionLocal()

#     chats = db.query(Chat).filter(Chat.username == username).all()

#     db.close()

#     return chats








































































































































































# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from rapidfuzz import process

# # 🔐 DATABASE IMPORTS
# from database import engine, SessionLocal, Base
# from models import User
# from passlib.context import CryptContext

# app = FastAPI()

# # ✅ CREATE TABLES
# Base.metadata.create_all(bind=engine)

# # ✅ PASSWORD HASHING
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# def hash_password(password):
#     return pwd_context.hash(password)

# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)

# # ✅ CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ MODELS
# class Message(BaseModel):
#     message: str

# class UserCreate(BaseModel):
#     username: str
#     password: str

# # ✅ FAQ DATA
# faq = {
#     "bc": {
#         "income limit": "BC students income limit is usually up to ₹1.5 lakh.",
#         "eligibility": "BC students must belong to backward class category and meet income criteria.",
#         "scholarship": "BC students can apply for post-matric scholarships through ePass."
#     },
#     "sc": {
#         "scholarship": "SC students get full fee reimbursement under ePass.",
#         "documents": "SC students need caste certificate, income certificate, and Aadhaar.",
#         "benefits": "SC students receive full tuition fee reimbursement and maintenance allowance."
#     },
#     "st": {
#         "benefits": "ST students receive full tuition fee reimbursement and maintenance allowance.",
#         "hostel": "ST students can apply for hostel facilities through welfare department.",
#         "documents": "ST students need caste certificate, Aadhaar, and income certificate."
#     },
#     "general": {
#         "how to apply": "Go to Telangana ePass website and click on Apply section.",
#         "documents": "You need Aadhaar card, income certificate, caste certificate, and bank details.",
#         "status": "Check your application status using your application number on ePass portal.",
#         "login problem": "Try resetting your password using 'Forgot Password' option.",
#         "helpline": "Contact Telangana ePass helpline for assistance."
#     }
# }

# # ✅ MEMORY
# last_category = {"value": None}

# # ✅ HOME
# @app.get("/")
# def home():
#     return {"message": "Backend running successfully 🚀"}

# # 🔐 SIGNUP API
# @app.post("/signup")
# def signup(user: UserCreate):
#     db = SessionLocal()

#     existing = db.query(User).filter(User.username == user.username).first()
#     if existing:
#         return {"message": "User already exists"}

#     new_user = User(
#         username=user.username,
#         password=hash_password(user.password)
#     )

#     db.add(new_user)
#     db.commit()
#     db.close()

#     return {"message": "User created successfully"}

# # 🔐 LOGIN API
# @app.post("/login")
# def login(user: UserCreate):
#     db = SessionLocal()

#     db_user = db.query(User).filter(User.username == user.username).first()

#     if not db_user or not verify_password(user.password, db_user.password):
#         return {"message": "Invalid credentials"}

#     return {"message": "Login successful"}

# # 🤖 CHAT API
# @app.post("/chat")
# def chat(data: Message):
#     user_msg = data.message.lower().strip()

#     # 🔥 CATEGORY BUTTON
#     if user_msg in ["bc", "sc", "st"]:
#         last_category["value"] = user_msg
#         options = "\n".join([f"- {q}" for q in faq[user_msg].keys()])
#         return {
#             "reply": f"📂 {user_msg.upper()} Category:\nChoose a topic:\n{options}"
#         }

#     # 🔹 DETECT CATEGORY
#     category = None
#     if "bc" in user_msg:
#         category = "bc"
#     elif "sc" in user_msg:
#         category = "sc"
#     elif "st" in user_msg:
#         category = "st"

#     # 🔥 USE MEMORY
#     if not category and last_category["value"]:
#         category = last_category["value"]

#     # 🔹 CATEGORY SEARCH
#     if category:
#         for key in faq[category]:
#             if key in user_msg:
#                 return {"reply": faq[category][key]}

#         best_match = process.extractOne(user_msg, faq[category].keys())
#         if best_match and best_match[1] > 60:
#             return {"reply": faq[category][best_match[0]]}

#     # 🔹 GENERAL SEARCH
#     for key in faq["general"]:
#         if key in user_msg:
#             return {"reply": faq["general"][key]}

#     best_match_general = process.extractOne(user_msg, faq["general"].keys())
#     if best_match_general and best_match_general[1] > 60:
#         return {"reply": faq["general"][best_match_general[0]]}

#     return {
#         "reply": "🤖 Sorry, I didn't understand.\nTry:\n- how to apply\n- documents\n- sc scholarship"
#     }














































































































# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # ✅ CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Request model
# class Message(BaseModel):
#     message: str

# # ✅ CATEGORY FAQ DATA
# faq = {
#     "bc": {
#         "income limit": "BC students income limit is usually up to ₹1.5 lakh.",
#         "eligibility": "BC students must belong to backward class category and meet income criteria.",
#         "scholarship": "BC students can apply for post-matric scholarships through ePass."
#     },
#     "sc": {
#         "scholarship": "SC students get full fee reimbursement under ePass.",
#         "documents": "SC students need caste certificate, income certificate, and Aadhaar.",
#         "benefits": "SC students receive full tuition fee reimbursement and maintenance allowance."
#     },
#     "st": {
#         "benefits": "ST students receive full tuition fee reimbursement and maintenance allowance.",
#         "hostel": "ST students can apply for hostel facilities through welfare department.",
#         "documents": "ST students need caste certificate, Aadhaar, and income certificate."
#     },
#     "general": {
#         "how to apply": "Go to Telangana ePass website and click on Apply section.",
#         "documents": "You need Aadhaar card, income certificate, caste certificate, and bank details.",
#         "status": "Check your application status using your application number on ePass portal.",
#         "login problem": "Try resetting your password using 'Forgot Password' option.",
#         "helpline": "Contact Telangana ePass helpline for assistance."
#     }
# }

# # ✅ HOME ROUTE
# @app.get("/")
# def home():
#     return {"message": "Backend running successfully 🚀"}

# # ✅ CHAT API
# @app.post("/chat")
# def chat(data: Message):
#     user_msg = data.message.lower().strip()

#     # 🔥 STEP 1: CATEGORY BUTTON CLICK
#     if user_msg in ["bc", "sc", "st"]:
#         options = "\n".join([f"- {q}" for q in faq[user_msg].keys()])
#         return {
#             "reply": f"📂 {user_msg.upper()} Category:\nChoose a topic:\n{options}"
#         }

#     # 🔹 STEP 2: Detect category from message
#     category = "general"

#     if "bc" in user_msg:
#         category = "bc"
#     elif "sc" in user_msg:
#         category = "sc"
#     elif "st" in user_msg:
#         category = "st"

#     # 🔹 STEP 3: Search inside category
#     for key in faq[category]:
#         if key in user_msg:
#             return {"reply": faq[category][key]}

#     # 🔹 STEP 4: Fallback to general
#     for key in faq["general"]:
#         if key in user_msg:
#             return {"reply": faq["general"][key]}

#     # 🔹 STEP 5: Default response
#     return {
#         "reply": "🤖 Sorry, I didn't understand.\nTry:\n- how to apply\n- documents\n- status\nOr select a category."
#     }































































# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # ✅ CORS (allow frontend)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Request model
# class Message(BaseModel):
#     message: str

# # ✅ CATEGORY-BASED FAQ DATA
# faq = {
#     "bc": {
#         "income limit": "BC students income limit is usually up to ₹1.5 lakh.",
#         "eligibility": "BC students must belong to backward class category and meet income criteria.",
#         "scholarship": "BC students can apply for post-matric scholarships through ePass."
#     },
#     "sc": {
#         "scholarship": "SC students get full fee reimbursement under ePass.",
#         "documents": "SC students need caste certificate, income certificate, and Aadhaar.",
#         "benefits": "SC students receive full tuition fee reimbursement and maintenance allowance."
#     },
#     "st": {
#         "benefits": "ST students receive full tuition fee reimbursement and maintenance allowance.",
#         "hostel": "ST students can apply for hostel facilities through welfare department.",
#         "documents": "ST students need caste certificate, Aadhaar, and income certificate."
#     },
#     "general": {
#         "how to apply": "Go to Telangana ePass website and click on Apply section.",
#         "documents": "You need Aadhaar card, income certificate, caste certificate, and bank details.",
#         "status": "Check your application status using your application number on ePass portal.",
#         "login problem": "Try resetting your password using 'Forgot Password' option.",
#         "helpline": "Contact Telangana ePass helpline for assistance."
#     }
# }

# # ✅ Home route
# @app.get("/")
# def home():
#     return {"message": "Backend running successfully 🚀"}

# # ✅ Chat API (Category + Smart Matching)
# @app.post("/chat")
# def chat(data: Message):
#     user_msg = data.message.lower()

#     # 🔹 Detect category
#     category = "general"

#     if "bc" in user_msg:
#         category = "bc"
#     elif "sc" in user_msg:
#         category = "sc"
#     elif "st" in user_msg:
#         category = "st"

#     # 🔹 Search inside selected category
#     for key in faq[category]:
#         if key in user_msg:
#             return {"reply": faq[category][key]}

#     # 🔹 Fallback to general
#     for key in faq["general"]:
#         if key in user_msg:
#             return {"reply": faq["general"][key]}

#     # 🔹 Default response
#     return {
#         "reply": "🤖 Sorry, I couldn't understand. Try asking like: 'how to apply', 'documents', 'status'."
#     }





































































# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from rapidfuzz import process

# app = FastAPI()

# # ✅ CORS (allow frontend)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Request model
# class Message(BaseModel):
#     message: str

# # ✅ FAQ DATA (expand anytime)
# faq = {
#     "how to apply": "Go to Telangana ePass website and click on Apply section.",
#     "documents required": "You need Aadhaar card, income certificate, caste certificate, and bank details.",
#     "check status": "Check your application status using your application number on ePass portal.",
#     "eligibility": "Students with family income below specified limit are eligible.",
#     "last date": "Visit official ePass website to check the latest deadlines.",
#     "renewal": "You can renew your scholarship by logging into your account.",
#     "login problem": "Try resetting your password using 'Forgot Password' option.",
#     "payment not received": "Check bank details and contact support if delay continues.",
#     "income limit": "Income limit varies depending on category. Check official guidelines.",
#     "helpline": "Contact Telangana ePass helpline for assistance."

# }

# # ✅ Home route
# @app.get("/")
# def home():
#     return {"message": "Backend running successfully 🚀"}

# # ✅ Smart Chatbot API
# @app.post("/chat")
# def chat(data: Message):
#     user_msg = data.message.lower()

#     # 🔹 Step 1: direct keyword match
#     for key in faq:
#         if key in user_msg:
#             return {"reply": faq[key]}

#     # 🔹 Step 2: fuzzy matching (smart AI-like)
#     best_match = process.extractOne(user_msg, faq.keys())

#     if best_match and best_match[1] > 60:
#         return {"reply": faq[best_match[0]]}

#     # 🔹 Step 3: fallback
#     return {
#         "reply": "🤖 Sorry, I didn’t understand. Try asking like: 'how to apply', 'documents required', 'check status'."
#     }


































# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # ✅ CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Message(BaseModel):
#     message: str

# # ✅ FAQ DATA (you can expand this)
# faq = {
#     "how to apply": "Go to Telangana ePass website and click on Apply section.",
#     "documents": "You need Aadhaar card, income certificate, caste certificate, and bank details.",
#     "status": "Check your application status using your application number on ePass portal.",
#     "eligibility": "Students with family income below specified limit are eligible.",
#     "last date": "Visit official ePass website to check the latest deadlines.",
#     "renewal": "You can renew your scholarship by logging into your account.",
#     "login problem": "Try resetting your password using 'Forgot Password' option.",
#     "payment not received": "Check bank details and contact support if delay continues.",
#     "income limit": "Income limit varies depending on category. Check official guidelines.",
#     "helpline": "Contact Telangana ePass helpline for assistance."
# }

# # ✅ HOME ROUTE
# @app.get("/")
# def home():
#     return {"message": "Backend running successfully 🚀"}

# # ✅ CHAT ROUTE
# @app.post("/chat")
# def chat(data: Message):
#     user_msg = data.message.lower()

#     for key in faq:
#         if key in user_msg:
#             return {"reply": faq[key]}

#     return {"reply": "❌ Sorry, I couldn't find an answer. Please try asking differently."}























































# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = FastAPI()

# # ✅ CORS MUST BE RIGHT AFTER app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # 🔥 IMPORTANT
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# class Message(BaseModel):
#     message: str

# @app.get("/")
# def home():
#     return {"message": "Backend running successfully 🚀"}

# @app.post("/chat")
# def chat(data: Message):
#     user_msg = data.message

#     response = client.chat.completions.create(
#         model="gpt-4.1-mini",
#         messages=[
#             {"role": "system", "content": "You are a Telangana ePass assistant helping students."},
#             {"role": "user", "content": user_msg}
#         ]
#     )

#     reply = response.choices[0].message.content

#     return {"reply": reply}









# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Message(BaseModel):
#     message: str

# @app.get("/")
# def home():
#     return {"message": "Backend running successfully 🚀"}

# @app.post("/chat")
# def chat(data: Message):
#     user_msg = data.message.lower()

#     if "apply" in user_msg:
#         reply = "Go to epass website and click on Apply section."
#     else:
#         reply = "I will help you with Telangana ePass queries."

#     return {"reply": reply}