import React, {Component} from 'react';

class Player extends Component {
    render() {
        return (
            <div className={'video_wrapper'}>
                <video width={'100%'}
                       // onKeyDown={(e) => {console.log(e.key)}}
                       // style={{ position: "absolute" }}
                       onClick={this.props.switch}
                       onPlay={this.props.play}
                       onPause={this.props.pause}

                       src={this.props.src}
                       ref={this.props.reference}
                       controls={true}
                />
            </div>
        );
    }
}

export default Player;