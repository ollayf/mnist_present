import React, { Component } from 'react';

class Header extends Component {
    constructor(props) {
        super(props);
    }

    render () {
        if (this.props.mode === 1) {
            return (
                <h1>
                    Ultra Instinct!!
                </h1>
            )
        }
        return (
            <h1>
                Submit a drawing of a digit!
            </h1>
        )
    }
}

export default Header
