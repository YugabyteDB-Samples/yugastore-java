package com.yugabyte.app.yugastore.service;

import java.util.Map;

public interface ShoppingCartServiceRest {
	
	String addProduct(String userId, String product);
	Map<String, Integer> getProductsInCart(String userId);
	String removeProduct(String userId, String product);
	String clearCart(String userId);
}
