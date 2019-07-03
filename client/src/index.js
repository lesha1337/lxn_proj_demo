import React from 'react';
import ReactDOM from 'react-dom';
import "bootstrap/dist/css/bootstrap.min.css";
import './index.css';
import Router from './Router';
import * as serviceWorker from './serviceWorker';
import { Provider } from "react-redux";
import store from "./store";

ReactDOM.render(
        <Provider store={store}>
            <Router />
        </Provider>
    , document.getElementById("root")
);

serviceWorker.unregister();
