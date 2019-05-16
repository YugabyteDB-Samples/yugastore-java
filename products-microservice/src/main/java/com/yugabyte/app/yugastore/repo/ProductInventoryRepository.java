package com.yugabyte.app.yugastore.repo;

import java.util.Optional;

import org.springframework.data.cassandra.repository.CassandraRepository;

import com.yugabyte.app.yugastore.domain.ProductInventory;

public interface ProductInventoryRepository extends CassandraRepository<ProductInventory, String> {
	Optional<ProductInventory> findById(String id);
}
