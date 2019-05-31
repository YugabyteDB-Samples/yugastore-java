package com.yugabyte.app.yugastore.cronoscheckoutapi.rest.clients;

import java.util.Map;

import org.springframework.cloud.netflix.feign.FeignClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient("cart-microservice")
@RequestMapping("/cart-microservice")
public interface ShoppingCartRestClient {
	
	@RequestMapping("/shoppingCart/addProduct")
	String addProductToCart(@RequestParam("userid") String userId, 
			@RequestParam("asin") String asin);
	
	@RequestMapping("/shoppingCart/productsInCart")
	Map<String, Integer> getProductsInCart(@RequestParam("userid") String userId);
	
	@RequestMapping("/shoppingCart/removeProduct")
	String removeProductFromCart(@RequestParam("userid") String userId, 
			@RequestParam("asin") String asin);
	
	@RequestMapping("/shoppingCart/clearCart")
	String clearCart(@RequestParam("userid") String userId);
}
