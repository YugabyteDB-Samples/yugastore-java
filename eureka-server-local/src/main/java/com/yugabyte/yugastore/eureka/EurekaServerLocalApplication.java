package io.pivotal.cronos.eureka;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@SpringBootApplication
@EnableEurekaServer
public class EurekaServerLocalApplication {

	public static void main(String[] args) {
		SpringApplication.run(EurekaServerLocalApplication.class, args);
	}

}
