package com.yugabyte.app.yugastore.domain;

import java.util.List;
import java.util.Set;
import org.springframework.data.cassandra.core.mapping.CassandraType;
import org.springframework.data.cassandra.core.mapping.Column;
import org.springframework.data.cassandra.core.mapping.PrimaryKey;
import org.springframework.data.cassandra.core.mapping.Table;
import org.springframework.hateoas.ResourceSupport;

import com.datastax.driver.core.DataType.Name;


@Table(value = "products")
public class ProductMetadata{

	
    @PrimaryKey(value="asin")
    private String id;
  //String asin;
    
	String brand;
	
	Set<String> categories;
	
	@Column(value = "imurl")
	String imUrl;
	
	Double price;
	
	String title;
	
	String description;
	
	@CassandraType(type = Name.LIST)
	List<String> also_bought;
	
	@CassandraType(type = Name.LIST)
	List<String> also_viewed;
	
	@CassandraType(type = Name.LIST)
	List<String> bought_together;
	
	@CassandraType(type = Name.LIST)
	List<String> buy_after_viewing;
	
	Integer num_reviews;
	
	Double num_stars;
	
	Double avg_stars;

	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public String getBrand() {
		return brand;
	}
	public void setBrand(String brand) {
		this.brand = brand;
	}
	public Set<String> getCategories() {
		return categories;
	}
	public void setCategories(Set<String> categories) {
		this.categories = categories;
	}
	public String getImUrl() {
		return imUrl;
	}
	public void setImUrl(String imUrl) {
		this.imUrl = imUrl;
	}
	public Double getPrice() {
		return price;
	}
	public void setPrice(Double price) {
		this.price = price;
	}
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	public List<String> getAlso_bought() {
		return also_bought;
	}
	public void setAlso_bought(List<String> also_bought) {
		this.also_bought = also_bought;
	}
	public List<String> getAlso_viewed() {
		return also_viewed;
	}
	public void setAlso_viewed(List<String> also_viewed) {
		this.also_viewed = also_viewed;
	}
	public List<String> getBought_together() {
		return bought_together;
	}
	public void setBought_together(List<String> bought_together) {
		this.bought_together = bought_together;
	}
	public Integer getNum_reviews() {
		return num_reviews;
	}
	public void setNum_reviews(Integer num_reviews) {
		this.num_reviews = num_reviews;
	}
	public Double getNum_stars() {
		return num_stars;
	}
	public void setNum_stars(Double num_stars) {
		this.num_stars = num_stars;
	}
	public Double getAvg_stars() {
		return avg_stars;
	}
	public void setAvg_stars(Double avg_stars) {
		this.avg_stars = avg_stars;
	}
	public List<String> getBuy_after_viewing() {
		return buy_after_viewing;
	}
	public void setBuy_after_viewing(List<String> buy_after_viewing) {
		this.buy_after_viewing = buy_after_viewing;
	}
	
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        ProductMetadata product = (ProductMetadata) o;

        return id.equals(product.id);
    }

    @Override
    public int hashCode() {
        return id.hashCode();
    }

}
