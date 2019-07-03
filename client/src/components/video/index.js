import React, { Component } from 'react'
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { getVideo } from "../../actions/videoActions";
import { Container, Row, Col } from 'react-bootstrap';

import Player from './Player';
import TimeCodes from './Timecodes';


class Video extends Component {

    constructor(props) {
        super(props); 
        this.html5player = React.createRef();
        this.onKeyDown = this.onKeyDown.bind(this)
    }

    static propTypes = {
        videoData: PropTypes.shape({
            title: PropTypes.string,
            video: PropTypes.string,
            timeData: PropTypes.array,
        })
    }

    static defaultProps = {
        videoData: {
            title: '',
            video: '',
            timeData: [],
        }
    }

    componentDidMount () {
        document.addEventListener('keydown', this.onKeyDown);
        document.onkeydown  = this.disableSpaceScroll;
        const { id } = this.props.match.params
        this.props.getVideo(id);
    }

    componentWillUnmount() {
        document.removeEventListener('keydown', this.onKeyDown, false)
        document.onkeydown = null;
    }

    state = {
        isPlaying: false,
    }

    disableSpaceScroll = (e) => {
        return e.code !== 'Space'
    }

    changeCurrentTime = (time) => { //time in seconds
        const player = this.html5player.current;
        player.currentTime = time;
        player.play()
    }

    play = () => {
        this.setState({ isPlaying: true });
    }

    pause = () => {
        this.setState({ isPlaying: false });
    }

    switchPlayPause = () => {
        const { isPlaying } = this.state;
        const player = this.html5player.current;

        if (!isPlaying){
            player.play()
        } else {
            player.pause()
        }
        this.setState({ isPlaying: !this.state.isPlaying })
    }

    onKeyDown = (e) => {
        if (e.code === 'Space'){
            this.switchPlayPause()
        }
    }

    render = () => {
        const {timeData, video, title} = this.props.videoData;
        const { id } = this.props.match.params;
        const url = `/api/videos/file/${id}`;

        return (
            <Container>
                <br/>
                <Row>
                    <Col xs={'12'}>
                        <h3>{title}</h3>
                    </Col>
                </Row>
                 <Row>
                    <Col xs={'9'}>
                        <Player reference={this.html5player}
                                play={this.play}
                                pause={this.pause}
                                switch={this.switchPlayPause}
                                src={url}
                        />
                    </Col>

                    <Col xs={'3'}>
                        <TimeCodes changeCurrentTime={this.changeCurrentTime}
                                   timeCodes={timeData}/>
                    </Col>
                </Row>
            </Container>
    )
  }
}

const mapStateToProps = state => ({
    videoData: state.video.videoData,
    loading: state.video.loading
})

export default connect(mapStateToProps, {getVideo})(Video);

const globalURL = 'http://192.168.1.69:10228';

const id = '5c926f6858dfc746ad92e9e5'