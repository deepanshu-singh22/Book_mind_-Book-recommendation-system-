"""
Book Recommender System — Flask Backend
Supports pandas 3.x with pickle files created on older pandas versions.
"""

import sys
from types import ModuleType

# ── Pandas backward-compat shim ──────────────────────────────────────────────
import pandas as pd

for _mod in ["pandas.core.indexes.numeric", "pandas.core.indexes.int64"]:
    _fake = ModuleType(_mod)
    _fake.Int64Index   = pd.Index
    _fake.Float64Index = pd.Index
    _fake.UInt64Index  = pd.Index
    sys.modules[_mod]  = _fake

import pandas.core.internals.blocks as _blks
import pandas._libs.internals as _int

_orig_new_block = _blks.new_block

def _compat_new_block(values, placement=None, *, ndim, refs=None):
    if isinstance(placement, slice):
        placement = _int.BlockPlacement(placement)
    return _orig_new_block(values, placement, ndim=ndim, refs=refs)

_blks.new_block = _compat_new_block
# ── End shim ─────────────────────────────────────────────────────────────────

import pickle
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

# ── Load model artifacts ──────────────────────────────────────────────────────
popular_df        = pickle.load(open("popular.pkl",          "rb"))
pivot_table       = pickle.load(open("pivot_table.pkl",      "rb"))
books             = pickle.load(open("books.pkl",            "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl","rb"))

# ── Build rating lookup from pivot_table (covers ALL 706 books) ───────────────
# pivot_table: rows = book titles, cols = users, values = ratings (0 = no rating)
rating_lookup = {}

for book_title in pivot_table.index:
    row     = pivot_table.loc[book_title]
    rated   = row[row > 0]           # sirf jinlogon ne rating di
    if len(rated) > 0:
        rating_lookup[book_title] = {
            "votes":  int(len(rated)),
            "rating": round(float(rated.mean()), 2),
        }

# popular_df ke ratings se override karo (zyada accurate hain)
for _, row in popular_df.iterrows():
    rating_lookup[row["Book-Title"]] = {
        "votes":  int(row["num_ratings"]),
        "rating": round(float(row["avg_rating"]), 2),
    }

app = Flask(__name__)
CORS(app)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/api/popular", methods=["GET"])
def popular():
    """Return top-50 popular books."""
    result = []
    for _, row in popular_df.iterrows():
        result.append({
            "title":  row["Book-Title"],
            "author": row["Book-Author"],
            "image":  row["Image-URL-M"],
            "votes":  int(row["num_ratings"]),
            "rating": round(float(row["avg_rating"]), 2),
        })
    return jsonify(result)


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Body JSON: { "title": "<book title>" }
    Returns a list of 4 similar books with ratings.
    """
    body = request.get_json(force=True) or {}
    user_input = body.get("title", "").strip()

    if not user_input:
        return jsonify({"error": "title is required"}), 400

    matches = np.where(pivot_table.index == user_input)[0]
    if len(matches) == 0:
        return jsonify({"error": f"Book '{user_input}' not found in index"}), 404

    idx = matches[0]
    similar_items = sorted(
        enumerate(similarity_scores[idx]),
        key=lambda x: x[1],
        reverse=True,
    )[1:5]

    data = []
    for i, _score in similar_items:
        book_title = pivot_table.index[i]
        temp_df = books[books["Book-Title"] == book_title].drop_duplicates("Book-Title")
        if temp_df.empty:
            continue
        row = temp_df.iloc[0]

        book_data = {
            "title":  row["Book-Title"],
            "author": row["Book-Author"],
            "image":  row["Image-URL-M"],
        }

        # Har book ki rating pivot_table se milegi
        rating_info = rating_lookup.get(book_title, {})
        if rating_info:
            book_data["votes"]  = rating_info["votes"]
            book_data["rating"] = rating_info["rating"]

        data.append(book_data)

    return jsonify(data)


@app.route("/api/titles", methods=["GET"])
def titles():
    """Return all indexed book titles (for autocomplete)."""
    return jsonify(list(pivot_table.index))


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "books_indexed": len(pivot_table.index)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)