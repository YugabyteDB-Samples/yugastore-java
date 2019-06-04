package com.yugabyte.app.yugastore.service.impl;

import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;
import org.springframework.stereotype.Service;
import org.springframework.web.context.WebApplicationContext;

import com.yugabyte.app.yugastore.domain.CheckoutStatus;
import com.yugabyte.app.yugastore.rest.clients.CheckoutRestClient;
import com.yugabyte.app.yugastore.service.CheckoutServiceRest;

@Service
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class CheckoutServiceRestImpl implements CheckoutServiceRest {
	
	private final CheckoutRestClient checkoutRestClient;
	
	public CheckoutServiceRestImpl(CheckoutRestClient checkoutRestClient) {
		this.checkoutRestClient = checkoutRestClient;
	}

	@Override
	public CheckoutStatus checkout() {

		return checkoutRestClient.checkout();
	}

}
