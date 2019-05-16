CREATE TABLE shopping_cart(
  cart_key TEXT NOT NULL,
  user_id TEXT NOT NULL,
  asin TEXT NOT NULL,
  time_added TEXT NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (cart_key)
);