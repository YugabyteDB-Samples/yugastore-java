package com.yugabyte.app.yugastore.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.stereotype.Component;

@RefreshScope
@Component
public class YugabyteAppProperties {

	@Value("${cronos.yugabyte.keyspace}")
	String keyspace;

	public String getKeyspace() {
		return keyspace;
	}

}
