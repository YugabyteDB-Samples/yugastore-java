package com.yugabyte.app.yugastore;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
//@EnableFeignClients
public class YugabyteClientApplication {

	public static void main(String[] args) {
		SpringApplication.run(YugabyteClientApplication.class, args);
	}
}
