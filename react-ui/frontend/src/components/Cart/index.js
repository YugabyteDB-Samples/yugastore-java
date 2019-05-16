//Dependencies
import React, { Component } from 'react';
import { Button } from '../../components/common';
import { Link } from 'react-router-dom';
//Internals
import './index.css';

class CartProducts extends Component {
  constructor(props) {
    super(props);
    this.state = {
      products: [],
      isCompleted: false
    };
  }

  componentDidMount() {
    Object.keys(this.props.cart.data).forEach( (product_id, quantity) =>
      this.fetchProductDetails(product_id)
    );
  }

  submitCheckout() {
    if (this.props.cart.total !== 0) {
      var url = '/cart/checkout';
      fetch(url, {  
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
        .then(res => res.json())
        .then(result => {this.setState({ result, isCompleted: true })})
        .then(res => this.props.fetchCart());
    }
  }

  costReducer = (accumulator, currentValue) => {
    const self = this;
    return accumulator + currentValue.price * parseInt(self.props.cart.data[currentValue.id] || 0);
  }

  fetchProductDetails(product_id) {
    if (!this.state.products.product_id) {
      this.state.product_id = "" + product_id;
      var url = '/products/details?asin=' + product_id;
      console.log("Fetching url: " + url);
      fetch(url)
        .then(res => res.json())
        .then(product => this.setState({ 
          products: this.state.products.concat([product])
        })
      );
    }
  }
  render() {
    const self = this;
    const totalCost = this.state.products.length ? this.state.products.reduce(this.costReducer, 0) : 0;
    return(
      <div className="cart-container">
      <div className="container">
        <h5>{ this.state.isCompleted ? "Thank you!" : "Items in cart" } {Boolean(this.props.cart.total) && <span className="total-in-cart">({this.props.cart.total})</span>}</h5>
          { this.state.products && <div className="items">
          { this.state.products.filter((product) => this.props.cart.data[product.id]).map(product => (
              <div key={product.id} className="cart-item">
                <div className="product-image">
                  <img src={product.imUrl} alt="product" />
                </div>
                <div className="details">
                  <Link to={`/item/${product.id.asin || product.id}`}>{product.title}</Link>
                </div>
    
                <div className="pricing">
                  <h6>${product.price.toFixed(2)}</h6> x {this.props.cart.data[product.id]}
                </div>
                <div className="actions">
                  <Button className="btn-cart-remove" onClick={() => this.props.removeItemFromCart(product)}  size="meduim">Remove</Button>
                </div>
              </div>
            ))}
        </div>}
        { !this.props.cart.total &&
          <h6>{ this.state.isCompleted ? <span>Your order <b>#kmp-{this.state.result.orderNumber}</b> is received.</span> : "Cart is empty"}</h6>
        }
        { Boolean(this.state.isCompleted) && this.state.result &&
          <div className="order-details">{this.state.result.orderDetails}</div>
        }
        { Boolean(this.props.cart.total) && 
            <div className="total">
              <div className="details">
              </div>

              <div className="pricing">
                Total:<br/>
                Taxes:
              </div>
              <div className="pricing">
                <h6>${totalCost.toFixed(2)}</h6>
                <h6>$0.00</h6>
              </div>
              <div className="actions">
              <Button onClick={() => {
                this.submitCheckout();
                this.setState({ isCompleted: true })
                }} size="meduim" disabled={!Boolean(this.props.cart.total)}>Checkout</Button>
              </div>
            </div>
        }
      </div>
      </div>
    );
  }
}

export default CartProducts;
