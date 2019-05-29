package com.yugabyte.app.yugastore.repo;

import com.yugabyte.app.yugastore.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
    User findByUsername(String username);
}
