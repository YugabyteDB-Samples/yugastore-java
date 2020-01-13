package com.yugabyte.app.yugastore.repo.rest;

import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.linkTo;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.methodOn;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.rest.webmvc.RepositoryRestController;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.yugabyte.app.yugastore.domain.ImageInfo;
import com.yugabyte.app.yugastore.domain.ProductMetadata;
import com.yugabyte.app.yugastore.repo.ProductMetadataRepo;

@RepositoryRestController
@RequestMapping(value = "/products-microservice")
public class ProductMetadataRestRepo {

	private final ProductMetadataRepo repository;

    @Autowired
    public ProductMetadataRestRepo(ProductMetadataRepo repo) {
        repository = repo;
    }

    @RequestMapping(method = RequestMethod.GET, value = "/productmetadata/relatedproducts")
    public @ResponseBody ResponseEntity<?> getRelatedProducts(@RequestParam("asin")String asin) {

    	ProductMetadata productMetadata = repository.findById(asin).get();
    	ImageInfo imageInfo = generatedRelatedProductImagesList(productMetadata);
    	imageInfo.add(linkTo( methodOn(ProductMetadataRestRepo.class).getRelatedProducts(asin)).withSelfRel());
        return new ResponseEntity<ImageInfo>(imageInfo, HttpStatus.OK);

    }

    private ImageInfo generatedRelatedProductImagesList(ProductMetadata productMetadata) {

    	ImageInfo imageInfo = new ImageInfo();

    	try {
    		imageInfo.setAlsoBought(retrieveImageUrlsFromAsin(productMetadata.getAlso_bought()));
//    		imageInfo.setAlsoViewed(retrieveImageUrlsFromAsin(productMetadata.getRelated().getAlso_viewed()));
    		imageInfo.setBoughtTogether(retrieveImageUrlsFromAsin(productMetadata.getBought_together()));
    	} catch (Exception e) {
    		e.printStackTrace();
    	}
    	return imageInfo;
    }

    private List<String> retrieveImageUrlsFromAsin(List<String> asinIds) {

    	List<String> result = new ArrayList<String>();
    	if(asinIds != null && asinIds.size() > 0) {
    		int count = 0;
    		Optional<ProductMetadata> temp;
    		for(String asin: asinIds) {
    			if (count > 10) {
    				return result;
    			} else {
    				temp = repository.findById(asin);
    				if ( temp.isPresent() && !StringUtils.isEmpty(temp.get().getImUrl())) {
	    				result.add(temp.get().getImUrl());
	    				count++;
    				}
    			}
    		}
    	}
    	return result;
    }

}
