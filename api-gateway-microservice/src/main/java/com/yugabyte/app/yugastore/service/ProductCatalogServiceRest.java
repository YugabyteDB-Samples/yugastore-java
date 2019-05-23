package com.yugabyte.app.yugastore.service;

import java.util.List;

import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.domain.ProductRanking;

public interface ProductCatalogServiceRest {
  
  ProductMetadata getProductDetails(String asin);

  List<ProductMetadata> getProducts(int limit, int offset);

  List<ProductRanking> getProductsByCategory(String category, int limit, int offset);
}
