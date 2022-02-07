package com.yugabyte.app.yugastore.rest.clients;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.yugabyte.app.yugastore.domain.CheckoutStatus;

@FeignClient("checkout-microservice")
public interface CheckoutRestClient {

  @RequestMapping(value = "/checkout-microservice/shoppingCart/checkout", method =
    RequestMethod.POST)
  CheckoutStatus checkout();

}
