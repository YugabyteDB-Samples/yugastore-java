package com.yugabyte.app.yugastore.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;
import org.springframework.stereotype.Service;
import org.springframework.web.context.WebApplicationContext;

import com.yugabyte.app.yugastore.domain.CheckoutStatus;
import com.yugabyte.app.yugastore.rest.clients.CheckoutRestClient;
import com.yugabyte.app.yugastore.rest.clients.ProductCatalogRestClient;
import com.yugabyte.app.yugastore.service.CheckoutServiceRest;

import feign.Client;
import feign.Contract;
import feign.Feign;
import feign.codec.Decoder;
import feign.codec.Encoder;

@Service
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class CheckoutServiceRestImpl implements CheckoutServiceRest {
	
	private final CheckoutRestClient checkoutRestClient;
	
//	public CheckoutServiceRestImpl(CheckoutRestClient checkoutRestClient) {
//		this.checkoutRestClient = checkoutRestClient;
//	}
	
	  @Autowired
	  public CheckoutServiceRestImpl(Decoder decoder, Encoder encoder, Client client, 
				Contract contract) {
		  this.checkoutRestClient = Feign.builder().client(client)
					.encoder(encoder)
					.decoder(decoder)
					.contract(contract)
					.target(CheckoutRestClient.class, 
							"http://checkout-microservice");
	  }

	@Override
	public CheckoutStatus checkout() {

		return checkoutRestClient.checkout();
	}

}
