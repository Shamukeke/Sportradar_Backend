import json

with open('activities_fixture.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Supprime le champ participants de chaque entrée
for obj in data:
    obj['fields'].pop('participants', None)

with open('activities_fixture_clean.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
