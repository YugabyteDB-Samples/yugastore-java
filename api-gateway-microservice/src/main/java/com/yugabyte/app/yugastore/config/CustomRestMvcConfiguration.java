package com.yugabyte.app.yugastore.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.rest.core.config.RepositoryRestConfiguration;
import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurer;
import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurerAdapter;

import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.domain.ProductRanking;

@Configuration
public class CustomRestMvcConfiguration {

	@Bean
	  public RepositoryRestConfigurer repositoryRestConfigurer() {

	    return new RepositoryRestConfigurerAdapter() {

	      @Override
	      public void configureRepositoryRestConfiguration(RepositoryRestConfiguration config) {
	        config.setBasePath("/api/v1");
	        config.exposeIdsFor(ProductMetadata.class, ProductRanking.class);
	      }
	    };
	  }

}
