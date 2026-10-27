import json

# 1. Wczytanie oraz parsowanie pliku JSON
with open("pytania.json", "r", encoding="utf-8") as f:
    data = json.load(f)

questions = data["questions"]
rules = data["rules"]
user_answers = {}

print("--- SYSTEM EKSPERCKI: DOBÓR FILMU ---\n")

# 2. Pytania do użytkowmika
for q_id, q_data in questions.items():
    print(f"{q_id}: {q_data['text']}")
    options = q_data["answers"]

    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    
    while True:
        choice = input("Wybierz odpowiedź lub numer: ").strip()
        if choice in options:
            user_answers[q_id] = choice
            break
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            user_answers[q_id] = options[int(choice) - 1]
            break
        print("Wpisz numer jednej z dostępnych odpowiedzi.")
    print()

# 3. Wybór pasujących reguł IF-THEN (operator AND)
matched_rules = []
for rule in rules:
    if all(user_answers.get(k) == v for k, v in rule["if"].items()):
        matched_rules.append(rule)

# 4. Wypisanie diagnozy
print("--- WYNIKI DIAGNOZY ---")
if matched_rules:
    for rule in matched_rules:
        print(f"- {rule['then']['diagnosis']}")
else:
    print("Nie znaleziono reguły pasującej do podanych odpowiedzi.")