// Dependencies
import _ from 'lodash';
import React, { Component } from 'react';
// Externals
import Cart from '../Cart';
import ShowProduct from '../ShowProduct';
import Products from '../Products';
import Home from '../Home';
import { Navbar, Footer, Subscribe } from '../Main/components';
import { Route, Switch } from 'react-router-dom';
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cart: {
        data: {},
        total: 0
      },
      scrolled: false,
      index: 0,
    };
  }

  componentWillUnmount() {
    window.removeEventListener('scroll');
  }

  componentDidMount() {
    this.fetchCart();
  }

  componentWillMount() {
    window.addEventListener('scroll', () =>{
      let supportPageOffset = window.pageXOffset !== undefined;
      let isCSS1Compat = ((document.compatMode || '') === 'CSS1Compat');
      const scroll = {
         x: supportPageOffset ? window.pageXOffset : isCSS1Compat ? document.documentElement.scrollLeft : document.body.scrollLeft,
         y: supportPageOffset ? window.pageYOffset : isCSS1Compat ? document.documentElement.scrollTop : document.body.scrollTop
      };
  
      if(scroll.y > 50 && !this.state.scrolled){
        this.setState({
          scrolled: true
        });
      } else if (scroll.y < 50 && this.state.scrolled) {
        this.setState({
          scrolled: false
        });
      }
    });
  }

  fetchCart = () => {
    const self = this;
    var url = '/cart/get';
    fetch(url, {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then(res => res.json())
      .then(cart => this.setState({
        cart: {
          data: cart,
          total: self.totalReducer(cart),
          error: false
        }
      }));
  }

  totalReducer = (data) => {
    let sum = 0;
    for( var el in data ) {
      if( data.hasOwnProperty( el ) ) {
        sum += parseFloat( data[el] );
      }
    }
    return sum;
  }

  addItemToCart = (product) => {
    if (product) {
      console.log("Added to Cart "+product.title);
      
      const self = this;
      const url = '/cart/add?asin='+(product.id.asin || product.id);
      let requestData = new FormData();
      requestData.append( "json", JSON.stringify( {asin: product.id} ));

      fetch(url, {  
        method: 'POST',
        body: requestData,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
        .then(res => res.json())
        .then(data => {
            self.setState({
              cart: {
                data: data,
                total: self.totalReducer(data)
              }
            });
        })
        .catch(error => {
          this.setState({
            cart: { ...this.state.cart, error: true }
          });
    
          setTimeout(() => this.setState({
            cart: { ...this.state.cart, error: false }
          }), 2500);
          console.warn('Request failed', error);

        });
    }
  }

  removeItemFromCart = (product) => {
    if (product) {
      console.log("Removed from Cart "+product.title);
      
      const self = this;
      const url = '/cart/remove/?asin='+product.id;
      let requestData = new FormData();
      requestData.append( "json", JSON.stringify( {asin: product.id} ));

      fetch(url, {  
        method: 'POST',
        body: requestData,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
        .then(res => res.json())
        .then(data => {
            // const dataMerged = {};
            // const data = self.state.cart.data;
            // dataMerged[product.id.asin || product.id] = data[product.id.asin || product.id] ? data[product.id.asin || product.id] + 1 : 1;
            
            self.setState({
              cart: {
                data: data,
                total: self.totalReducer(data)
              }
            });
        })
        .catch(error => {
          this.setState({
            cart: { ...this.state.cart, error: true }
          });
    
          setTimeout(() => this.setState({
            cart: { ...this.state.cart, error: false }
          }), 2500);
          console.warn('Request failed', error);
        });
    }
  }

  render() {
    return(

      <div>
        <Navbar cart={this.state.cart} scrolled={this.state.scrolled}/>
        <Switch>
          <Route exact path="/" 
            render={(props) => (
              <Home
                addItemToCart={this.addItemToCart} />
            )} />
      
          <Route path="/cart" 
            render={(props) => (
              <Cart
                cart={this.state.cart} fetchCart={this.fetchCart} removeItemFromCart={this.removeItemFromCart}/>
            )} />
      
          <Route path="/Music"
            render={(props) => (
              <Products
                category="Music"
                addItemToCart={this.addItemToCart} />
            )} />
          <Route path="/Books"
            render={(props) => (
              <Products
                category={"Books"}
                addItemToCart={this.addItemToCart} />
            )} />
          <Route path="/Beauty"
            render={(props) => (
              <Products
                category={"Beauty"}
                addItemToCart={this.addItemToCart} />
            )} />
          <Route path="/Electronics"
            render={(props) => (
              <Products
                category={"Electronics"}
                addItemToCart={this.addItemToCart} />
            )} />
          <Route exact path="/:category"
            render={(props) => (
              <Products
                {...props}
                addItemToCart={this.addItemToCart} />
            )} />
    
          <Route path="/sort/:query"
            render={(props) => (
              <Products
                sort={props.match.params.query}
                addItemToCart={this.addItemToCart} />
            )} />
      
          <Route exact path="/item/:id" render={(props) => (
            <ShowProduct {...props} addItemToCart={this.addItemToCart}/>
          )}/>
        </Switch>
        <Subscribe/>
        <Footer />
      </div>
    )
  }
}
