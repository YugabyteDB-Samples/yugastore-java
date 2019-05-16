//Dependencies
import React from 'react';
import {NavLink} from 'react-router-dom';
//Internals
import './index.css';

const Highlights = () => (
  <div className="highlights">
    <div className="links-highlights">
      <p>
        <NavLink activeClassName="selected" className="nav-link-highlights" to="/sort/num_stars">
          Highest Rating
        </NavLink>
      </p>
      <p>
        <NavLink activeClassName="selected" className="nav-link-highlights" to="/sort/num_reviews">
          Most Reviews
        </NavLink>
      </p>
      <p>
        <NavLink activeClassName="selected" className="nav-link-highlights" to="/sort/num_buys">
          Best Selling
        </NavLink>
      </p>
      <p>
        <NavLink activeClassName="selected" className="nav-link-highlights" to="/sort/num_views">
          Most Viewed
        </NavLink>
      </p>
    </div>
  </div>
)

export default Highlights;
