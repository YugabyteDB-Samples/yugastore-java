package com.yugabyte.app.yugastore.exception;

import com.yugabyte.app.yugastore.domain.ProductInventory;
import com.yugabyte.app.yugastore.domain.ProductMetadata;

public class NotEnoughProductsInStockException extends Exception {

    /**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private static final String DEFAULT_MESSAGE = "Not enough products in stock";

    public NotEnoughProductsInStockException() {
        super(DEFAULT_MESSAGE);
    }

    public NotEnoughProductsInStockException(ProductInventory productInventory, ProductMetadata product) {
        super(String.format("Not enough %s products in stock. Only %d left", product.getTitle(), productInventory.getQuantity()));
    }

}
