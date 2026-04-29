import { Link } from "react-router-dom";
import "./Home.scss";

function Home() {
  return (
    <div className="home-page">
      <h1 className="logo-main">DOT8</h1>
      <div className="nav-links">
        <Link to="/signup" className="btn-link">
          Sign Up
        </Link>
        <Link to="/signin" className="btn-link">
          Sign In
        </Link>
      </div>
    </div>
  );
}

export default Home;
