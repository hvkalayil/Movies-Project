import { selectMovies } from "../services/reducers/movies"
import { useAppSelector } from "../store"

function Carousel() {
    const movies = useAppSelector(selectMovies)
    const carouselItems = movies.data.map((movie) => (
        <div className="flex flex-col w-1/4 h-1/4 m-4">
            <img src={movie.Poster} alt={movie.MovieName} />
            <h1>{movie.MovieName}</h1>
        </div>
    ))

    return (
        <div className="w-full flex flex-row flex-wrap justify-center bg-cyan-600">
            {carouselItems}
        </div>
    )
}

export default Carousel