package com.yugabyte.app.yugastore.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;
import org.springframework.stereotype.Service;
import org.springframework.web.context.WebApplicationContext;

import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.domain.ProductRanking;
import com.yugabyte.app.yugastore.rest.clients.ProductCatalogRestClient;
import com.yugabyte.app.yugastore.service.ProductCatalogServiceRest;

import feign.Client;
import feign.Contract;
import feign.Feign;
import feign.codec.Decoder;
import feign.codec.Encoder;

@Service
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ProductCatalogServiceRestImpl implements ProductCatalogServiceRest {

  private final ProductCatalogRestClient productCatalogRestClient;

//  @Autowired
//  public ProductCatalogServiceRestImpl(ProductCatalogRestClient productCatalogRestClient) {
//    this.productCatalogRestClient = productCatalogRestClient;
//  }
  
  @Autowired
  public ProductCatalogServiceRestImpl(Decoder decoder, Encoder encoder, Client client, 
			Contract contract) {
	  this.productCatalogRestClient = Feign.builder().client(client)
				.encoder(encoder)
				.decoder(decoder)
				.contract(contract)
				.target(ProductCatalogRestClient.class, 
						"http://products-microservice");
  }

  @Override
  public ProductMetadata getProductDetails(String asin) {
    ProductMetadata result = productCatalogRestClient.getProductDetails(asin);
    return result;
  }

  @Override
  public List<ProductMetadata> getProducts(int limit, int offset) {
    return productCatalogRestClient.getProducts(limit, offset);
  }

  @Override
  public List<ProductRanking> getProductsByCategory(String category, int limit, int offset) {
    return productCatalogRestClient.getProductsByCategory(category, limit, offset);
  }
}