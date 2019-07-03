import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from "react-router-dom";

import NavigationBar from './components/navigationBar';
import Main from "./components/main";
import Feed from "./components/feed";
import Video from "./components/video";

class App extends Component {
  render() {
    return (
        <>
            <NavigationBar/>
            <BrowserRouter>
                <Switch>
                    <Route exact path="/" component={() => <div>hello</div>} />
                    <Route path="/feed" component={Feed} />
                    <Route path="/video/:id" component={Video} />
                </Switch>
            </BrowserRouter>
        </>
    );
  }
}

export default App;
