package com.yugabyte.app.yugastore.util;


import org.springframework.data.domain.Page;

import com.yugabyte.app.yugastore.domain.ProductMetadata;

public class Pager {

    private final Page<ProductMetadata> products;

    public Pager(Page<ProductMetadata> products) {
        this.products = products;
    }

    public int getPageIndex() {
        return products.getNumber() + 1;
    }

    public int getPageSize() {
        return products.getSize();
    }

    public boolean hasNext() {
        return products.hasNext();
    }

    public boolean hasPrevious() {
        return products.hasPrevious();
    }

    public int getTotalPages() {
        return products.getTotalPages();
    }

    public long getTotalElements() {
        return products.getTotalElements();
    }

    public boolean indexOutOfBounds() {
        return this.getPageIndex() < 0 || this.getPageIndex() > this.getTotalElements();
    }

}
