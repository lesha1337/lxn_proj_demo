import React, {Component} from 'react';
import { ListGroup } from 'react-bootstrap'


class TimeCodes extends Component {
    constructor(props) {
        super(props);
    }

    renderData = () => {
        const {timeCodes, changeCurrentTime} = this.props;
        return timeCodes.map((elem, key) => (
            <ListGroup.Item
                onClick={() => changeCurrentTime(elem.timestamp)}
                key={key}>

                {elem.timestamp}: {elem.objectName}

            </ListGroup.Item>
        ))
    }
    render = () => {
        return (
            <ListGroup>
                {this.renderData()}
            </ListGroup>
        );
    }
}

export default TimeCodes;