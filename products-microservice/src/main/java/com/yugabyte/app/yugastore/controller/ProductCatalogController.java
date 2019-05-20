package com.yugabyte.app.yugastore.cronoscheckoutapi.controller;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
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
    System.out.println("[KAR: DEBUG] " + "Got request: getProductDetails(" + asin + ")");
    ProductMetadata productMetadata = productService.findById(asin).get();
    return productMetadata;
  }  
}
