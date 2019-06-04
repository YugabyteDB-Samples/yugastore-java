package com.yugabyte.app.yugastore.cronoscheckoutapi.repositories;

import java.util.Optional;

import org.springframework.data.cassandra.repository.CassandraRepository;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductInventory;

public interface ProductInventoryRepository extends CassandraRepository<ProductInventory, String> {
	Optional<ProductInventory> findById(String id);
}
