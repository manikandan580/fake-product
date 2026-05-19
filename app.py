import os
import csv
import requests
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for



# 👉 helpers import
from utils.helpers import get_reviews_by_ratio, load_reviews, predict_reviews

# Try to import the scraper, handle if not available
try:
    from utils.web_scraper import ProductScraper
    SCRAPER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Web scraper not available: {e}")
    SCRAPER_AVAILABLE = False


app = Flask(__name__)
app.secret_key = "secret123"

# 📁 Folders
UPLOAD_FOLDER = "static/uploads"
DATASET_FOLDER = "dataset"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

# 📄 Files
PRODUCT_CSV = os.path.join(DATASET_FOLDER, "products.csv")
REVIEW_CSV = os.path.join(DATASET_FOLDER, "reviews.csv")



# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- PRODUCT UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        # ================= IMAGE =================
        image_file = request.files.get("image_file")
        image_url = request.form.get("image_url")
        image_name = "default.jpg"

        if image_file and image_file.filename != "":
            image_name = image_file.filename
            image_file.save(os.path.join(UPLOAD_FOLDER, image_name))

        elif image_url:
            try:
                image_name = image_url.split("/")[-1]
                img_data = requests.get(image_url).content
                with open(os.path.join(UPLOAD_FOLDER, image_name), 'wb') as f:
                    f.write(img_data)
            except:
                image_name = "default.jpg"

        # ================= PRODUCT DATA =================
        title = request.form.get("title")
        price = request.form.get("price")
        description = request.form.get("description")
        features = request.form.get("features", "")
        address = request.form.get("address", "")
        brand = request.form.get("brand", "")
        rating = request.form.get("rating", "")
        link = request.form.get("link", "")

        # ================= REVIEW LOGIC =================
        review_option = request.form.get("review_option")
        manual_reviews = request.form.get("reviews", "")

        if review_option == "manual":
            reviews_list = [r.strip() for r in manual_reviews.split("\n") if r.strip()]
        else:
            review_ratio = request.form.get("review_ratio", "50_50")
            reviews_list = get_reviews_by_ratio(review_ratio)

        # ================= SAVE PRODUCT =================
        file_exists = os.path.exists(PRODUCT_CSV)

        # Use csv module with proper quoting to handle commas and special characters
        with open(PRODUCT_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, escapechar='\\')

            if not file_exists:
                writer.writerow([
                    "image", "title", "price", "description",
                    "features", "address", "brand", "rating", "link"
                ])

            # Clean the data to avoid issues
            writer.writerow([
                image_name, 
                title.replace(',', ' ').replace('\n', ' '), 
                price, 
                description.replace(',', ' ').replace('\n', ' '),
                features.replace(',', ' ').replace('\n', ' '), 
                address.replace(',', ' ').replace('\n', ' '), 
                brand.replace(',', ' ').replace('\n', ' '), 
                rating, 
                link
            ])

        # ================= SAVE REVIEWS =================
        file_exists = os.path.exists(REVIEW_CSV)

        with open(REVIEW_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)

            if not file_exists:
                writer.writerow(["product_link", "review_text", "label"])

            for r in reviews_list:
                writer.writerow([link, r.replace(',', ' ').replace('\n', ' '), "unknown"])

        flash("✅ Product Uploaded Successfully!", "success")
        return redirect(url_for("upload"))

    return render_template("upload.html")

# Add this function to convert data types when reading CSV
def convert_product_types(product_dict):
    """Convert string values to appropriate types"""
    if 'price' in product_dict and product_dict['price']:
        try:
            product_dict['price'] = float(product_dict['price'])
        except:
            product_dict['price'] = 0.0
    
    if 'rating' in product_dict and product_dict['rating']:
        try:
            product_dict['rating'] = float(product_dict['rating'])
        except:
            product_dict['rating'] = 0.0
    
    return product_dict

# Updated safe CSV reader function
def safe_read_csv(file_path):
    """Safely read CSV file with error handling"""
    try:
        # Try reading with pandas first
        df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
        return df
    except Exception as e:
        print(f"Error reading with pandas: {e}")
        # Fallback to manual CSV reading
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, quotechar='"', quoting=csv.QUOTE_ALL)
                for row in reader:
                    data.append(row)
            
            if data:
                headers = data[0]
                rows = data[1:]
                df = pd.DataFrame(rows, columns=headers)
                return df
            else:
                return pd.DataFrame()
        except Exception as e2:
            print(f"Error reading with csv module: {e2}")
            return pd.DataFrame()

