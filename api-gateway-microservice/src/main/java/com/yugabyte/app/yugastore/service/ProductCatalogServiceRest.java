package com.yugabyte.app.yugastore.service;

import java.util.List;

import com.yugabyte.app.yugastore.domain.ProductMetadata;

public interface ProductCatalogServiceRest {
  
  ProductMetadata getProductDetails(String asin);

  List<ProductMetadata> getProducts(int limit, int offset);
}
