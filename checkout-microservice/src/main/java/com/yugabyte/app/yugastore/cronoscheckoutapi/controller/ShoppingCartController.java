package com.yugabyte.app.yugastore.cronoscheckoutapi.controller;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.yugabyte.app.yugastore.cronoscheckoutapi.service.OrderCheckoutService;

@RestController
@RequestMapping(value = "/cronos-checkout-api")
public class ShoppingCartController {
	
	@Autowired
	OrderCheckoutService orderCheckoutService;
	
	@RequestMapping(method = RequestMethod.GET, value = "/shoppingCart/addProduct", produces = "application/json")
	public String addProductToCart(@RequestParam("userid") String userId, 
			@RequestParam("asin") String asin) {
		orderCheckoutService.addProductToShoppingCart(userId, asin);
		return String.format("Added to Cart");
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/shoppingCart/productsInCart", produces = "application/json")
	public Map<String, Integer> getProductsInCart(@RequestParam("userid") String userId) {
		return orderCheckoutService.getProductsInCart(userId);
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/shoppingCart/removeProduct", produces = "application/json")
	public String removeProductFromCart(@RequestParam("userid") String userId, 
			@RequestParam("asin") String asin) {
		orderCheckoutService.removeProductFromCart(userId, asin);
		return String.format("Removing from Cart");
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/shoppingCart/clearCart", produces = "application/json")
	public String clearCart(@RequestParam("userid") String userId) {
		 orderCheckoutService.clearCart(userId);
		 return String.format("Clearing Cart, Checkout successful");
	}
}
