package com.yugabyte.app.yugastore.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.repository.query.Param;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.domain.ProductRanking;
import com.yugabyte.app.yugastore.service.ProductRankingService;
import com.yugabyte.app.yugastore.service.ProductService;

@RestController
@RequestMapping(value = "/products-microservice")
public class ProductCatalogController {
  
  // This service is used to lookup metadata of products by their id.
  @Autowired
  ProductService productService;

  // This service is used to lookup the top products by sales rank in a category.
  @Autowired
  ProductRankingService productRankingService;
  
  @RequestMapping(method = RequestMethod.GET, value = "/product/{asin}", produces = "application/json")
  public ProductMetadata getProductDetails(@PathVariable String asin) {
    ProductMetadata productMetadata = productService.findById(asin).get();
    return productMetadata;
  }  

  @RequestMapping(method = RequestMethod.GET, value = "/products", produces = "application/json")
  public List<ProductMetadata> getProducts(@Param("limit") int limit, @Param("offset") int offset) {
    return productService.findAllProductsPageable(limit, offset);
  }  

  @RequestMapping(method = RequestMethod.GET, value = "/products/category/{category}", produces = "application/json")
  public List<ProductRanking> getProductsByCategory(@PathVariable String category,
                                                    @Param("limit") int limit,
                                                    @Param("offset") int offset) {
    return productRankingService.getProductsByCategory(category, limit, offset);
  }  
}
