import React, { Component } from 'react'
import { connect } from 'react-redux';
import PropTypes from "prop-types";
import { getAllVideos } from "../../actions/videoActions";
import { Container, Alert } from "react-bootstrap";
import { Link } from 'react-router-dom'

class Feed extends Component {
  componentDidMount() {
    this.props.getAllVideos();
  }

  static propTypes = {
        videos: PropTypes.array,
    }

    static defaultProps = {
        videos: [],
    }

  render() {
    const {videos} = this.props;
    
    return (
      <Container>
        <br/>
        {videos.map((elem, index) => (
          <Link to={`/video/${elem._id}`} key={index}>
            <Alert variant={'secondary'}>
              {elem.title}
            </Alert>
          </Link>
        ))}
      </Container>
    );
  }
}

const mapStateToProps = (state) => ({
  videos: state.video.videos,
  loading: state.video.loading
})

export default connect(mapStateToProps, { getAllVideos })(Feed);