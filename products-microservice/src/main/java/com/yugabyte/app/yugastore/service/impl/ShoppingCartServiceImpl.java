package com.yugabyte.app.yugastore.service.impl;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;
import org.springframework.data.cassandra.core.CassandraOperations;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.WebApplicationContext;

import com.yugabyte.app.yugastore.domain.Order;
import com.yugabyte.app.yugastore.domain.ProductInventory;
import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.exception.NotEnoughProductsInStockException;
import com.yugabyte.app.yugastore.repo.OrderRepository;
import com.yugabyte.app.yugastore.repo.ProductInventoryRepository;
import com.yugabyte.app.yugastore.repo.ProductMetadataRepo;
import com.yugabyte.app.yugastore.service.ShoppingCartService;

/**
 * Shopping Cart is implemented with a Map, and as a session bean
 *
 */
@Service
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
@Transactional
public class ShoppingCartServiceImpl implements ShoppingCartService {

	private final ProductMetadataRepo productRepository;

	private final OrderRepository orderRepository;

	private final ProductInventoryRepository productInventoryRepository;

	ProductInventory productInventory;
	ProductMetadata productDetails;

	@Autowired
	private CassandraOperations cassandraTemplate;

//    private CqlOperations cqlTemplate;

//	private Map<ProductMetadata, Integer> products = new HashMap<>();
	private static Map<String, Integer> products = new HashMap<>();

	@Autowired
	public ShoppingCartServiceImpl(ProductInventoryRepository productInventoryRepository,
			OrderRepository orderRepository, ProductMetadataRepo productRepository) {
		this.productInventoryRepository = productInventoryRepository;
		this.orderRepository = orderRepository;
		this.productRepository = productRepository;
	}

	/**
	 * If product is in the map just increment quantity by 1. If product is not in
	 * the map with, add it with quantity 1
	 *
	 * @param product
	 */
	@Override
	public void addProduct(String asin) {
		if (products.containsKey(asin)) {
			products.replace(asin, products.get(asin) + 1);
			System.out.println("Adding product: " + asin);
		} else {
			products.put(asin, 1);
			System.out.println("Adding product: " + asin);
		}
	}

	/**
	 * If product is in the map with quantity > 1, just decrement quantity by 1. If
	 * product is in the map with quantity 1, remove it from map
	 *
	 * @param product
	 */
	@Override
	public void removeProduct(String asin) {
		System.out.println("*** In remove products ***");
		if (products.containsKey(asin)) {
			if (products.get(asin) > 1) {
				products.replace(asin, products.get(asin) - 1);
				System.out.println("Removing product: " + asin);
			} else if (products.get(asin) == 1) {
				products.remove(asin);
				System.out.println("Removing product since it was qty 1 : " + asin);
			}
		}
	}

	/**
	 * @return unmodifiable copy of the map
	 */
	@Override
	public Map<String, Integer> getProductsInCart() {
		return Collections.unmodifiableMap(products);
	}

	/**
	 * Checkout will rollback if there is not enough of some product in stock
	 *
	 * @throws NotEnoughProductsInStockException
	 */
	@Override
	public Order checkout() throws NotEnoughProductsInStockException {
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
				productDetails = productRepository.findById(entry.getKey()).orElse(null);
				if (productInventory.getQuantity() < entry.getValue())
					throw new NotEnoughProductsInStockException(productInventory, productDetails);

				updateCartpreparedStatement.append(" UPDATE product_inventory SET quantity = quantity - "
						+ entry.getValue() + " where asin = '" + entry.getKey() + "' ;");
				orderDetails.append(" Product: " + productDetails.getTitle() + ", Quantity: " + entry.getValue() + ";");
			}
			double orderTotal = getTotal();
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

		return currentOrder;
	}

	@Override
	public Double getTotal() {
		double price = 0.0;
		for (Map.Entry<String, Integer> entry : products.entrySet()) {

			productInventory = productInventoryRepository.findById(entry.getKey()).orElse(null);
			productDetails = productRepository.findById(entry.getKey()).orElse(null);
			price = price + productDetails.getPrice() * entry.getValue();
		}
		return price;
	}

	public Order createOrder(String orderDetails, double orderTotal) {
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
