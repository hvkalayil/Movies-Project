import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "../../store";
import { Movie } from "../models/movies";

export interface MoviesState {
    data:Movie[];
    isLoading:boolean
}

export const initialState:MoviesState = {
    data:[],
    isLoading:false
}

export const selectMovies = (state:RootState) => state.movies;

export const movieSlice = createSlice({
    name:'movies',
    initialState:initialState,
    reducers:{
        movie_load_in_progress:(state)=>{
            state.isLoading = true
        },
        movie_load_success:(state,action:PayloadAction<any>) => {
            state.isLoading = false,
            state.data = action.payload
        },
        movie_load_fail:(state)=>{
            state.isLoading = false;
        }
    }
})

export const {movie_load_in_progress, movie_load_success,movie_load_fail}  = movieSlice.actions

export default movieSlice.reducer