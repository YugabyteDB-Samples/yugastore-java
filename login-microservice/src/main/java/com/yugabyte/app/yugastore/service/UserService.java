package com.yugabyte.app.yugastore.service;

import com.yugabyte.app.yugastore.model.User;

public interface UserService {
    void save(User user);

    User findByUsername(String username);
}
