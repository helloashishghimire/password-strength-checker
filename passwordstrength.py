#!/usr/bin/env python3
# password_strength.py
# A lightweight password strength checker (no dependencies)

import math
import re
import sys
from getpass import getpass

COMMON = {
    "password","123456","123456789","12345","qwerty","abc123","111111","123123",
    "letmein","admin","welcome","iloveyou","monkey","dragon","football","baseball",
    "qwertyuiop","1234","1q2w3e4r","passw0rd","password1","000000"
}

def charset_size(pw: str) -> int:
    size = 0
    if re.search(r"[a-z]", pw): size += 26
    if re.search(r"[A-Z]", pw): size += 26
    if re.search(r"[0-9]", pw): size += 10
    if re.search(r"[^\w]", pw): size += 33  # rough printable symbols
    return size or 1

def shannon_entropy_bits(pw: str) -> float:
    # Approximate: log2(charset^length) = length * log2(charset)
    return len(pw) * math.log2(charset_size(pw))

def repeating_or_sequences_penalty(pw: str) -> int:
    penalty = 0
    if re.search(r"(.)\1{2,}", pw):           # aaa, !!!, 111
        penalty += 1
    if re.search(r"(?:0123|1234|2345|3456|4567|5678|6789)", pw):
        penalty += 1
    if re.search(r"(?:abcd|bcde|cdef|defg|qwer|asdf|zxcv)", pw.lower()):
        penalty += 1
    kb_rows = ["qwertyuiop","asdfghjkl","zxcvbnm"]
    for row in kb_rows:
        for i in range(len(row)-3):
            if row[i:i+4] in pw.lower():
                penalty += 1
                break
    return penalty

def score_password(pw: str) -> dict:
    if not pw:
        return {"score": 0, "label": "Empty", "reasons": ["No password provided."]}

    reasons = []
    score = 0

    # 1) Common/blacklist
    if pw.lower() in COMMON:
        return {"score": 1, "label": "Very Weak", "reasons": ["Common password (easily guessed)."]}

    # 2) Length tiers
    L = len(pw)
    if L >= 16: score += 4
    elif L >= 12: score += 3
    elif L >= 10: score += 2
    elif L >= 8: score += 1
    else: reasons.append("Too short (< 8 characters).")

    # 3) Character variety
    cats = sum(bool(re.search(p, pw)) for p in [r"[a-z]", r"[A-Z]", r"[0-9]", r"[^\w]"])
    score += max(0, cats - 1)  # 0..3 points
    if cats <= 1:
        reasons.append("Use a mix of lowercase, uppercase, digits, and symbols.")

    # 4) Entropy (rough)
    bits = shannon_entropy_bits(pw)
    if bits >= 80: score += 3
    elif bits >= 60: score += 2
    elif bits >= 40: score += 1
    else: reasons.append("Low entropy — consider longer length and more variety.")

    # 5) Pattern penalties
    penalty = repeating_or_sequences_penalty(pw)
    score -= penalty
    if penalty:
        reasons.append("Avoid repeats or easy sequences (e.g., 1234, qwer, aaa).")

    # Clamp and label
    score = max(0, min(10, score))
    if score >= 9: label = "Excellent"
    elif score >= 7: label = "Strong"
    elif score >= 5: label = "Moderate"
    elif score >= 3: label = "Weak"
    else: label = "Very Weak"

    return {
        "score": score,
        "label": label,
        "entropy_bits": round(bits, 1),
        "length": L,
        "reasons": reasons
    }

def main():
    # Support: echo-free prompt OR arg
    pw = None
    if len(sys.argv) > 1:
        pw = sys.argv[1]
    else:
        pw = getpass("Enter a password to check (input hidden): ")

    result = score_password(pw)
    print("\n🔎 Password Check")
    print(f"Score         : {result.get('score', 0)}/10 — {result.get('label','')}")
    if "entropy_bits" in result:
        print(f"Entropy       : ~{result['entropy_bits']} bits (approx.)")
    if "length" in result:
        print(f"Length        : {result['length']} chars")
    if result.get("reasons"):
        print("Notes         : " + " | ".join(result["reasons"]))
    print("\nTips: Use 3–4 random words + symbols (e.g., 'river*planet*violet*42'). Avoid personal info and patterns.")

if __name__ == "__main__":
    main()

