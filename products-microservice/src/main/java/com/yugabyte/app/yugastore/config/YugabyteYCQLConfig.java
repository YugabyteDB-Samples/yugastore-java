package com.yugabyte.app.yugastore.config;

import com.datastax.oss.driver.api.core.CqlSession;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.cassandra.config.AbstractCassandraConfiguration;
import org.springframework.data.cassandra.config.SchemaAction;
import org.springframework.data.cassandra.core.CassandraTemplate;
import org.springframework.data.cassandra.repository.config.EnableCassandraRepositories;


@Configuration
@EnableAutoConfiguration
@Profile(value = "local")
class YugabyteYCQLConfig {

  @Configuration
  @EnableCassandraRepositories(basePackages = { "com.yugabyte.app.yugastore.repo" })
  class CassandraConfig extends AbstractCassandraConfiguration {

    @Value("${cronos.yugabyte.hostname:localhost}")
    private String cassandraHost;

    @Value("${cronos.yugabyte.port:9042}")
    private int cassandraPort;

    @Value("${cronos.yugabyte.keyspace:cronos}")
    private String keyspace;

    @Override
    public String getKeyspaceName() {
      return keyspace;
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
    public SchemaAction getSchemaAction() {
      return SchemaAction.CREATE_IF_NOT_EXISTS;
    }

    @Bean
    public CassandraTemplate cassandraTemplate(CqlSession session) {
      return new CassandraTemplate(session);
    }

  }
}
