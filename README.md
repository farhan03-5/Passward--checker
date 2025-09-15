# 🔐 Password Strength Checker (Python)

passward-checker is a Python module and CLI tool that analyzes password strength and provides actionable feedback.
It helps users create stronger, more secure passwords by evaluating length, character variety, entropy, common/dictionary word usage, sequences, and repetition patterns.

---

## 🚀 Features
✅ Strength Scoring (0–100 scale, classified as Weak, Better, or Strong)
✅ Entropy Estimation (measures randomness in bits)
✅ Character Class Detection (lowercase, uppercase, digits, symbols)
✅ Common Password Detection (flags widely used/unsafe passwords)
✅ Dictionary Word Detection (detects plain dictionary words in passwords)
✅ Sequence Detection (e.g., abcd, 1234, qwerty)
✅ Repetition Penalty (penalizes long runs of repeated characters)
✅ Suggestions (clear tips to strengthen weak passwords)
✅ CLI Support – run directly from the terminal

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

