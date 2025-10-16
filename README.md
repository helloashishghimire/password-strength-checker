# password-strength.py

# 🔐 Password Strength Checker (Python)

A tiny, dependency-free CLI tool that rates password strength from **0–10**, estimates **entropy (bits)**, and flags risky patterns (common passwords, repeats, sequences).

## Features
- No dependencies (pure Python 3)
- Entropy estimate based on charset × length
- Checks for repeats (`aaa`), numeric/keyboard sequences (`1234`, `qwer`)
- Helpful notes and improvement tips

## Usage
```bash
# Hidden input prompt
python3 password_strength.py

# Or pass as an argument (useful for demos/automation)
python3 password_strength.py "Kumari@2025!"
Example
pgsql
Copy code
Enter a password to check (input hidden):

🔎 Password Check
Score         : 8/10 — Strong
Entropy       : ~64.3 bits (approx.)
Length        : 12 chars
Notes         : Avoid repeats or easy sequences (e.g., 1234, qwer, aaa).

Tips: Use 3–4 random words + symbols (e.g., 'river*planet*violet*42'). Avoid personal info and patterns.
Why this project?
Perfect for showcasing security awareness and clean Python.

Fits in under ~100 lines, easy to read and extend.
