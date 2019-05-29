package com.yugabyte.app.yugastore.repo;

import com.yugabyte.app.yugastore.model.Role;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RoleRepository extends JpaRepository<Role, Long>{
}
