//Dependencies
import React, { Component } from 'react';
import { Icon } from 'react-materialize';
import _ from 'lodash';
import { Link } from 'react-router-dom';
import { Row, Col } from 'react-bootstrap';
import { Button } from '../../components/common';
//Internals
import './index.css';

class Products extends Component {
  state = {current_query: "", category: undefined, products: [], isUpdating: true}

  componentDidMount() {
    const category = this.props.category || this.props.match.params.category;
    this.setState({ category: this.linkEncode(category) || null }, this.fetchProducts(this.linkEncode(category)));
  }

  componentWillReceiveProps(nextProps) {
    const category = nextProps.category || nextProps.match.params.category;
    if (this.state.category !== this.linkEncode(category) && this.state.category !== undefined) this.setState({ category: this.linkEncode(category), products: [] }, this.fetchProducts(this.linkEncode(category)));
  }

  shouldComponentUpdate(nextProps, nextState) {
    return !_.isEqual(this.state.products, nextState.products);
  }

  linkEncode = (name) => {
    return name.replace(' ','%20').replace(/&/g, '%26').replace(',', '%2C');
  }

  linkDecode = (name) => {
    return name.replace('%20',' ').replace('%26', '&').replace('%2C', ',');
  }

  fetchProducts(nextCategory, nextLimit, nextOffset) {
    let url, query = '';
    const limit = this.props.limit || 12 || nextLimit;
    const offset = this.props.offset || nextOffset || 0;
    if (nextCategory) {
      url = '/products/category?';
      query = 'name=' + nextCategory + '&';
    }
    else {
      url = '/products?';
    }
    query += "limit=" + limit + '&';
    query += "offset=" + offset;
    this.setState({ current_query: url+query })
    if (this.state.current_query !== url+query) {
      fetch(url+query)
        .then(res => res.json())
        .then(products => this.setState({ products, limit, offset, isUpdating: false }));
    }
  }

  setSortName(query) {
    switch (query) {
      case "num_stars":
        return "Books with the Highest Rating";
      case "num_reviews":
        return "Books with the Most Reviews";
      case "num_buys":
        return "Best Selling Books";
      case "num_views":
        return "Books with the Most Pageviews";
      default:
        return "";
    }
  }

  render() {
    let stars = ["star_border", "star_border", "star_border", "star_border", "star_border"];
    const self = this;
    const category = this.props.category || this.props.match.params.category;
    return (
      <div className={ "container " + (this.props.isInline ? '' : "content")}>
        <div className="products">
        <div className="products-title">
          <h1 className="highlights-title">{this.props.name || this.linkDecode(category) || "Our bestsellers"}</h1>
        </div>

          <Row className="items">
            {Boolean(this.state.products.length) && this.state.products.sort((a, b)=>{
              if(self.props.sort) {
                return a[self.props.sort] > b[self.props.sort];
              }
              return false;
            }).map((product) => {
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
                  <Col lg={3} md={6} xs={12} key={product.id.asin || product.id}>
                    <div className="item" >
                      <Link to={`/item/${product.id.asin || product.id}`}>
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
            })}
          </Row>
          {Boolean(this.state.products.length) && this.state.limit === 12 &&
            <div className="pagination">
            <Button onClick={() => {
                  this.setState({ products: []});
                  this.fetchProducts(this.state.category, this.state.limit, this.state.offset - this.state.limit)
                }
              } size="large" disabled={!Boolean(this.state.offset)}>Previous page</Button>

              <Button onClick={() => {
                  this.setState({ products: [], isUpdating: true});
                  this.fetchProducts(this.state.category, this.state.limit, this.state.offset + this.state.limit)
                }
              } size="large" className="pull-right" disabled={(this.state.products.length < 12 && this.state.products.length !== 0) || (this.state.products.length === 0 && !this.state.isUpdating)}>Next page</Button>
            </div>
          }
        </div>
      </div>
    );
  }
}

export default Products;
