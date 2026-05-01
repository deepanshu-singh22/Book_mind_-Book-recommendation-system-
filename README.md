# 📚 BookMind — Book Recommender System

Ek full-stack book recommender system with a **Flask REST API backend** aur ek **modern dark-theme frontend**.

---

## 📁 Project Structure

```
book-recommender/
│
├── app.py                  ← Flask backend (REST API)
├── requirements.txt        ← Python dependencies
│
├── popular.pkl             ← (copy karo apni pickle files yahan)
├── pt.pkl
├── books.pkl
├── similarity_scores.pkl
│
└── frontend/
    └── index.html          ← Standalone frontend (browser mein open karo)
```

---

## 🚀 Setup & Run

### 1. Pickle files copy karo
```bash
# Apni zip se extract karo aur isi folder mein rakh do
cp popular.pkl pt.pkl books.pkl similarity_scores.pkl ./
```

### 2. Dependencies install karo
```bash
pip install -r requirements.txt
```

### 3. Flask backend start karo
```bash
python app.py
```
→ Backend chalega `http://localhost:5000` pe

### 4. Frontend open karo
`frontend/index.html` ko browser mein open karo.

---

## 🔌 API Endpoints

| Method | Endpoint            | Description                          |
|--------|---------------------|--------------------------------------|
| GET    | `/api/popular`      | Top 50 popular books return karta hai |
| POST   | `/api/recommend`    | Similar books recommend karta hai    |
| GET    | `/api/titles`       | Autocomplete ke liye saare titles    |
| GET    | `/`                 | Health check                         |

### POST `/api/recommend` — Request body:
```json
{ "title": "Harry Potter and the Sorcerer's Stone (Book 1)" }
```

### Response:
```json
[
  { "title": "...", "author": "...", "image": "..." },
  ...
]
```

---

## 🌐 Production Deploy (Render / Railway)

```bash
gunicorn app:app
```

Set `Procfile`:
```
web: gunicorn app:app
```

---

## ⚙️ Notes

- Backend uses a **pandas 3.x compatibility patch** — pickle files purane pandas se bane the, koi issue nahi.
- Frontend standalone hai — koi npm/build step nahi chahiye.
- Agar server alag port pe ho, `frontend/index.html` mein `const API` update karo.
