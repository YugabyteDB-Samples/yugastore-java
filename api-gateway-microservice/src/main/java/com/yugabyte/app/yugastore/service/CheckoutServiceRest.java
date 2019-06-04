package com.yugabyte.app.yugastore.service;

import com.yugabyte.app.yugastore.domain.CheckoutStatus;

public interface CheckoutServiceRest {
	
	CheckoutStatus checkout();

}
