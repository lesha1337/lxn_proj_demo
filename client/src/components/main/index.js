import React, { Component } from 'react'
import { Container, Row, Col } from 'react-bootstrap'

class Main extends Component {
  render() {
    return (
      <>
        <Container>
          <Row>
            <Col md={"9"}>
              lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem
              lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem
              lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem
            </Col>
            <Col md={"3"}>
              lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem
              lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem
              lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem
            </Col>
          </Row>
        </Container>
      </>
    );
  }
}

export default Main;