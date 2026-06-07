import urllib.request, json

api = "http://localhost:8000"
fe = "http://localhost:8501"
errors = []

def ok(msg):
    print(f"  OK  {msg}")

def fail(msg):
    print(f"  FAIL {msg}")
    errors.append(msg)

print("Testing Backend...")
r = json.loads(urllib.request.urlopen(f"{api}/").read())
ok(f"Root: {r['status']}") if r["status"] == "ok" else fail("Root")

r = json.loads(urllib.request.urlopen(f"{api}/api/sources").read())
ok(f"Sources: {r['total']} total") if r["total"] > 0 else fail("Sources")

r = json.loads(urllib.request.urlopen(f"{api}/api/universities?limit=5").read())
ok(f"Universities: {r['total']} total") if r["total"] > 0 else fail("Universities")

r = json.loads(urllib.request.urlopen(f"{api}/api/universities/ui/programs").read())
ok(f"UI Programs: {len(r['programs'])} programs") if len(r["programs"]) > 0 else fail("Programs")

r = json.loads(urllib.request.urlopen(f"{api}/api/compare?score=700&limit=3").read())
ok(f"Compare(700): {r['total']} unis")

body = json.dumps({"pilihan": [{"universitas": "ui", "program": "Kedokteran"}, {"universitas": "itb", "program": "STEI"}]}).encode()
req = urllib.request.Request(f"{api}/api/compare/choices", data=body, headers={"Content-Type": "application/json"})
r = json.loads(urllib.request.urlopen(req).read())
ok(f"Choices: {len(r['pilihan'])} matched, selisih={r['perbandingan']['selisih']}") if len(r["pilihan"]) == 2 else fail("Choices")

body = json.dumps({"username": "test123", "password": "test123"}).encode()
req = urllib.request.Request(f"{api}/api/auth/register", data=body, headers={"Content-Type": "application/json"})
r = json.loads(urllib.request.urlopen(req).read())
ok(f"Register OK")

req = urllib.request.Request(f"{api}/api/favorites", headers={"Authorization": f"Bearer {r['access_token']}"})
r = json.loads(urllib.request.urlopen(req).read())
ok(f"Favorites: {len(r['favorites'])} items")

print("\nTesting Frontend...")
r = urllib.request.urlopen(fe)
ok(f"Streamlit: status={r.status}") if r.status == 200 else fail("Frontend status")

print(f"\n{'='*40}")
if errors:
    print(f"{len(errors)} error(s) ditemukan:")
    for e in errors:
        print(f"  - {e}")
else:
    print("SEMUA TERINTEGRASI DENGAN BAIK! ✅")
