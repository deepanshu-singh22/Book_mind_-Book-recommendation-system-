# 📚 Book Recommender System

## Overview
Is project mein UI **Flask** se banaya gaya hai aur ek **Popularity-Based + Collaborative Filtering** Recommender System implement kiya gaya hai.

---

## 🎯 Recommender System Kya Hota Hai?

Recommender System ka kaam hota hai user ko unki pasand ke hisaab se cheezein suggest karna. Ye 4 types ka hota hai:

### i) Popularity Based Recommender System
- Platform pe jo cheezein sabse zyada popular hain unhe sabko dikhaate hain.
- Example: "Top 50 Books" — jo sabse zyada logo ne read/rate ki hain.

### ii) Content-Based Recommender System
- Content ki **similarity** ke basis par recommendation aata hai.
- Matlab agar ek book pasand hai to usse milti-julti doosri books recommend hoti hain.

### iii) Collaborative Filtering Based Recommender System
- User ke **pasand ke hisaab** se cheezein recommend ki jaati hain.
- Example: Ek movie ko ek user ne kitna rate kiya — iske basis par similar users ko same movie recommend hoti hai.

### iv) Hybrid Recommender System
- Dono approaches (Content-Based + Collaborative) ko milake sahi tarike se cheezein recommend ki jaati hain.

---

## 🏗️ Is Project Mein Kya Banaya?

**Popularity Based Recommendation System** — Taaki hum **Top 50 Books** dikha sakein jo sabse zyada popular hain.

**Collaborative Filtering** — Taaki user koi bhi book search kare to usse similar books recommend ho sakein.

---

## 📊 Data ki Jankari

Hamare paas 2 cheezein thi:
- **Books data** — Book ka naam, ISBN, Author, Image, etc.
- **Ratings data** — `User-ID → Book-ID → Rating`

In dono ko milake ek **naya data** create kiya gaya — **Pivot Table**.

---

## 🔢 Pivot Table Kaise Bani?

```
           User1   User2   User3  ...  User810
Book1        5       6       0    ...     7
Book2        0       3       8    ...     0
...
Book706
```

- Rows = Books
- Columns = Users
- Values = Rating (0 matlab us user ne rate nahi kiya)

### Filter Conditions (Experimental Data):
Data ko clean karne ke liye sirf wahi records rakhe:

- ✅ **Users > 200** — Jin books ko minimum **200 users** ne rating di ho
- ✅ **Books > 50** — Jinhe minimum **50 users** ne rating di ho

Isse **sparse data** hataya gaya aur meaningful data raha.

---

## 📐 Final Pivot Table Shape: (706 × 810)

```
706  →  Books (rows)
810  →  Users (columns)
```

Matlab har book ek **810-dimensional vector** ban gayi.

---

## 📏 Similarity Kaise Calculate Ki?

Har book ab ek vector hai (810 numbers). Ab in vectors ke beech **cosine similarity** calculate ki gayi:

```
Book1  →  [5, 6, 0, 7, ...]   ← 810 dimensions
Book2  →  [0, 3, 8, 0, ...]   ← 810 dimensions
```

Jo books **zyada similar** hain (vector direction same hai), unhe recommend kiya jaata hai.

---

## ⚙️ Tech Stack

| Component  | Technology           |
|------------|----------------------|
| Backend    | Python, Flask        |
| Frontend   | HTML, CSS, JavaScript|
| ML Library | NumPy, Pandas        |
| Model      | Cosine Similarity    |
| Data       | Book-Crossing Dataset|

---

## 🚀 Run Karne Ka Tarika

```bash
# 1. Dependencies install karo
pip install flask flask-cors numpy pandas

# 2. Backend chalao
python app.py

# 3. Browser mein index.html open karo
```

Backend chalega: `http://127.0.0.1:5000`

---

## 🔌 API Endpoints

| Method | Endpoint         | Kaam                              |
|--------|------------------|-----------------------------------|
| GET    | `/api/popular`   | Top 50 popular books return karta |
| POST   | `/api/recommend` | Similar books recommend karta     |
| GET    | `/api/titles`    | Autocomplete ke liye saare titles |
| GET    | `/`              | Health check                      |

---

## 📁 Project Structure

```
Book_recommendation_system/
├── app.py                  ← Flask Backend
├── index.html              ← Frontend UI
├── popular.pkl             ← Top 50 books data
├── pivot_table.pkl         ← User-Book matrix (706×810)
├── books.pkl               ← Books metadata
└── similarity_scores.pkl   ← Cosine similarity matrix
```
