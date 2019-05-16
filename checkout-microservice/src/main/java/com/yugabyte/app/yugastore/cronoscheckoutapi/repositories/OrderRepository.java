package com.yugabyte.app.yugastore.cronoscheckoutapi.repositories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.yugabyte.app.yugastore.cronoscheckoutapi.domain.Order;

@Repository
public interface OrderRepository extends CrudRepository<Order, String> {

}
