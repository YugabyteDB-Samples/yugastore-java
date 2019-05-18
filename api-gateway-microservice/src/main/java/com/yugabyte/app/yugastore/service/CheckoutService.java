package com.yugabyte.app.yugastore.service;

import com.yugabyte.app.yugastore.domain.Order;
import com.yugabyte.app.yugastore.exception.NotEnoughProductsInStockException;

public interface CheckoutService {
	
    Order checkout(String userId) throws NotEnoughProductsInStockException;

}
