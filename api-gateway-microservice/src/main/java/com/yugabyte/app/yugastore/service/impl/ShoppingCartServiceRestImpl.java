package com.yugabyte.app.yugastore.service.impl;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;
import org.springframework.stereotype.Service;
import org.springframework.web.context.WebApplicationContext;

import com.yugabyte.app.yugastore.rest.clients.ShoppingCartRestClient;
import com.yugabyte.app.yugastore.service.ShoppingCartServiceRest;

@Service
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ShoppingCartServiceRestImpl implements ShoppingCartServiceRest {

	private final ShoppingCartRestClient shoppingCartRestClient;

	@Autowired
	public ShoppingCartServiceRestImpl(ShoppingCartRestClient shoppingCartRestClient) {
		this.shoppingCartRestClient = shoppingCartRestClient;
	}

	@Override
	public String addProduct(String userId, String asin) {

		String result = shoppingCartRestClient.addProductToCart(userId, asin);
		return result;
	}

	@Override
	public Map<String, Integer> getProductsInCart(String userId) {

		Map<String, Integer> productsInCart = shoppingCartRestClient.getProductsInCart(userId);
		return productsInCart;
	}

	@Override
	public String removeProduct(String userId, String asin) {
		String result = shoppingCartRestClient.removeProductFromCart(userId, asin);
		return result;
	}

	@Override
	public String clearCart(String userId) {
		String result = shoppingCartRestClient.clearCart(userId);
		return result;
	}

}