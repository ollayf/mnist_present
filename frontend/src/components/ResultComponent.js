import React, { Component } from 'react';

class Result extends Component {
    constructor(props) {
        super(props);
    }

    render () {
        if (this.props.result < 0) {
            return null;
        }
        return (
            <div className='result'>
                <h2>Result: {this.props.result}</h2>
                <h4>Confidence: {this.props.confidence}</h4>
            </div>
        )
    }
}

export default Result