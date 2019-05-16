package com.yugabyte.app.yugastore.domain;

import java.util.ArrayList;
import java.util.List;

import org.springframework.hateoas.ResourceSupport;

public class ImageInfo extends ResourceSupport {

	List<String> alsoBought;
	List<String> alsoViewed;
	List<String> boughtTogether;

	public ImageInfo() {
		alsoBought = new ArrayList<String>();
		alsoViewed = new ArrayList<String>();
	}

	public List<String> getAlsoBought() {
		return alsoBought;
	}
	public void setAlsoBought(List<String> alsoBought) {
		this.alsoBought = alsoBought;
	}
	public List<String> getAlsoViewed() {
		return alsoViewed;
	}
	public void setAlsoViewed(List<String> alsoViewed) {
		this.alsoViewed = alsoViewed;
	}

	public List<String> getBoughtTogether() {
		return boughtTogether;
	}

	public void setBoughtTogether(List<String> boughtTogether) {
		this.boughtTogether = boughtTogether;
	}
}
