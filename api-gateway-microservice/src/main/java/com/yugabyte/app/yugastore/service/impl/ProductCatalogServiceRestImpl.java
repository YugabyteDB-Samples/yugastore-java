package com.yugabyte.app.yugastore.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;
import org.springframework.stereotype.Service;
import org.springframework.web.context.WebApplicationContext;

import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.rest.clients.ProductCatalogRestClient;
import com.yugabyte.app.yugastore.service.ProductCatalogServiceRest;

@Service
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ProductCatalogServiceRestImpl implements ProductCatalogServiceRest {

  private final ProductCatalogRestClient productCatalogRestClient;

  @Autowired
  public ProductCatalogServiceRestImpl(ProductCatalogRestClient productCatalogRestClient) {
    this.productCatalogRestClient = productCatalogRestClient;
  }

  @Override
  public ProductMetadata getProductDetails(String asin) {
    ProductMetadata result = productCatalogRestClient.getProductDetails(asin);
    return result;
  }
}
