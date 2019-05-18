package com.yugabyte.app.yugastore.repo;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.springframework.data.cassandra.repository.CassandraRepository;
import org.springframework.data.cassandra.repository.Query;
import org.springframework.data.rest.core.annotation.RestResource;

import com.yugabyte.app.yugastore.domain.Order;

public interface OrderRepository  extends CassandraRepository<Order, String>{

	Optional<Order> findOrderById(String id);
	
	@Query("select * from cronos.orders")
	@RestResource(path = "orders")
	List<Order> findAllOrdersPageable();
	
	@Query("select * from cronos.orders limit 1")
	List<Order> findAll();
	
}
