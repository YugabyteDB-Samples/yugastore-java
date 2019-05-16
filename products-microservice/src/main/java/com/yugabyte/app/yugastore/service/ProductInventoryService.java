package com.yugabyte.app.yugastore.service;

import java.util.Optional;

import com.yugabyte.app.yugastore.domain.*;

public interface ProductInventoryService {

    Optional<ProductInventory> findById(String id);

}
