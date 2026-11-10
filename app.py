
from flask import Flask, redirect, url_for, session, request, render_template_string

app = Flask(__name__)
app.secret_key = "nova-store-demo-key"

STORE_EMAIL = "nova789.store.official@gmail.com"

products = [
    {"id": 1, "name": "RGB Gaming Keyboard", "price": 89, "category": "Gaming", "emoji": "⌨️", "stock": True},
    {"id": 2, "name": "RGB Gaming Mouse", "price": 59, "category": "Gaming", "emoji": "🖱️", "stock": True},
    {"id": 3, "name": "Gaming Headset", "price": 119, "category": "Gaming", "emoji": "🎧", "stock": True},
    {"id": 4, "name": "PlayStation Controller", "price": 179, "category": "Gaming", "emoji": "🎮", "stock": True},
    {"id": 5, "name": "Gaming Monitor", "price": 499, "category": "Gaming", "emoji": "🖥️", "stock": False},
    {"id": 6, "name": "Gaming Chair", "price": 518.70, "category": "Gaming", "emoji": "🪑", "stock": False},
    {"id": 7, "name": "NOVA Black Hoodie", "price": 89, "category": "Fashion", "emoji": "🧥", "stock": False},
    {"id": 8, "name": "NOVA Street T-Shirt", "price": 49, "category": "Fashion", "emoji": "👕", "stock": False},
    {"id": 9, "name": "NOVA Sneakers", "price": 159, "category": "Fashion", "emoji": "👟", "stock": False},
    {"id": 10, "name": "NOVA Cap", "price": 39, "category": "Fashion", "emoji": "🧢", "stock": False},
]

STYLE = """
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #090b14;
    color: white;
    font-family: Arial, sans-serif;
}
header {
    background: #111526;
    padding: 20px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
    border-bottom: 1px solid #242c46;
}
.logo {
    font-size: 28px;
    font-weight: 900;
    color: #35d9ff;
}
nav a {
    color: white;
    text-decoration: none;
    margin: 0 12px;
    font-weight: bold;
}
nav a:hover { color: #35d9ff; }
.hero {
    text-align: center;
    padding: 65px 20px;
    background: radial-gradient(ellipse, #192a50, #090b14 70%);
}
.hero h1 { font-size: 46px; margin: 10px; }
.hero span { color: #35d9ff; }
.hero p { color: #b8c2dc; }
.search {
    padding: 13px;
    width: min(90%, 400px);
    border-radius: 10px;
    border: 1px solid #34466c;
    background: #141b2e;
    color: white;
}
main { padding: 30px 7%; }
h2 { color: #35d9ff; }
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 22px;
}
.card {
    background: #141a2a;
    border: 1px solid #28334e;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transition: .2s;
}
.card:hover {
    border-color: #35d9ff;
    transform: translateY(-4px);
}
.emoji {
    font-size: 65px;
    background: #202a43;
    border-radius: 12px;
    padding: 20px;
}
.price {
    color: #35d9ff;
    font-size: 22px;
    font-weight: bold;
}
button, .btn {
    background: linear-gradient(90deg, #147dff, #8b45ff);
    border: 0;
    color: white;
    padding: 12px 18px;
    border-radius: 9px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
}
button:disabled {
    background: #555;
    cursor: not-allowed;
}
.stock { color: #ff647c; font-weight: bold; }
.available { color: #57e69a; }
footer {
    text-align: center;
    color: #9ca9c5;
    padding: 30px;
    border-top: 1px solid #242c46;
    margin-top: 40px;
}
a { color: #35d9ff; }
.total {
    font-size: 25px;
    color: #35d9ff;
}
</style>
"""

PAGE = """
<!DOCTYPE html>
<html>
<meta name="google-site-verification" content="w_S-vsUzbSZlFxl5p7ebnZrJWkjhpLvsnHALC2rCxos" />
<title>NOVA STORE</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
""" + STYLE + """
</head>
<body>
<header>
 <div class="logo">✦ NOVA STORE</div>
 <nav>
  <a href="/">Home</a>
  <a href="/gaming">Gaming</a>
  <a href="/fashion">Fashion</a>
  <a href="/contact">Contact</a>
  <a href="/cart">Cart ({{ count }})</a>
 </nav>
</header>
{{ content|safe }}
<footer>© 2026 NOVA STORE · Gaming & Fashion · Prices in DT</footer>
</body>
</html>
"""

def show(content):
    count = sum(session.get("cart", {}).values())
    return render_template_string(PAGE, content=content, count=count)

