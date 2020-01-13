//package com.yugabyte.app.yugastore.rest.clients;
//
//import java.util.Map;
//
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.cloud.client.loadbalancer.LoadBalanced;
//import org.springframework.cloud.netflix.ribbon.RibbonClient;
//import org.springframework.context.annotation.Bean;
//import org.springframework.stereotype.Component;
//import org.springframework.web.client.RestTemplate;
//
//import com.netflix.client.config.IClientConfig;
//import com.netflix.loadbalancer.AvailabilityFilteringRule;
//import com.netflix.loadbalancer.IPing;
//import com.netflix.loadbalancer.IRule;
//import com.netflix.loadbalancer.PingUrl;
//
//@RibbonClient(name = "cart-microservice", configuration = ShoppingCartServiceConfiguration.class)
//@Component
//public class ShoppingCartK8sRestClient {
//	
//
//    @Autowired
//    RestTemplate restTemplate;
//	
//	@LoadBalanced
//    @Bean
//    RestTemplate restTemplate() {
//        return new RestTemplate();
//    }
//	
//	public String addProductToCart(String userId, String asin) {
//		
//		String result = this.restTemplate.getForObject("http://cart-microservice/shoppingCart/addProduct", String.class);
//		return result;
//		
//	}
//	
//	@SuppressWarnings("unchecked")
//	public Map<String, Integer> getProductsInCart(String userId) {
//		
//		Map<String, Integer> productsInCart = this.restTemplate.getForObject("http://cart-microservice/shoppingCart/productsInCart", Map.class);
//		return productsInCart;
//		
//	}
//	
//	public String removeProductFromCart(String userId, String asin) {
//		
//		String result = this.restTemplate.getForObject("http://cart-microservice/shoppingCart/removeProduct", String.class);
//		return result;
//		
//	}
//	
//	public String clearCart(String userId) {
//		
//		String result = this.restTemplate.getForObject("http://cart-microservice/shoppingCart/clearCart", String.class);
//		return result;
//	}
//
//}
//
//class ShoppingCartServiceConfiguration {
//	
//    @Autowired
//    IClientConfig ribbonClientConfig;
//    
//    @Bean
//    public IPing ribbonPing(IClientConfig config) {
//        return new PingUrl();
//    }
//    
//    @Bean
//    public IRule ribbonRule(IClientConfig config) {
//        return new AvailabilityFilteringRule();
//    }
//}