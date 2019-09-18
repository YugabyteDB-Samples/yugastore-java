package com.yugabyte.app.yugastore.cronoscheckoutapi.config;

import org.springframework.cloud.openfeign.FeignClientsConfiguration;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Import(FeignClientsConfiguration.class)
@Configuration
public class FeignConfiguration {

}
