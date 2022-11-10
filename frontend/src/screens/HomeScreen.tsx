import { useEffect } from "react";
import Carousel from "../components/carousel";
import { selectMovies } from "../services/reducers/movies";
import { getMovies } from "../services/thunks/movies";
import { useAppDispatch, useAppSelector } from "../store";

function HomeScreen() {
    const dispatch = useAppDispatch()
    useEffect(() => {
        dispatch(getMovies())
    }, [])


    return (<div className="container">
        <Carousel></Carousel>
    </div>)
}

export default HomeScreen