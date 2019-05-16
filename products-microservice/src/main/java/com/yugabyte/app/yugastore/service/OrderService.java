package com.yugabyte.app.yugastore.service;

import java.util.List;

import java.util.Optional;
import java.util.UUID;

import com.yugabyte.app.yugastore.domain.Order;

public interface OrderService {
	
	Optional<Order> findOrderById(String id);
	
	List<Order> findAllOrdersPageable();

}
