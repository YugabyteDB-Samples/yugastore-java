package com.yugabyte.app.yugastore.cronoscheckoutapi.domain;

import org.springframework.data.cassandra.core.mapping.Column;
import org.springframework.data.cassandra.core.mapping.PrimaryKey;
import org.springframework.data.cassandra.core.mapping.Table;

@Table(value = "product_inventory")
public class ProductInventory {

   @PrimaryKey(value="asin")
   private String id;
   
   @Column(value = "quantity")
   private Integer quantity;

	public String getId() {
		return id;
	}

	public Integer getQuantity() {
		return quantity;
	}

	public void setId(String id) {
		this.id = id;
	}

	public void setQuantity(Integer quantity) {
		this.quantity = quantity;
	}
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        ProductInventory product = (ProductInventory) o;

        return id.equals(product.id);
    }

    @Override
    public int hashCode() {
        return id.hashCode();
    }

}

