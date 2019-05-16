import React, { Component } from 'react';
import { Grid, FormGroup, FormControl } from 'react-bootstrap';
import { Button } from '../../../common';
import './index.css';

class Subscribe extends Component {
  render() {
    return(
    <div className="subscribe">
      <Grid>
        <div className="left">
          <h5>Let’s keep the conversation going</h5>
          <p>Receive our newsletter and discover our stories, collections, and surprises.</p>
        </div>
        <div className="right">
          <form>
            <FormControl placeholder="Email"/>
            <Button size="large">Subscribe</Button>
          </form>
        </div>
      </Grid>
    </div>
    )
  }
}

export default Subscribe;
