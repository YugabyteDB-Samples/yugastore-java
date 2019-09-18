package com.yugabyte.app.yugastore.cart.config;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.yugabyte.YBClusterAwareDataSource;

@Configuration
public class YugabyteDataSourceConfig {
	
	@Value("${yugabyte.sql.datasource.url}")
	String jdbcUrl;

	@Bean
	public DataSource getDataSource() {
		return new YBClusterAwareDataSource(jdbcUrl);
	}
}
