import requests
import json

BACKEND_URL = "https://community-backend-778734323929.europe-west1.run.app"

def fetch_categories_with_top(days=30, limit=20):
    url = f"{BACKEND_URL}/api/categories_with_top?days={days}&limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  # fingir que é browser
        "Accept": "application/json",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

# Mostra a resposta completa
#print(json.dumps(data, indent=2, ensure_ascii=False))
import json
from collections import defaultdict

# Carrega o ficheiro JSON
with open("backend/app/demo_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Mapeamentos úteis
products = {p["id"]: p for p in data["products"]}  # id → info do produto
categories = {c["id"]: c["name"] for c in data["categories"]}  # id → nome da categoria

# Dicionário: category_id → dict de product_id → quantidade total
category_sales = defaultdict(lambda: defaultdict(int))

# Percorre todas as orders e soma quantidades por categoria
for order in data["orders"]:
    for item in order["products"]:
        product_id = item["id"]
        qty = item["qty"]
        category_id = products[product_id]["category_id"]
        category_sales[category_id][product_id] += qty

# Mostra o top vendido por categoria
for category_id, sales in category_sales.items():
    category_name = categories[category_id]
    print(f"\n Category: {category_name}")
    
    # Ordena os produtos por quantidade vendida (decrescente)
    sorted_sales = sorted(sales.items(), key=lambda x: x[1], reverse=True)
    
    for product_id, total_qty in sorted_sales:
        product_name = products[product_id]["name"]
        print(f"  {product_name}: {total_qty} units sold")

expected_top_product = {
    "Queijos": "Queijo de Azeitão",
    "Doces": "Bolo de Mel da Madeira",
    "Conservas": "Mexilhão em Escabeche",
    "Azeites": "Azeite Trás-os-Montes 750ml",
    "Vinhos": "Vinho Tinto Douro",
    # adiciona mais categorias e produtos esperados aqui
}

def test_first_product():
    data = fetch_categories_with_top()
    
    for category in data:
        category_data = category.get("category")  # agora é um dict
        category_name = category_data.get("name")  # agora é uma string

        top_products = category.get("top", [])    # ou "top_products"
        
        if not top_products:
            print(f"Category '{category_name}' has no products sold")
            continue
        
        first_product_name = top_products[0].get("name")  # ou a chave que indica o nome do produto
        
        expected_product = expected_top_product.get(category_name)
        
        if expected_product is None:
            print(f"No product defined for category'{category_name}'")
            continue
        
        if first_product_name == expected_product:
            print(f"Category '{category_name}': 1st product right ({first_product_name})")
        else:
            print(f"Category '{category_name}': 1st product wrong")
            print(f"   Expected: {expected_product}")
            print(f"   Recieved: {first_product_name}")

if __name__ == "__main__":
    test_first_product()