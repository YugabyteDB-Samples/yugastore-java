package com.yugabyte.app.yugastore;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
public class YugastoreApiGateway {

	public static void main(String[] args) {
		SpringApplication.run(YugastoreApiGateway.class, args);
	}
}
