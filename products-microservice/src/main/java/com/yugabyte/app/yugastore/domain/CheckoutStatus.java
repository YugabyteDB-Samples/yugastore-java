package com.yugabyte.app.yugastore.domain;

public class CheckoutStatus {
	
	public static final String SUCCESS = "SUCCESS";
	
	public static final String FAILURE = "FAILURE";
	
	String status;

	String orderNumber;
	
	String orderDetails;
	
	public String getOrderDetails() {
		return orderDetails;
	}

	public void setOrderDetails(String orderDetails) {
		this.orderDetails = orderDetails;
	}

	public String getStatus() {
		return status;
	}

	public String getOrderNumber() {
		return orderNumber;
	}

	public void setStatus(String status) {
		this.status = status;
	}

	public void setOrderNumber(String orderNumber) {
		this.orderNumber = orderNumber;
	}

}
