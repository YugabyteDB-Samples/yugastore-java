// Dependencies
import axios from 'axios';
import React, { Component } from 'react';
import { Link } from 'react-router-dom';
//Internals
import { Hero } from '../Main/components';
import Products from '../Products';
import './index.css';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cart: {},
    };
  }

  render() {
    return (
      <div>
        <Hero/>
        <div className="paragraph">
          <Products addItemToCart={this.props.addItemToCart} isInline={true} name={<span>Bestsellers in <Link to={"/Books"}>Books</Link></span>} category="Books" limit={4}/>
          <Products addItemToCart={this.props.addItemToCart} isInline={true} name={<span>Bestsellers in <Link to={"/Music"}>Music</Link></span>} category="Music" limit={4}/>
          <Products addItemToCart={this.props.addItemToCart} isInline={true} name={<span>Bestsellers in <Link to={"/Books"}>Beauty</Link></span>} category="Beauty" limit={4}/>
          <Products addItemToCart={this.props.addItemToCart} isInline={true} name={<span>Bestsellers in <Link to={"/Electronics"}>Electronics</Link></span>} category="Electronics" limit={4}/>
        </div>
      </div>
    );
  }
}

export default Home;
