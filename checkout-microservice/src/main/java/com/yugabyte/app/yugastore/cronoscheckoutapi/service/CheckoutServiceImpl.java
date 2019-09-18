package com.yugabyte.app.yugastore.cronoscheckoutapi.service;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;
import org.springframework.data.cassandra.core.CassandraOperations;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.WebApplicationContext;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.Order;
import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductInventory;
import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductMetadata;
import com.yugabyte.app.yugastore.cronoscheckoutapi.exception.NotEnoughProductsInStockException;
import com.yugabyte.app.yugastore.cronoscheckoutapi.repositories.ProductInventoryRepository;
import com.yugabyte.app.yugastore.cronoscheckoutapi.rest.clients.ProductCatalogRestClient;
import com.yugabyte.app.yugastore.cronoscheckoutapi.rest.clients.ShoppingCartRestClient;

import feign.Client;
import feign.Contract;
import feign.Feign;
import feign.codec.Decoder;
import feign.codec.Encoder;


@Service
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
@Transactional
public class CheckoutServiceImpl {

	private final ShoppingCartRestClient shoppingCartRestClient;
	private final ProductCatalogRestClient productCatalogRestClient;
	private final ProductInventoryRepository productInventoryRepository;

	ProductInventory productInventory;
	ProductMetadata productDetails;
	
	  @Autowired
	  public CheckoutServiceImpl (ProductInventoryRepository productInventoryRepository, 
			  Decoder decoder, Encoder encoder, Client client, 
				Contract contract) {
		  this.productInventoryRepository = productInventoryRepository;
		  this.shoppingCartRestClient = Feign.builder().client(client)
					.encoder(encoder)
					.decoder(decoder)
					.contract(contract)
					.target(ShoppingCartRestClient.class, 
							"http://cart-microservice");
		  this.productCatalogRestClient = Feign.builder().client(client)
					.encoder(encoder)
					.decoder(decoder)
					.contract(contract)
					.target(ProductCatalogRestClient.class, 
							"http://products-microservice");
	  }
	  
//	@Autowired
//	public CheckoutServiceImpl(ProductInventoryRepository productInventoryRepository, 
//			ShoppingCartRestClient shoppingCartRestClient, ProductCatalogRestClient productCatalogRestClient) {
//		this.productInventoryRepository = productInventoryRepository;
//		this.shoppingCartRestClient = shoppingCartRestClient;
//		this.productCatalogRestClient = productCatalogRestClient;	
//	}

	@Autowired
	private CassandraOperations cassandraTemplate;

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
				productDetails = productCatalogRestClient.getProductDetails(entry.getKey());
				
				if (productInventory.getQuantity() < entry.getValue())
					throw new NotEnoughProductsInStockException(productDetails.getTitle(), productInventory.getQuantity());

				updateCartpreparedStatement.append(" UPDATE product_inventory SET quantity = quantity - "
						+ entry.getValue() + " where asin = '" + entry.getKey() + "' ;");
				orderDetails.append(" Product: " + productDetails.getTitle() + ", Quantity: " + entry.getValue() + ";");
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
			productDetails = productCatalogRestClient.getProductDetails(entry.getKey());
			price = price + productDetails.getPrice() * entry.getValue();
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
