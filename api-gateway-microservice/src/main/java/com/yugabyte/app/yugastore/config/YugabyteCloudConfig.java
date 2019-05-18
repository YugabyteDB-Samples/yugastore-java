package com.yugabyte.app.yugastore.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.cassandra.config.AbstractCassandraConfiguration;
import org.springframework.data.cassandra.config.CassandraCqlClusterFactoryBean;
import org.springframework.data.cassandra.config.SchemaAction;
import org.springframework.data.cassandra.core.CassandraTemplate;
import org.springframework.data.cassandra.repository.config.EnableCassandraRepositories;

import com.datastax.driver.core.AuthProvider;
import com.datastax.driver.core.HostDistance;
import com.datastax.driver.core.PlainTextAuthProvider;
import com.datastax.driver.core.PoolingOptions;
import com.datastax.driver.core.Session;

@Configuration
@EnableAutoConfiguration
@Profile(value = "cloud")
class CassandraCloudConfig {

	@Configuration
	@EnableCassandraRepositories(basePackages = { "com.yugabyte.app.yugastore.repo" })
	class CassandraConfig extends AbstractCassandraConfiguration {

		@Autowired
		YugabyteAppProperties properties;

		@Value("${cronos.yugabyte.hostname}")
		private String cassandraHost;

		@Value("${cronos.yugabyte.port:9042}")
		private int cassandraPort;
		
		@Value("${cronos.yugabyte.username:cassandra}")
		private String cassandraUsername;

		
		@Value("${cronos.yugabyte.password:cassandra}")
		private String cassandraPassword;


		@Override
		public String getKeyspaceName() {
			return properties.getKeyspace();
		}

		@Override
		public String getContactPoints() {
			return cassandraHost;

		}

		@Override
		public int getPort() {
			return cassandraPort;
		}
		
		@Override
		protected AuthProvider getAuthProvider() {
			return new PlainTextAuthProvider(cassandraUsername, cassandraPassword);
		}
//
//		@Bean
//		public CassandraCqlClusterFactoryBean cluster() {
//
//			CassandraCqlClusterFactoryBean cluster = new CassandraCqlClusterFactoryBean();
//			cluster.setContactPoints(cassandraHost);
//			cluster.setPoolingOptions(getPoolingOptions());
//
//			return cluster;
//		}
//		
		@Override
		public PoolingOptions getPoolingOptions() {
			
			PoolingOptions poolingOptions = new PoolingOptions()
		    .setMaxRequestsPerConnection(HostDistance.LOCAL, 32768)
		    .setMaxRequestsPerConnection(HostDistance.REMOTE, 2000);
			
			return poolingOptions;
		}

		@Override
		public SchemaAction getSchemaAction() {
			return SchemaAction.CREATE_IF_NOT_EXISTS;
		}

		@Bean
		public CassandraTemplate cassandraTemplate(Session session) {
			return new CassandraTemplate(session);
		}

	}
}
