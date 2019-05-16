// Dependencies
import React, { Component } from 'react';
//Internals
import './index.css';
import { Navbar, Footer } from './components';

class Main extends Component {

  render() {
    return (
      <div>
        <Navbar/>
        {this.props.children}
        <Footer />
      </div>
    );
  }
}

export default Main;
