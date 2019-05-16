import json
import sys
import random, math

def safe_encode(str):
    str1 = str.replace('\\', "\\\\")
    return ('"' + str1.replace('"', '\\"').replace("\n"," ").strip().decode('utf-8', 'ignore') + '"')

def collection_to_str(items, start_sep, end_sep):
    if len(items) == 0:
        return ""
    tmp = start_sep
    first = True
    for item in items:
        if (first):
            first = False
        else:
            tmp += ","
        tmp += item
    tmp += end_sep
    return safe_encode(tmp)

def parse_and_write_metadata(product, f_products, f_rankings, f_inventory):
    """
    This function takes a json object that represents the details of a product as input, parses it,
    and writes a line of CSV to the output files in the format the YugaByte DB loader expects.
    """
    num_reviews = random.randint(100, 1000)
    num_stars = round((random.random() * 2 * num_reviews + 3 * num_reviews),2)
    avg_stars = round(num_stars / num_reviews,2)
    default_price = round(random.uniform(20,800), 2)

    if "description" in product:
        f_products.write(product["asin"])
        f_products.write(",")
        if "title" in product:
            f_products.write(safe_encode(product["title"]))
        f_products.write(",")
        #if "description" in product:
        f_products.write(safe_encode(product.get("description", "")))
        f_products.write(",")
        #if "price" in product:
        f_products.write(str(product.get("price", default_price)))
        f_products.write(",")
        if "imUrl" in product:
            f_products.write(safe_encode(product["imUrl"]))
        f_products.write(",")
        if ("related" in product):
            f_products.write(collection_to_str(product["related"].get("also_bought", []), "[", "]"))
        f_products.write(",")
        if ("related" in product):
            f_products.write(collection_to_str(product["related"].get("also_viewed", []), "[", "]"))
        f_products.write(",")
        if ("related" in product):
            f_products.write(collection_to_str(product["related"].get("bought_together", []), "[", "]"))
        f_products.write(",")
        if ("related" in product):
            f_products.write(collection_to_str(product["related"].get("buy_after_viewing", []), "[", "]"))
        f_products.write(",")
        f_products.write(product.get("brand", ""))
        f_products.write(",")
        if "categories" in product:
            f_products.write(collection_to_str(product["categories"][0], "{", "}"))
        f_products.write(",")
        #num_reviews generated
        #f_products.write(str(random.randint(100, 5000)))
        f_products.write(str(num_reviews))
        f_products.write(",")
        #total_stars generated
        f_products.write(str(num_stars))
        f_products.write(",")
        #avg_stars generated
        f_products.write(str(avg_stars))
        f_products.write("\n")
        #Product Inventory
        f_inventory.write(product["asin"])
        f_inventory.write(",")
        f_inventory.write(str(random.randint(100, 1000)))
        f_inventory.write("\n")
        if ("salesRank" in product):
            for category, rank in product["salesRank"].items():
                f_rankings.write(product["asin"])
                f_rankings.write(",")
                f_rankings.write(safe_encode(category))
                f_rankings.write(",")
                f_rankings.write(str(rank))
                f_rankings.write(",")
                if "title" in product:
                    f_rankings.write(safe_encode(product["title"]))
                f_rankings.write(",")
                f_rankings.write(str(product.get("price", default_price)))
                f_rankings.write(",")
                if "imUrl" in product:
                    f_rankings.write(safe_encode(product["imUrl"]))
                f_rankings.write(",")
                f_rankings.write(str(num_reviews))
                f_rankings.write(",")
                f_rankings.write(str(num_stars))
                f_rankings.write(",")
                f_rankings.write(str(avg_stars))
                f_rankings.write("\n")

# The input data file.
if len(sys.argv) < 2:
    print "Error: Metadata file (one JSON product info per line) argument expected."
    exit()
metadata_file = str(sys.argv[1])
print ("Processing file: %s " % metadata_file)

# This is the file to which the product data is written.
f_products = open('cronos_products.csv', 'w')

# This is the file to which the product asin, categories and sales rank related info is written.
f_rankings = open('cronos_product_rankings.csv', 'w')

# This is the file to which the product inventory is written

f_inventory = open('cronos_product_inventory.csv', 'w')

#
# Read and parse the metadata input file one line at a time. The output is 2 csv files, which have
# the following columns:
#   cronos_products.csv:
#     asin, title, price, imUrl, also_bought, also_viewed, bought_together, brand, categories
#   cronos_product_rankings.csv
#     asin, category, sales_rank
#
with open(metadata_file) as f:
    for line in f:
        product = json.loads(line)
        # Parse and write out the product info.
        parse_and_write_metadata(product, f_products, f_rankings, f_inventory)

# Close the various files.
f_products.close()
f_rankings.close()
f_inventory.close()
