package com.yugabyte.app.yugastore.cronoscheckoutapi.domain;

import java.io.Serializable;

public class ProductRankingKey implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -6646128061564873843L;

	private String asin;
	
	private String category;

	public String getAsin() {
		return asin;
	}

	public String getCategory() {
		return category;
	}

	public void setId(String asin) {
		this.asin = asin;
	}

	public void setCategory(String category) {
		this.category = category;
	}
	
	@Override
	  public int hashCode() {
	    final int prime = 31;
	    int result = 1;
	    result = prime * result + ((asin == null) ? 0 : asin.hashCode());
	    result = prime * result + ((asin == null) ? 0 : asin.hashCode());
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
	    ProductRankingKey other = (ProductRankingKey) obj;
	    if (asin == null) {
	      if (other.asin != null)
	        return false;
	      else {
	    	  if (!asin.equals(other.asin)) {
	    		  return false;
	    	  }
	      }
	    }
	    return true;
	  }

}
