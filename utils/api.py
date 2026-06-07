import os
import requests

API_BASE_URL = os.environ.get("UNICOMPARE_API_URL", "http://localhost:8000")

def _get_headers(token=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def _handle_error(e):
    if isinstance(e, requests.exceptions.ConnectionError):
        return {"error": f"Tidak dapat terhubung ke server ({API_BASE_URL})"}, True
    if isinstance(e, requests.exceptions.Timeout):
        return {"error": "Waktu permintaan habis"}, True
    return {"error": str(e)}, True

def get_sources():
    try:
        r = requests.get(f"{API_BASE_URL}/api/sources", timeout=10)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def get_universities(limit=0):
    try:
        r = requests.get(f"{API_BASE_URL}/api/universities", params={"limit": limit}, timeout=10)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def search_universities(q):
    try:
        r = requests.get(f"{API_BASE_URL}/api/universities/search", params={"q": q}, timeout=10)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def get_university_detail(university_name):
    try:
        r = requests.get(f"{API_BASE_URL}/api/universities/{university_name}", timeout=10)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def get_university_programs(university_id):
    try:
        r = requests.get(f"{API_BASE_URL}/api/universities/{university_id}/programs", timeout=10)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def compare_score(score, q="", universities="", limit=50):
    try:
        params = {"score": score, "q": q, "universities": universities, "limit": limit}
        r = requests.get(f"{API_BASE_URL}/api/compare", params=params, timeout=10)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def compare_choices(pilihan):
    try:
        r = requests.post(f"{API_BASE_URL}/api/compare/choices",
                          json={"pilihan": pilihan}, timeout=10)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def login(username, password):
    try:
        r = requests.post(f"{API_BASE_URL}/api/auth/login",
                          json={"username": username, "password": password}, timeout=10)
        if r.status_code == 401:
            return {"error": "Username atau password salah"}, True
        if r.status_code == 422:
            detail = r.json().get("detail", [{}])
            msg = detail[0].get("msg", "Data tidak valid") if isinstance(detail, list) else str(detail)
            return {"error": msg}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def register(username, password):
    try:
        r = requests.post(f"{API_BASE_URL}/api/auth/register",
                          json={"username": username, "password": password}, timeout=10)
        if r.status_code == 409:
            return {"error": "Username sudah terdaftar"}, True
        if r.status_code == 422:
            return {"error": r.json().get("detail", "Data tidak valid")}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def get_me(token):
    try:
        r = requests.get(f"{API_BASE_URL}/api/auth/me",
                         headers=_get_headers(token), timeout=10)
        if r.status_code in (401, 403):
            return {"error": "Sesi telah berakhir, silakan login ulang"}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def get_admin_users(token):
    try:
        r = requests.get(f"{API_BASE_URL}/api/admin/users",
                         headers=_get_headers(token), timeout=10)
        if r.status_code == 403:
            return {"error": "Akses khusus admin"}, True
        if r.status_code == 401:
            return {"error": "Sesi telah berakhir, silakan login ulang"}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def delete_admin_user(token, username):
    try:
        r = requests.delete(f"{API_BASE_URL}/api/admin/users/{username}",
                            headers=_get_headers(token), timeout=10)
        if r.status_code == 400:
            return {"error": "Tidak dapat menghapus diri sendiri"}, True
        if r.status_code == 404:
            return {"error": "User tidak ditemukan"}, True
        if r.status_code == 403:
            return {"error": "Akses khusus admin"}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def create_admin_university(token, id, name, sources=None):
    try:
        r = requests.post(f"{API_BASE_URL}/api/admin/universities",
                          json={"id": id, "name": name, "sources": sources or []},
                          headers=_get_headers(token), timeout=10)
        if r.status_code == 403:
            return {"error": "Akses khusus admin"}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def update_admin_university(token, university_id, name=None, sources=None):
    try:
        body = {}
        if name is not None:
            body["name"] = name
        if sources is not None:
            body["sources"] = sources
        r = requests.put(f"{API_BASE_URL}/api/admin/universities/{university_id}",
                          json=body,
                          headers=_get_headers(token), timeout=10)
        if r.status_code == 404:
            return {"error": "Universitas tidak ditemukan"}, True
        if r.status_code == 403:
            return {"error": "Akses khusus admin"}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def delete_admin_university(token, university_id):
    try:
        r = requests.delete(f"{API_BASE_URL}/api/admin/universities/{university_id}",
                            headers=_get_headers(token), timeout=10)
        if r.status_code == 404:
            return {"error": "Universitas tidak ditemukan"}, True
        if r.status_code == 403:
            return {"error": "Akses khusus admin"}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def update_admin_university_programs(token, university_id, programs):
    try:
        r = requests.put(f"{API_BASE_URL}/api/admin/universities/{university_id}/programs",
                          json={"programs": programs},
                          headers=_get_headers(token), timeout=10)
        if r.status_code == 404:
            return {"error": "Universitas tidak ditemukan"}, True
        if r.status_code == 403:
            return {"error": "Akses khusus admin"}, True
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)

def root():
    try:
        r = requests.get(f"{API_BASE_URL}/", timeout=10)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return _handle_error(e)
