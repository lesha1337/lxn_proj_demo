import axios from 'axios';
import { GET_VIDEO, GET_ALL_VIDEOS, VIDEOS_LOADING } from "./types";

export const getVideo = id => dispatch => {
    dispatch(setVideosLoading());
    axios.get(`/api/videos/${id}`).then(res => 
        dispatch({
            type: GET_VIDEO,
            payload: res.data
        }))
};

export const getAllVideos = () => dispatch => {
    dispatch(setVideosLoading());
    axios.get(`/api/videos/`).then(res => 
        dispatch({
            type: GET_ALL_VIDEOS,
            payload: res.data
        }))
};

export const setVideosLoading = () => {
    return {
      type: VIDEOS_LOADING
    };
};