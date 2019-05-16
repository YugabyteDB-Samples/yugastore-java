
import React, { PureComponent } from 'react';
import { Icon } from '../';
//Internals
import './index.css';

class Button extends PureComponent {
  render() {
    return (
      <button disabled={this.props.disabled} onClick={this.props.onClick} className={"btn btn-"+this.props.size+" btn-"+this.props.color+" "+this.props.className}>
        {this.props.icon && <Icon color={this.props.iconColor} icon={this.props.icon}/>}
        {this.props.children}
      </button>
    );
  }
}

export default Button;
