package com.yugabyte.app.yugastore.cronoscheckoutapi.domain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity(name = "product_inventory")
@Table(name = "product_inventory")
public class ProductInventory {

   @Id
   @Column(name = "asin")
   private String id;
   
   @Column(name = "quantity")
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

