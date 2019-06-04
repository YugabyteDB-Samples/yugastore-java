package com.yugabyte.app.yugastore.cronoscheckoutapi.repositories;

import org.springframework.data.repository.CrudRepository;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductInventory;

public interface ProductInventoryRepo extends CrudRepository<ProductInventory, String> {

}
