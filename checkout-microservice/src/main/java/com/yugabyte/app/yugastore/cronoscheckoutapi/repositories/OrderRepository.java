package com.yugabyte.app.yugastore.cronoscheckoutapi.repositories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.data.rest.webmvc.RepositoryRestController;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.Order;

@RepositoryRestController
public interface OrderRepository extends CrudRepository<Order, String> {

}
