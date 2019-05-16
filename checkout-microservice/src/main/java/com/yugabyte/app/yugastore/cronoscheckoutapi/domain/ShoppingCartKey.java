package com.yugabyte.app.yugastore.cronoscheckoutapi.domain;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Embeddable;

@Embeddable
public class ShoppingCartKey implements Serializable {

	/**
	* 
	*/
	private static final long serialVersionUID = 343234890377423559L;

	@Column(name = "user_id")
	private String id;

	@Column(name = "asin")
	private String asin;
	
	public ShoppingCartKey() {
		
	}
	
	public ShoppingCartKey(String id, String asin) {
		this.id = id;
		this.asin = asin;
	}

	public String getAsin() {
		return asin;
	}

	public void setAsin(String asin) {
		this.asin = asin;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}


	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((id == null) ? 0 : asin.hashCode());
		result = prime * result + ((asin == null) ? 0 : id.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		ShoppingCartKey other = (ShoppingCartKey) obj;
		if (id == null) {
			if (other.id != null)
				return false;
			else {
				if (!id.equals(other.id)) {
					return false;
				}
			}
		}
		return true;
	}
}
