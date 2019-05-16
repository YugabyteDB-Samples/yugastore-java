package com.yugabyte.app.yugastore.service;

import java.util.List;
import java.util.Optional;

import com.yugabyte.app.yugastore.domain.ProductRanking;

public interface ProductRankingService {

	Optional<ProductRanking> findProductRankingById(String asin);
	
	List<ProductRanking> getProductsByCategory(String category, int limit, int offset);
	
}
