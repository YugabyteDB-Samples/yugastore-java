package io.pivotal.cronos.ui.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import io.pivotal.cronos.ui.rest.DashboardRestConsumer;

@RestController
public class CronosProductsController {
	
	@Autowired
	DashboardRestConsumer dashboardRestConsumer;

	@GetMapping("/products")
	public String getProductDetails() {
		return dashboardRestConsumer.getHomePageProducts(10, 0);
		//return "[{\"id\": 5,\"name\": \"How to Win Friends & Influence People\",\"description\": \"For more than sixty years the rock-solid\",\"price\": 9.6,\"author\": \"Dale Carnegie\",\"type\": \"paperback\",\"img\": \"https://images-na.ssl-images-amazon.com/images/I/51PWIy1rHUL._AA300_.jpg\",\"category\": \"business\",\"num_reviews\": 182,\"total_stars\": 550,\"stars\": \"3.02\"}]";
	}

	@GetMapping("/products/category")
	public String getProductDetails(@RequestParam("name") String name, @RequestParam("limit") int limit, @RequestParam("offset") int offset) {
		return dashboardRestConsumer.getProductsByCategory(name, limit, offset);
	}

  @RequestMapping(method = RequestMethod.GET, value = "/products/details")
  public @ResponseBody String getProductDetails(@RequestParam("asin") String asin) {
    return dashboardRestConsumer.getProductDetails(asin);
  }

  @PostMapping("/cart/add")
	public @ResponseBody String addProductToCart(@RequestParam("asin") String asin) {
		return dashboardRestConsumer.addProductToCart(asin);
	}
  
  @PostMapping("/cart/get")
	public @ResponseBody String showCart() {
		return dashboardRestConsumer.showCart();
	}
  
  @PostMapping("/cart/checkout")
	public @ResponseBody String checkoutCart() {
		return dashboardRestConsumer.checkout();
	}

  @RequestMapping(method = RequestMethod.POST, value = "/cart/remove")
	public @ResponseBody String removeProductFromCart(@RequestParam("asin") String asin) {
		return dashboardRestConsumer.removeProductFromCart(asin);
	}

  @RequestMapping(method = RequestMethod.POST, value = "/cart/getCart")
	public @ResponseBody String getCart() {
		return dashboardRestConsumer.getCart();
	}
}
