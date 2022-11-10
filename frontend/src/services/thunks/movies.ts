import { AppThunk } from "../../store";
import { movie_load_fail, movie_load_in_progress, movie_load_success } from "../reducers/movies";

export const getMovies = ():AppThunk => async (dispatch) => {
    try {
        dispatch(movie_load_in_progress())
        
        const data = await fetch(`${import.meta.env.VITE_API_URL}/api/movies`)
        const movies = await data.json()

        dispatch(movie_load_success(movies))
    } catch (error) {
        console.log(error);
        dispatch(movie_load_fail())
    }
}