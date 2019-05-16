package com.yugabyte.app.yugastore.service;

import java.util.Map;

import com.yugabyte.app.yugastore.domain.Order;
import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.exception.NotEnoughProductsInStockException;

public interface ShoppingCartService {

    void addProduct(String product);

    void removeProduct(String product);

    Map<String, Integer> getProductsInCart();

    Order checkout() throws NotEnoughProductsInStockException;

    Double getTotal();
}
