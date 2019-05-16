package com.yugabyte.app.yugastore.repo;

import java.util.List;
import java.util.Optional;

import org.springframework.data.cassandra.repository.CassandraRepository;
import org.springframework.data.cassandra.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import org.springframework.data.rest.core.annotation.RestResource;

import com.yugabyte.app.yugastore.domain.ProductMetadata;

@RepositoryRestResource(path = "productmetadata")
public interface ProductMetadataRepo extends CassandraRepository<ProductMetadata, String> {
	
	@Query("SELECT * FROM cronos.products limit ?0 offset ?1")
	@RestResource(path = "products", rel = "products")
	public List<ProductMetadata> getProducts(@Param("limit") int limit, @Param("offset") int offset);

	Optional<ProductMetadata> findById(String id);
}
