package com.yugabyte.app.yugastore.cronoscheckoutapi.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.repository.query.Param;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.service.ProductService;

@RestController
@RequestMapping(value = "/products-microservice")
public class ProductCatalogController {
  
  @Autowired
  ProductService productService;
  
  @RequestMapping(method = RequestMethod.GET, value = "/product/{asin}", produces = "application/json")
  public ProductMetadata getProductDetails(@PathVariable String asin) {
    ProductMetadata productMetadata = productService.findById(asin).get();
    return productMetadata;
  }  


  @RequestMapping(method = RequestMethod.GET, value = "/products", produces = "application/json")
  public List<ProductMetadata> getProducts(@Param("limit") int limit, @Param("offset") int offset) {
    return productService.findAllProductsPageable(limit, offset);
  }  
}
