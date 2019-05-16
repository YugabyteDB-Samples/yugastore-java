package com.yugabyte.app.yugastore.cronoscheckoutapi.service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ShoppingCart;
import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ShoppingCartKey;
import com.yugabyte.app.yugastore.cronoscheckoutapi.repositories.OrderRepository;
import com.yugabyte.app.yugastore.cronoscheckoutapi.repositories.ProductInventoryRepository;
import com.yugabyte.app.yugastore.cronoscheckoutapi.repositories.ShoppingCartRepository;

@Service
public class OrderCheckoutService {

	private static final int DEFAULT_QUANTITY = 1;
	private final OrderRepository orderRepository;
	private final ProductInventoryRepository productInventoryRepository;
	private final ShoppingCartRepository shoppingCartRepository;

	@Autowired
	public OrderCheckoutService(OrderRepository orderRepository, ProductInventoryRepository productInventoryRepository,
			ShoppingCartRepository shoppingCartRepository) {
		this.orderRepository = orderRepository;
		this.productInventoryRepository = productInventoryRepository;
		this.shoppingCartRepository = shoppingCartRepository;
	}

	/**
	 * If product is in the map just increment quantity by 1. If product is not in
	 * the map with, add it with quantity 1
	 *
	 * @param product
	 */
	public void addProductToShoppingCart(String userId, String asin) {

		ShoppingCartKey currentKey = new ShoppingCartKey(userId, asin);
		String shoppingCartKeyStr = userId + "-" + asin;
		if (shoppingCartRepository.findById(shoppingCartKeyStr).isPresent()) {
//		if (shoppingCartRepository.findByUserIdAndAsin(userId).isPresent()) {
			shoppingCartRepository.updateQuantityForShoppingCart(userId, asin);
			System.out.println("Adding product: " + asin);
		} else {
			ShoppingCart currentShoppingCart = createCartObject(currentKey);
			shoppingCartRepository.save(currentShoppingCart);
			System.out.println("Adding product: " + asin);
		}
	}

	public Map<String, Integer> getProductsInCart(String userId) {

		Map<String, Integer> productsInCartAsin = new HashMap<String, Integer>();

		if (shoppingCartRepository.findProductsInCartByUserId(userId).isPresent()) {

			List<ShoppingCart> productsInCart = shoppingCartRepository.findProductsInCartByUserId(userId).get();
			for (ShoppingCart item : productsInCart) {
				productsInCartAsin.put(item.getAsin(), item.getQuantity());
			}

		}
		return productsInCartAsin;
	}

	public void removeProductFromCart(String userId, String asin) {
		String shoppingCartKeyStr = userId + "-" + asin;
		if (shoppingCartRepository.findById(shoppingCartKeyStr).isPresent()) {
			if (shoppingCartRepository.findById(shoppingCartKeyStr).get().getQuantity() > 1) {
				shoppingCartRepository.decrementQuantityForShoppingCart(userId, asin);
				System.out.println("Decrementing product: " + asin + " quantity");
			} else if (shoppingCartRepository.findById(shoppingCartKeyStr).get().getQuantity() == 1) {
				shoppingCartRepository.deleteById(shoppingCartKeyStr);
				System.out.println("Removing product: " + asin + " since it was qty 1");
			}
		}
	}

	private ShoppingCart createCartObject(ShoppingCartKey currentKey) {
		ShoppingCart currentShoppingCart = new ShoppingCart();
		currentShoppingCart.setCartKey(currentKey.getId() + "-" + currentKey.getAsin());
		currentShoppingCart.setUserId(currentKey.getId());
		currentShoppingCart.setAsin(currentKey.getAsin());
		LocalDateTime currentTime = LocalDateTime.now();
		currentShoppingCart.setTime_added(currentTime.toString());
		currentShoppingCart.setQuantity(DEFAULT_QUANTITY);

		return currentShoppingCart;
	}

	public void clearCart(String userId) {

		if (shoppingCartRepository.findProductsInCartByUserId(userId).isPresent()) {
			shoppingCartRepository.deleteProductsInCartByUserId(userId);
			System.out.println("Deleteing all products for user: " + userId + " since checkout was successful");
		}
	}
}
