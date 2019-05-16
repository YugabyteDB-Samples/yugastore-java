package com.yugabyte.app.yugastore.domain;

import org.springframework.data.cassandra.core.mapping.Column;
import org.springframework.data.cassandra.core.mapping.PrimaryKey;
import org.springframework.data.cassandra.core.mapping.Table;

@Table(value = "product_rankings")
public class ProductRanking{

	@PrimaryKey
	private ProductRankingKey asin;

	@Column(value = "sales_rank")
	private int salesRank;
	
	private String title;
	
	private Double price;
	
	@Column(value = "imurl")
	private String imUrl;
	
	private Integer num_reviews;
	
	private Double num_stars;
	
	private Double avg_stars;

	public int getSalesRank() {
		return salesRank;
	}

	public void setSalesRank(int salesRank) {
		this.salesRank = salesRank;
	}

	public ProductRankingKey getId() {
		return asin;
	}

	public String getTitle() {
		return title;
	}

	public Double getPrice() {
		return price;
	}

	public String getImUrl() {
		return imUrl;
	}

	public Integer getNum_reviews() {
		return num_reviews;
	}

	public Double getNum_stars() {
		return num_stars;
	}

	public Double getAvg_stars() {
		return avg_stars;
	}

	public void setId(ProductRankingKey id) {
		this.asin = id;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public void setPrice(Double price) {
		this.price = price;
	}

	public void setImUrl(String imUrl) {
		this.imUrl = imUrl;
	}

	public void setNum_reviews(Integer num_reviews) {
		this.num_reviews = num_reviews;
	}

	public void setNum_stars(Double num_stars) {
		this.num_stars = num_stars;
	}

	public void setAvg_stars(Double avg_stars) {
		this.avg_stars = avg_stars;
	}

}
