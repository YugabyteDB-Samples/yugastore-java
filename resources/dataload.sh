for i in dataToLoad/x*; do echo $i; python parse_metadata_json.py $i; 
./cassandra-loader -f cronos_products.csv -host 35.224.62.157 -schema "cronos.products(asin, title, description, price, imUrl, also_bought, also_viewed, bought_together, buy_after_viewing, brand, categories,num_reviews,num_stars,avg_stars)" -maxInsertErrors 10000 -maxErrors 10000 -charsPerColumn 256000;
./cassandra-loader -f cronos_product_rankings.csv -host 35.224.62.157 -schema "cronos.product_rankings(asin, category, sales_rank, title, price, imurl, num_reviews, num_stars, avg_stars)" -maxInsertErrors 10000 -maxErrors 10000 -charsPerColumn 256000;
./cassandra-loader -f cronos_product_inventory.csv -host 35.224.62.157 -schema "cronos.product_inventory(asin, quantity)";
mv $i done$i; 
done