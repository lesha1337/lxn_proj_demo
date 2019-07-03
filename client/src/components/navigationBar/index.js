import React, { Component } from 'react';
import { Navbar } from 'react-bootstrap'

class Index extends Component {
    render() {
        return (
            <Navbar bg="dark">
                <Navbar.Brand href="/feed">
                    <img
                        src="/favicon.ico"
                        width="30"
                        height="30"
                        className="d-inline-block align-top"
                        alt="React Bootstrap logo"
                    />
                </Navbar.Brand>
            </Navbar>
        );
    }
}

export default Index;