# ---------------- PRODUCT VIEW ----------------
@app.route("/products")
def view_products():
    products = []

    if os.path.exists(PRODUCT_CSV):
        try:
            # Use safe CSV reader
            df = safe_read_csv(PRODUCT_CSV)
            
            if not df.empty:
                products = df.to_dict(orient="records")
                # Convert data types for each product
                products = [convert_product_types(p) for p in products]
            else:
                print("DataFrame is empty")
        except Exception as e:
            print(f"Error reading products: {e}")
            flash(f"Error loading products: {str(e)}", "error")

    return render_template("view_products.html", products=products)

# ---------------- PRODUCT DETAIL ----------------
@app.route("/product/<int:id>")
def product(id):
    try:
        if os.path.exists(PRODUCT_CSV):
            df = safe_read_csv(PRODUCT_CSV)
            
            if not df.empty and id < len(df):
                product = df.iloc[id].to_dict()
                product = convert_product_types(product)
                
                # Handle NaN values
                if pd.isna(product.get('features', '')):
                    product['features'] = ''
                if pd.isna(product.get('address', '')):
                    product['address'] = ''
                if pd.isna(product.get('brand', '')):
                    product['brand'] = ''
                    
                return render_template("product_detail.html", product=product)
            else:
                flash("Product not found!", "error")
                return redirect(url_for("view_products"))
        else:
            flash("No products available!", "error")
            return redirect(url_for("view_products"))
    except Exception as e:
        print(f"Error in product route: {e}")
        flash(f"Error loading product details: {str(e)}", "error")
        return redirect(url_for("view_products"))

# ---------------- PRODUCT DETECTION ----------------
@app.route("/product_detection", methods=["GET", "POST"])
def product_detection():

    product = None
    result = None

    if request.method == "POST":
        link = request.form.get("link")

        if os.path.exists(PRODUCT_CSV):
            df = safe_read_csv(PRODUCT_CSV)
            
            if not df.empty:
                matched = df[df['link'] == link]

                if not matched.empty:
                    product = matched.iloc[0].to_dict()
                    product = convert_product_types(product)

                    # SIMPLE RULE
                    try:
                        price = float(product['price']) if product['price'] else 0
                        rating = float(product['rating']) if product['rating'] else 0

                        if price < 100 or rating > 4.8:
                            result = "Fake Product ❌"
                        else:
                            result = "Real Product ✅"
                    except:
                        result = "Unable to determine ❓"
                else:
                    flash("❌ Product not found! Please check the product link.", "error")
            else:
                flash("❌ No products found in database!", "error")

    return render_template("product_detection.html",
                           product=product,
                           result=result)

# ---------------- REVIEW DETECTION ----------------
@app.route("/review_detection", methods=["GET", "POST"])
def review_detection():

    product = None
    reviews = []
    fake_percent = 0
    real_percent = 0
    error = None

    if request.method == "POST":

        link = request.form.get("link")

        # Get product details
        if os.path.exists(PRODUCT_CSV):
            df_products = safe_read_csv(PRODUCT_CSV)
            
            if not df_products.empty:
                matched_product = df_products[df_products['link'] == link]
                
                if not matched_product.empty:
                    product = matched_product.iloc[0].to_dict()
                    product = convert_product_types(product)

        # Get reviews
        try:
            df = load_reviews()
            if not df.empty:
                matched = df[df['product_link'] == link]

                if not matched.empty:

                    review_list = matched['review_text'].tolist()

                    fake_count = 0
                    real_count = 0

                    for r in review_list:
                        try:
                            fake_score, real_score = predict_reviews(r)
                            label = "Fake" if fake_score > real_score else "Real"

                            if label == "Fake":
                                fake_count += 1
                            else:
                                real_count += 1

                            reviews.append({
                                "review_text": r,
                                "predicted": label
                            })
                        except Exception as e:
                            print(f"Error predicting review: {e}")

                    total = len(review_list)
                    if total > 0:
                        fake_percent = int((fake_count / total) * 100)
                        real_percent = int((real_count / total) * 100)

                else:
                    error = "❌ No reviews found for this product!"
                    if not product:
                        error = "❌ Product not found! Please check the product link."
            else:
                error = "❌ No reviews found in database!"
        except Exception as e:
            print(f"Error loading reviews: {e}")
            error = f"❌ Error loading reviews: {str(e)}"

    return render_template(
        "review_detection.html",
        product=product,
        reviews=reviews,
        fake_percent=fake_percent,
        real_percent=real_percent,
        error=error
    )


    

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)