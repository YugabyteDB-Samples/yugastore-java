package com.yugabyte.app.yugastore.domain;

public class ProductInventory {

   private String id;
   
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

