package com.yugabyte.app.yugastore.service;

import com.yugabyte.app.yugastore.domain.ProductMetadata;

public interface ProductCatalogServiceRest {
  
  ProductMetadata getProductDetails(String asin);
}
