//Dependencies
import React, { Component } from 'react';
import { Icon } from 'react-materialize';
import { Button } from "../../components/common";
import { Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
//Internals
import './index.css';

class ShowProduct extends Component {
  state = {product_id: "", product: undefined, productAlsoBought: []}

  componentDidMount() {
    var new_product_id = this.props.match.params.id;
    this.fetchProductDetails(new_product_id)
  }

  fetchProductDetails = (new_product_id) => {
    if (new_product_id != undefined &&
        this.state.product_id != undefined &&
        new_product_id != this.state.product_id) {
      this.state.product_id = "" + new_product_id;
      var url = '/products/details?asin=' + new_product_id;
      console.log("Fetching url: " + url);
      fetch(url)
        .then(res => res.json())
        .then(product => {
          this.setState({ product });
          if (product.also_bought) this.fetchProductAlsoBought(product.also_bought.slice(0,4));
        });
    }
  }

  fetchProductAlsoBought = (productList) => {
    productList.forEach(element => {
      let url = '/products/details?asin=' + element;
      fetch(url,{
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        })
        .then(res => res.json())
        .then(product => {if (product.id) this.setState({ productAlsoBought: [...this.state.productAlsoBought, product] })});
    });
  }

  render () {
    var new_product_id = this.props.match.params.id;
    this.fetchProductDetails(new_product_id)
    const currentProduct = this.state.product;
    if (!currentProduct) {
      return ("");      
    }
    var stars = ["star_border", "star_border", "star_border", "star_border", "star_border"];
    if (currentProduct.avg_stars > 0) {
      stars[0] = (currentProduct.avg_stars < 1) ? "star_half" : "star";
    }
    if (currentProduct.avg_stars > 1) {
      stars[1] = (currentProduct.avg_stars < 2) ? "star_half" : "star";
    }
    if (currentProduct.avg_stars > 2) {
      stars[2] = (currentProduct.avg_stars < 3) ? "star_half" : "star";
    }
    if (currentProduct.avg_stars > 3) {
      stars[3] = (currentProduct.avg_stars < 4) ? "star_half" : "star";
    }
    if (currentProduct.avg_stars > 4) {
      stars[4] = (currentProduct.avg_stars < 5) ? "star_half" : "star";
    }
    console.log(currentProduct);
    return (
      <div className="show-product">
        <div className="content">
          <div className="container">
            {currentProduct && <div className="item-wrapper">
              <Row>
                <Col xs={10} xsPush={1}>
                  <div className="item-image">
                    <img className="product-image" src={currentProduct.imUrl} alt="product" />
                  </div>

                  <div className="item-details">
                    <div className="item-name">
                      <div className="product-info">
                        <h2 id="product-name">{currentProduct.title}</h2>
                      </div>
                      <div className="product-review">
                        <div className="stars">
                          <Icon small id="add-icon" className="review-star">{ stars[0] }</Icon>
                          <Icon small id="add-icon" className="review-star">{ stars[1] }</Icon>
                          <Icon small id="add-icon" className="review-star">{ stars[2] }</Icon>
                          <Icon small id="add-icon" className="review-star">{ stars[3] }</Icon>
                          <Icon small id="add-icon" className="review-star">{ stars[4] }</Icon>
                        </div>
                      </div>
                      <div className="product-bio">
                        <div className="product-review">
                          {currentProduct.num_stars} stars from {currentProduct.num_reviews} reviews
                        </div>
                        <div className="add-to-cart">
                          <Button color="primary" onClick={() => this.props.addItemToCart(currentProduct)} size="large">
                            <Icon small className="add-icon">add_shopping_cart</Icon>Add to cart
                          </Button>
                        </div>
                        <div className="product-price">${currentProduct.price.toFixed(2)}</div>
                        <div className="product-description">{currentProduct.description}</div>
                      </div>
                    </div>
                  </div>
                </Col>
              </Row>
            </div>}
          </div>
        </div>
        {Boolean(this.state.productAlsoBought.length) && 
        <div className="content content-white">
          <div className="container">
          <div className="products">

            <div className="products-title">
              <h1 className="highlights-title">Also bought</h1>
            </div>
          <div className="items">
              {
                this.state.productAlsoBought.map(product => {
                  if (product.avg_stars > 0) {
                    stars[0] = (product.avg_stars < 1) ? "star_half" : "star";
                  }
                  if (product.avg_stars > 1) {
                    stars[1] = (product.avg_stars < 2) ? "star_half" : "star";
                  }
                  if (product.avg_stars > 2) {
                    stars[2] = (product.avg_stars < 3) ? "star_half" : "star";
                  }
                  if (product.avg_stars > 3) {
                    stars[3] = (product.avg_stars < 4) ? "star_half" : "star";
                  }
                  if (product.avg_stars > 4) {
                    stars[4] = (product.avg_stars < 5) ? "star_half" : "star";
                  }
                  return (
                    <Col lg={3} md={6} xs={12} key={product.id}>
                      <div className="item" >
                        <Link to={`/item/${product.id}`}>
                          <div className="product-img" style={{backgroundImage: `url(${product.imUrl})`}}></div>
                          <div className="product-details">
                            <div className="reviews-add">
                              <div className="stars">
                                <Icon small id="add-icon" className="review-star">{ stars[0] }</Icon>
                                <Icon small id="add-icon" className="review-star">{ stars[1] }</Icon>
                                <Icon small id="add-icon" className="review-star">{ stars[2] }</Icon>
                                <Icon small id="add-icon" className="review-star">{ stars[3] }</Icon>
                                <Icon small id="add-icon" className="review-star">{ stars[4] }</Icon>
                              </div>
                              {product.num_stars} stars from {product.num_reviews} reviews
                            </div>
                            <div className="product-name">{product.title}</div>
                          </div>
                        </Link>
                        <button onClick={() => this.props.addItemToCart(product)} className="price-add">
                          <div className="product-price">${product.price}</div>
                          <Icon small className="add-icon">add_shopping_cart</Icon>
                        </button>
                      </div>
                    </Col>
                  )
                })
              }
            </div>
            </div>
          </div>
        </div>}
      </div>
    );
  }
}

export default ShowProduct;
