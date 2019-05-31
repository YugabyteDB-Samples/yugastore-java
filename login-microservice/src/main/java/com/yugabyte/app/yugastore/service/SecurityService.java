package com.yugabyte.app.yugastore.service;

public interface SecurityService {
    String findLoggedInUsername();

    void autoLogin(String username, String password);
}
