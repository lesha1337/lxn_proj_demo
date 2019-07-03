import { GET_VIDEO, GET_ALL_VIDEOS, VIDEOS_LOADING } from '../actions/types';

const initialState = {
    videos: [],
    loading: false,
}

export default (state = initialState, action) => {
    switch (action.type) {
        case GET_VIDEO:
            return {
                ...state,
                videoData: action.payload,
                loading: false
            }
        case GET_ALL_VIDEOS:
            return {
                ...state,
                videos: action.payload,
                loading: false
            }
        case VIDEOS_LOADING:
            return {
                ...state,
                loading: true
            }
        default:
            return state;
    }
}