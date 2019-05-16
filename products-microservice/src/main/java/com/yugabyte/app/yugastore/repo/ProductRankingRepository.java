package com.yugabyte.app.yugastore.repo;

import java.util.List;
import java.util.Optional;
import org.springframework.data.cassandra.repository.CassandraRepository;
import org.springframework.data.cassandra.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RestResource;
import com.yugabyte.app.yugastore.domain.ProductRanking;

public interface ProductRankingRepository extends CassandraRepository<ProductRanking, String> {
	
	@Query("select * from cronos.product_rankings where asin=?0")
	@RestResource(path = "product", rel = "product")
	Optional<ProductRanking> findProductRankingById(String asin);
	
	@Query("SELECT * FROM cronos.product_rankings where category =?0 limit ?1 offset ?2")
	@RestResource(path = "category", rel = "category")
	public List<ProductRanking> getProductsByCategory(@Param("name") String category, @Param("limit") int limit, @Param("offset") int offset);

}
