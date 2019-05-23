package com.yugabyte.yugastore.ui.rest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.*;

@Component
public class DashboardRestConsumer {

	@Autowired
	RestTemplate restTemplate;
	
	@Value("${cronos.yugabyte.api:http://localhost:8081/api/v1}")
	String restUrlBase;

	public String getHomePageProducts(int limit, int offset) {

		String restURL = restUrlBase + "products?limit=" + limit + "&offset=" + offset;
		ResponseEntity<String> rateResponse =
		        restTemplate.exchange(restURL,
		                    HttpMethod.GET, null, new ParameterizedTypeReference<String>() {
		            });
		String productListJsonResponse = rateResponse.getBody();

		JsonElement productListJsonArray =
			new Gson().fromJson(productListJsonResponse, JsonArray.class);
		return productListJsonArray.toString();
	}

	public String getProductsByCategory(String name, int limit, int offset) {
		String encodedName = name.replace(" ","%20").replace("&","%26").replace(",","%2C");
		String restURL = restUrlBase + "products/category/" + encodedName+ "?limit=" + limit + "&offset=" + offset;
		System.out.println(restURL);
		ResponseEntity<String> rateResponse =
		        restTemplate.exchange(restURL,
		                    HttpMethod.GET, null, new ParameterizedTypeReference<String>() {
		            });
		String productListJsonResponse = rateResponse.getBody();

		JsonElement productListJsonArray =
			new Gson().fromJson(productListJsonResponse, JsonArray.class);
		return productListJsonArray.toString();
	}

	/**
	 * Loads the details page of any product.
	 */
	public String getProductDetails(String asin) {

		String restURL = restUrlBase + "product/" + asin;
		ResponseEntity<String> rateResponse =
		  restTemplate.exchange(
		  	restURL,
				HttpMethod.GET, null, new ParameterizedTypeReference<String>() {});
		String productDetailsJsonResponse = rateResponse.getBody();
		return productDetailsJsonResponse;
	}	

	public String addProductToCart(String asin) {

		String restURL = restUrlBase + "shoppingCart/addProduct";
		MultiValueMap<String, String> params = new LinkedMultiValueMap<String, String>();
		params.add("asin", asin);
		

		HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<MultiValueMap<String, String>>(params, null);

		ResponseEntity<String> rateResponse =
		        restTemplate.exchange(restURL,
		                    HttpMethod.POST, request, new ParameterizedTypeReference<String>() {
		            });
		String addProductJsonResponse = rateResponse.getBody();
		return addProductJsonResponse;
	}

	public String removeProductFromCart(String asin) {

		String restURL = restUrlBase + "shoppingCart/removeProduct";
		MultiValueMap<String, String> params = new LinkedMultiValueMap<String, String>();
		params.add("asin", asin);
		

		HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<MultiValueMap<String, String>>(params, null);

		ResponseEntity<String> rateResponse =
		        restTemplate.exchange(restURL,
		                    HttpMethod.POST, request, new ParameterizedTypeReference<String>() {
		            });
		String addProductJsonResponse = rateResponse.getBody();
		return addProductJsonResponse;
	}

	public String getCart() {
		String restURL = restUrlBase + "shoppingCart";
		ResponseEntity<String> rateResponse =
		        restTemplate.exchange(restURL,
		                    HttpMethod.POST, null, new ParameterizedTypeReference<String>() {
		            });
		String getCartJsonResponse = rateResponse.getBody();
		return getCartJsonResponse;
	}

	public String checkout() {

		String restURL = restUrlBase + "shoppingCart/checkout";
		MultiValueMap<String, String> params = new LinkedMultiValueMap<String, String>();
		params.add("userId", "1");
		

		HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<MultiValueMap<String, String>>(params, null);

		ResponseEntity<String> rateResponse =
		        restTemplate.exchange(restURL,
		                    HttpMethod.POST, request, new ParameterizedTypeReference<String>() {
		            });
		String addProductJsonResponse = rateResponse.getBody();
		return addProductJsonResponse;
	}

	public String showCart() {
		String restURL = restUrlBase + "shoppingCart";
		MultiValueMap<String, String> params = new LinkedMultiValueMap<String, String>();
		params.add("userId", "1");
		

		HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<MultiValueMap<String, String>>(params, null);

		ResponseEntity<String> rateResponse =
		        restTemplate.exchange(restURL,
		                    HttpMethod.POST, request, new ParameterizedTypeReference<String>() {
		            });
		String addProductJsonResponse = rateResponse.getBody();
		return addProductJsonResponse;
	}	
}
