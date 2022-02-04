package com.yugabyte.app.yugastore.rest.clients;

import java.util.Map;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient("cart-microservice")
public interface ShoppingCartRestClient {

  @RequestMapping("/cart-microservice/shoppingCart/addProduct")
  String addProductToCart(@RequestParam("userid") String userId,
    @RequestParam("asin") String asin);

  @RequestMapping("/cart-microservice/shoppingCart/productsInCart")
  Map<String, Integer> getProductsInCart(@RequestParam("userid") String userId);

  @RequestMapping("/cart-microservice/shoppingCart/removeProduct")
  String removeProductFromCart(@RequestParam("userid") String userId,
    @RequestParam("asin") String asin);

  @RequestMapping("/cart-microservice/shoppingCart/clearCart")
  String clearCart(@RequestParam("userid") String userId);
}
