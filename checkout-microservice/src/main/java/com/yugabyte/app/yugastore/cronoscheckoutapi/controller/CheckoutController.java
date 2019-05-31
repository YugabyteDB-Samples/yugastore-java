package com.yugabyte.app.yugastore.cronoscheckoutapi.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.yugabyte.app.yugastore.cronoscheckoutapi.service.CheckoutServiceImpl;

@RestController
@RequestMapping(value = "/checkout-microservice")
public class CheckoutController {
	
	@Autowired
	CheckoutServiceImpl orderCheckoutService;
	
}
