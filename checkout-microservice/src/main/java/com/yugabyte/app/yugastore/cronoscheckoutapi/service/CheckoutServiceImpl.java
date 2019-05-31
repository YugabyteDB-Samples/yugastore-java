package com.yugabyte.app.yugastore.cronoscheckoutapi.service;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.UUID;

import org.springframework.stereotype.Service;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.Order;
import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductInventory;
import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductMetadata;
import com.yugabyte.app.yugastore.cronoscheckoutapi.exception.NotEnoughProductsInStockException;
import com.yugabyte.app.yugastore.cronoscheckoutapi.repositories.ProductInventoryRepo;
import com.yugabyte.app.yugastore.cronoscheckoutapi.rest.clients.ShoppingCartRestClient;


@Service
public class CheckoutServiceImpl {
	
	private final ShoppingCartRestClient shoppingCartRestClient;
	private final ProductInventoryRepo productInventoryRepository;
	ProductInventory productInventory;
	ProductMetadata productDetails;
	
	public CheckoutServiceImpl(ShoppingCartRestClient shoppingCartRestClient, 
			ProductInventoryRepo productInventoryRepository) {
		this.shoppingCartRestClient = shoppingCartRestClient;
		this.productInventoryRepository = productInventoryRepository;
	}
	
	public Order checkout(String userId) throws NotEnoughProductsInStockException {
		
		Map<String, Integer> products = shoppingCartRestClient.getProductsInCart(userId);
		System.out.println("*** In Checkout products ***");
		StringBuilder updateCartpreparedStatement = new StringBuilder();
		updateCartpreparedStatement.append("BEGIN TRANSACTION");
		Order currentOrder = null;
		StringBuilder orderDetails = new StringBuilder();
		orderDetails.append("Customer bought these Items: ");
		if (products.size() != 0) {
			for (Map.Entry<String, Integer> entry : products.entrySet()) {
				// Refresh quantity for every product before checking
				System.out.println("*** Checking out product *** " + entry.getKey());
				productInventory = productInventoryRepository.findById(entry.getKey()).orElse(null);
//				productDetails = productRepository.findById(entry.getKey()).orElse(null);
				if (productInventory.getQuantity() < entry.getValue())
					throw new NotEnoughProductsInStockException(productInventory, productDetails);

				updateCartpreparedStatement.append(" UPDATE product_inventory SET quantity = quantity - "
						+ entry.getValue() + " where asin = '" + entry.getKey() + "' ;");
				orderDetails.append(" Product: " + "title" + ", Quantity: " + entry.getValue() + ";");
			}
			double orderTotal = getTotal(products);
			orderDetails.append(" Order Total is : " + orderTotal);
			currentOrder = createOrder(orderDetails.toString(), orderTotal);
			updateCartpreparedStatement
					.append(" INSERT INTO orders (order_id, user_id, order_details, order_time, order_total) VALUES ("
							+ "'" + currentOrder.getId() + "', " + "'1'" + ", '" + currentOrder.getOrder_details()
							+ "', '" + currentOrder.getOrder_time() + "'," + currentOrder.getOrder_total() + ");");
			updateCartpreparedStatement.append(" END TRANSACTION;");
			System.out.println("Statemet is " + updateCartpreparedStatement.toString());
			cassandraTemplate.getCqlOperations().execute(updateCartpreparedStatement.toString());
		}
		products.clear();
		shoppingCartRestClient.clearCart(userId);
		System.out.println("*** Checkout complete, cart cleared ***");
		return currentOrder;

	}
	
	private Double getTotal(Map<String, Integer> products) {
		double price = 0.0;
		for (Map.Entry<String, Integer> entry : products.entrySet()) {

			productInventory = productInventoryRepository.findById(entry.getKey()).orElse(null);
//			productDetails = productRepository.findById(entry.getKey()).orElse(null);
//			price = price + productDetails.getPrice() * entry.getValue();
			price = price + 100;
		}
		return price;
	}

	private Order createOrder(String orderDetails, double orderTotal) {
		Order order = new Order();
		LocalDateTime currentTime = LocalDateTime.now();
		order.setId(UUID.randomUUID().toString());
		order.setUser_id(1);
		order.setOrder_details(orderDetails);
		order.setOrder_time(currentTime.toString());
		order.setOrder_total(orderTotal);
		return order;
	}
	
}
