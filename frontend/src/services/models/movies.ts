export interface Movie {
    _id: string;
    Plot: string;
    Director: string;
    Writer: string;
    Cast: string[];
    Rating: string;
    Genre: string[];
    Poster: string;
    MovieName: string;
    ReleaseDate: string;
    ScreenPlay: string[];
    Day: number;
    Month: number
    isGood: boolean
}