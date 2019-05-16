package com.yugabyte.app.yugastore.service.impl;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.yugabyte.app.yugastore.domain.ProductInventory;
import com.yugabyte.app.yugastore.repo.ProductInventoryRepository;
import com.yugabyte.app.yugastore.service.ProductInventoryService;

@Service
public class ProductInventoryServiceImpl implements ProductInventoryService {

    private final ProductInventoryRepository productInventoryRepository;

    @Autowired
    public ProductInventoryServiceImpl(ProductInventoryRepository productInventoryRepository) {
        this.productInventoryRepository = productInventoryRepository;
    }

    @Override
    public Optional<ProductInventory> findById(String id) {
        return productInventoryRepository.findById(id);
    }
}
