package com.yugabyte.app.yugastore.cronoscheckoutapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class CheckoutService {

	public static void main(String[] args) {
		SpringApplication.run(CheckoutService.class, args);
	}

}
