package io.pivotal.cronos.ui.model;

import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class ProductMetadata {
	
	String brand;
	List<String> categories;
	String imUrl;
	Double price;
	Map<String, Integer> salesRank;
	String title;
	Map<String, List<String>> related;
	Map<String, Map<String, String>> _links;
	Integer num_reviews;
	Double num_stars;
	Double avg_stars;
	
	public String getBrand() {
		return brand;
	}
	public void setBrand(String brand) {
		this.brand = brand;
	}
	public List<String> getCategories() {
		return categories;
	}
	public void setCategories(List<String> categories) {
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
	public Map<String, Integer> getSalesRank() {
		return salesRank;
	}
	public void setSalesRank(Map<String, Integer> salesRank) {
		this.salesRank = salesRank;
	}
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public Map<String, List<String>> getRelated() {
		return related;
	}
	public void setRelated(Map<String, List<String>> related) {
		this.related = related;
	}
	public Map<String, Map<String, String>> get_links() {
		return _links;
	}
	public void set_links(Map<String, Map<String, String>> _links) {
		this._links = _links;
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

}
