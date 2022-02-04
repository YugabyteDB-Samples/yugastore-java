package com.yugabyte.app.yugastore.cronoscheckoutapi.rest.clients;

import java.util.List;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductMetadata;
import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.ProductRanking;

@FeignClient("products-microservice")

public interface ProductCatalogRestClient {

  @RequestMapping("/products-microservice/product/{asin}")
  ProductMetadata getProductDetails(@PathVariable("asin") String asin);

  @RequestMapping("/products-microservice/products")
  List<ProductMetadata> getProducts(@RequestParam("limit") int limit,
    @RequestParam("offset") int offset);

  @RequestMapping("/products-microservice/products/category/{category}")
  List<ProductRanking> getProductsByCategory(@PathVariable("category") String category,
    @RequestParam("limit") int limit,
    @RequestParam("offset") int offset);
}
