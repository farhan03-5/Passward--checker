# 🔐 Password Strength Checker (Python)

A simple **Cybersecurity project** that checks if a password is **Weak / Better / Strong** and gives **suggestions to improve it**.  
This project demonstrates basic **password security principles** like length, character variety, and entropy.

---

## 🚀 Features
- Classifies passwords as **Weak, Better, or Strong**
- Provides actionable **suggestions to improve weak passwords**
- Simple **command-line interface (CLI)**
- Beginner-friendly Python project for cybersecurity portfolios

---

## 📸 Example Usage
```bash
$ python password_checker.py Fraddy@123 -------- (Enter your passward)

{
  "password": "Fraddy@123",
  "classification": "Weak",
  "score": 0,
  "details": {
    "length_score": 16,
    "classes": {"lower": true, "upper": false, "digit": true, "symbol": false},
    "entropy_bits": 39.86,
    "entropy_score": 12.46,
    "raw_score": 44.46,
    "penalties": 50,
    "final_score": 0
  },
  "suggestions": [
    "Add uppercase letters.",
    "Add symbols (e.g. !@#$%).",
    "Do not use common passwords (e.g. 'password', '123456').",
    "Avoid plain dictionary words; consider mixing or using unrelated words."
  ]
}

