//Dependencies
import React, { PureComponent } from 'react';
import { Logo } from '../';
import { Icon } from '../../../common';
import { NavLink } from 'react-router-dom';
//Internals
import './index.css';

class Footer extends PureComponent {
  linkFormat = (name) => {
    return name.replace(' ','%20').replace(/&/g, '%26').replace(',', '%2C');
  }

  render() {
    return(
      <div className="footer">
        <div className="footer-block1">
          <Logo mode={'dark'} />

          <div>This app is made with YugaByte DB. <br/>Read more on <NavLink to="http://yugabyte.com">yugabyte.com</NavLink></div>
          <p>© Copyright Yugabyte 2018</p>
        </div>
        <div className="footer-block2">
          <h6>Categories</h6>
          <ul>
            <li><NavLink to={`/${this.linkFormat("Books")}`}>Books</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Music")}`}>Music</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Beauty")}`}>Beauty</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Electronics")}`}>Electronics</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Kitchen & Dining")}`}>Kitchen & Dining</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Toys & Games")}`}>Toys & Games</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Pet Supplies")}`}>Pet Supplies</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Grocery & Gourmet Food")}`}>Grocery & Gourmet Food</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Video Games")}`}>Video Games</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Movies & TV")}`}>Movies & TV</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Arts, Crafts & Sewing")}`}>Arts, Crafts & Sewing</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Kitchen & Dining")}`}>Kitchen & Dining</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Home & Kitchen")}`}>Home & Kitchen</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Patio, Lawn & Garden")}`}>Patio, Lawn & Garden</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Health & Personal Care")}`}>Health & Personal Care</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Cell Phones & Accessories")}`}>Cell Phones & Accessories</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Industrial & Scientific")}`}>Industrial & Scientific</NavLink></li>
            <li><NavLink to={`/${this.linkFormat("Sports & Outdoors")}`}>Sports & Outdoors</NavLink></li>
          </ul>
        </div>
      </div>
    )
  }
}

export default Footer;
