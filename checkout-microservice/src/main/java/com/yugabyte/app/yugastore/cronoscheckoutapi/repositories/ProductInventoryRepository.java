package com.yugabyte.app.yugastore.cronoscheckoutapi.repositories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductInventory;

@Repository
public interface ProductInventoryRepository extends CrudRepository<ProductInventory, String> {

}
