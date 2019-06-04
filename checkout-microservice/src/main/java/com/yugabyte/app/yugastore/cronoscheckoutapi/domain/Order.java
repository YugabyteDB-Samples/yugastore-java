package com.yugabyte.app.yugastore.cronoscheckoutapi.domain;

import org.springframework.data.cassandra.core.mapping.Column;
import org.springframework.data.cassandra.core.mapping.PrimaryKey;
import org.springframework.data.cassandra.core.mapping.Table;

@Table(value="orders")
public class Order {
	
    @PrimaryKey(value="order_id")
    private String id;
    
    @Column(value = "user_id")
    private Integer user_id;
    
    @Column(value = "order_details")
    private String order_details;
    
    @Column(value = "order_time")
    private String order_time;
    
    @Column(value = "order_total")
    private Double order_total;

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public Integer getUser_id() {
		return user_id;
	}

	public void setUser_id(Integer user_id) {
		this.user_id = user_id;
	}

	public String getOrder_details() {
		return order_details;
	}

	public void setOrder_details(String order_details) {
		this.order_details = order_details;
	}

	public String getOrder_time() {
		return order_time;
	}

	public void setOrder_time(String order_time) {
		this.order_time = order_time;
	}
	
    public Double getOrder_total() {
		return order_total;
	}

	public void setOrder_total(Double order_total) {
		this.order_total = order_total;
	}

	@Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Order order = (Order) o;

        return id.equals(order.id);
    }

    @Override
    public int hashCode() {
        return id.hashCode();
    }


}
