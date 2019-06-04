package com.yugabyte.app.yugastore.cronoscheckoutapi.exception;

public class NotEnoughProductsInStockException extends Exception {

    private static final String DEFAULT_MESSAGE = "Not enough products in stock";

    public NotEnoughProductsInStockException() {
        super(DEFAULT_MESSAGE);
    }

    public NotEnoughProductsInStockException(String title, Integer quantity) {
        super(String.format("Not enough %s products in stock. Only %d left", title, quantity));
    }

}