def product_cards(category):
    items = [p for p in products if p["category"] == category]
    return render_template_string("""
    <main>
      <h2>{{ category }} Collection</h2>
      <input class="search" id="search" placeholder="Search products..." oninput="filterProducts()">
      <div class="grid" id="products">
      {% for p in items %}
       <div class="card">
        <div class="emoji">{{ p.emoji }}</div>
        <h3>{{ p.name }}</h3>
        <div class="price">{{ "%.2f"|format(p.price) }} DT</div>
        {% if p.stock %}
         <p class="available">● In Stock</p>
         <form method="POST" action="/add/{{ p.id }}">
            <button>Add to Cart</button>
         </form>
        {% else %}
         <p class="stock">● OUT OF STOCK</p>
         <button disabled>Unavailable</button>
        {% endif %}
       </div>
      {% endfor %}
      </div>
    </main>
    <script>
    function filterProducts() {
      let q = document.getElementById('search').value.toLowerCase();
      document.querySelectorAll('#products .card').forEach(card => {
        card.style.display = card.innerText.toLowerCase().includes(q) ? 'block' : 'none';
      });
    }
    </script>
    """, category=category, items=items)

@app.route("/")
def home():
    content = """
    <section class="hero">
      <h1>WELCOME TO <span>NOVA STORE</span></h1>
      <p>Your next level gaming and fashion destination.</p>
      <a class="btn" href="/gaming">Explore Gaming</a>
      <a class="btn" href="/fashion">Explore Fashion</a>
    </section>
    <main>
      <h2>Discover NOVA</h2>
      <div class="grid">
       <div class="card">
         <div class="emoji">🎮</div>
         <h3>Gaming</h3>
         <a class="btn" href="/gaming">Shop Gaming</a>
       </div>
       <div class="card">
         <div class="emoji">👕</div>
         <h3>Fashion</h3>
         <a class="btn" href="/fashion">Shop Fashion</a>
       </div>
       <div class="card">
         <div class="emoji">🛒</div>
         <h3>Your Cart</h3>
         <a class="btn" href="/cart">View Cart</a>
       </div>
      </div>
    </main>
    """
    return show(content)

@app.route("/gaming")
def gaming():
    return show(product_cards("Gaming"))

@app.route("/fashion")
def fashion():
    return show(product_cards("Fashion"))

@app.route("/add/<int:product_id>", methods=["POST"])
def add(product_id):
    p = next((p for p in products if p["id"] == product_id), None)
    if p and p["stock"]:
        cart = session.get("cart", {})
        key = str(product_id)
        cart[key] = cart.get(key, 0) + 1
        session["cart"] = cart
    return redirect(request.referrer or url_for("gaming"))

@app.route("/cart")
def cart():
    cart_data = session.get("cart", {})
    selected = []
    total = 0

    for p in products:
        quantity = cart_data.get(str(p["id"]), 0)
        if quantity:
            subtotal = p["price"] * quantity
            total += subtotal
            selected.append({
                "name": p["name"],
                "price": p["price"],
                "quantity": quantity,
                "subtotal": subtotal
            })

    content = render_template_string("""
    <main>
      <h2>Your Shopping Cart 🛒</h2>
      {% if selected %}
        {% for p in selected %}
        <div class="card" style="margin:12px 0;text-align:left">
          <b>{{ p.name }}</b> · {{ p.quantity }} × {{ "%.2f"|format(p.price) }} DT
          <span style="float:right">{{ "%.2f"|format(p.subtotal) }} DT</span>
        </div>
        {% endfor %}
        <p class="total">Total: {{ "%.2f"|format(total) }} DT</p>
      {% else %}
        <p>Your cart is empty. Go explore our store!</p>
      {% endif %}
      <a class="btn" href="/gaming">Continue Shopping</a>
    </main>
    """, selected=selected, total=total)

    return show(content)

@app.route("/contact")
def contact():
    content = """
    <main>
      <h2>Contact NOVA STORE</h2>
      <div class="card">
        <div class="emoji">📧</div>
        <h3>Need Help?</h3>
        <p>Contact our team for questions about products and orders.</p>
        <p>Email:
          <a href="mailto:nova789.store.official@gmail.com">
          nova789.store.official@gmail.com</a>
        </p>
        <a class="btn" href="mailto:nova789.store.official@gmail.com">
          Send us an Email
        </a>
      </div>
    </main>
    """
    return show(content)

if __name__ == "__main__":
    app.run(debug=True)

