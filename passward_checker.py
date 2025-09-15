import re
import math
import sys

                      # small sample common password list (for demonstration). In real project, use larger list.
COMMON_PASSWORDS = {
    "123456","password","123456789","qwerty","abc123","password1","111111","123123","letmein"
}

                       # small dictionary snippet for demo; replace with full dictionary file for production
SAMPLE_WORDS = {"password","admin","let","me","in","secret","welcome","pass","hello"}

SEQUENCE_PATTERNS = [
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789",
    "`~!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"
]

def contains_sequence(pw, length=4):
    s = pw
    for seq in SEQUENCE_PATTERNS:
        for i in range(len(seq)-length+1):
            sub = seq[i:i+length]
            if sub in s or sub[::-1] in s:
                return True
    return False

def char_classes(password):
    classes = {
        'lower': bool(re.search(r'[a-z]', password)),
        'upper': bool(re.search(r'[A-Z]', password)),
        'digit': bool(re.search(r'\d', password)),
        'symbol': bool(re.search(r'[^A-Za-z0-9]', password))
    }
    return classes

def estimate_charset_size(classes_used):
    size = 0
    if classes_used['lower']:
        size += 26
    if classes_used['upper']:
        size += 26
    if classes_used['digit']:
        size += 10
    if classes_used['symbol']:
                        # rough symbols count
        size += 32
    return size if size>0 else 1

def entropy_bits(password):
    classes = char_classes(password)
    charset = estimate_charset_size(classes)
    return len(password) * math.log2(charset)

def contains_common(password):
    pw_lower = password.lower()
    if pw_lower in COMMON_PASSWORDS:
        return True
    for c in COMMON_PASSWORDS:
        if c in pw_lower:
            return True
    return False

def contains_dictionary_word(password):
    pw_lower = password.lower()
                    # simple substring search against SAMPLE_WORDS
    for w in SAMPLE_WORDS:
        if w in pw_lower and len(w)>=3:
            return True
    return False

def repeated_chars_penalty(password):
                    # detect long runs of same char
    max_run = 1
    curr = 1
    for i in range(1,len(password)):
        if password[i] == password[i-1]:
            curr += 1
            max_run = max(max_run, curr)
        else:
            curr = 1
    if max_run >= 4:
        return min(10, (max_run - 3)*3)  # up to 10 points penalty
    return 0

def analyze_password(password):
    password = password or ""
    L = len(password)

                    # Base scores
    score = 0
    details = {}

                    # 1) Length (max 30)
    length_score = min(30, max(0, (L - 4) * 2))  # 6 -> 4, 16 -> 24 -> capped at 30
    details['length_score'] = length_score
    score += length_score
                
                    # 2) Character classes (max 20)
    classes = char_classes(password)
    class_count = sum(classes.values())
    class_score = class_count * 5  # up to 20
    details['classes'] = classes
    details['class_score'] = class_score
    score += class_score

                    # 3) Entropy (max 25)
    ent = entropy_bits(password)
                # map e.g. 0-80 bits -> 0-25 points
    ent_score = min(25, (ent / 80.0) * 25)
    details['entropy_bits'] = round(ent,2)
    details['entropy_score'] = round(ent_score,2)
    score += ent_score

                  # 4) Penalties
    penalties = 0
    if contains_common(password):
        penalties += 40
        details['common_password'] = True
    else:
        details['common_password'] = False

    if contains_dictionary_word(password):
        penalties += 15
        details['contains_dictionary_word'] = True
    else:
        details['contains_dictionary_word'] = False

    if contains_sequence(password):
        penalties += 12
        details['sequence_detected'] = True
    else:
        details['sequence_detected'] = False

    rep_pen = repeated_chars_penalty(password)
    penalties += rep_pen
    details['repeated_penalty'] = rep_pen

                  # ensure penalties cannot drop score below 0
    final_score = max(0, score - penalties)
    details['raw_score'] = round(score,2)
    details['penalties'] = penalties
    details['final_score'] = round(final_score,2)

                  # classification
    if final_score < 40:
        classification = "Weak"
    elif final_score < 70:
        classification = "Better"
    else:
        classification = "Strong"

                          # suggestions
    suggestions = []
    if L < 12:
        suggestions.append("Increase length to 12+ characters (or use a passphrase).")
    if not classes['upper']:
        suggestions.append("Add uppercase letters.")
    if not classes['lower']:
        suggestions.append("Add lowercase letters.")
    if not classes['digit']:
        suggestions.append("Add digits.")
    if not classes['symbol']:
        suggestions.append("Add symbols (e.g. !@#$%).")
    if details['common_password']:
        suggestions.append("Do not use common passwords (e.g. 'password', '123456').")
    if details['contains_dictionary_word']:
        suggestions.append("Avoid plain dictionary words; consider mixing or using unrelated words.")
    if details['sequence_detected']:
        suggestions.append("Avoid sequential patterns like 'abcd' or '1234'.")
    if rep_pen:
        suggestions.append("Avoid long repeated characters or repeated sequences.")
    if not suggestions:
        suggestions.append("Looks good — consider using a password manager to generate/store an even stronger random password.")

    return {
        'password': password,
        'classification': classification,
        'score': round(final_score,2),
        'details': details,
        'suggestions': suggestions
    }

                        # CLI entry
def main():
    if len(sys.argv) < 2:
        print("Usage: python password_strength.py <password>")
        sys.exit(1)
    pw = sys.argv[1]
    report = analyze_password(pw)
    import json
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
