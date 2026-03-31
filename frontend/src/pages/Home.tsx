import { Link } from "react-router-dom";

function Home() {
  return (
    <>
      <h1 className="font-monospace">DOT8</h1>
      <div className="position-absolute top-0 end-0 m-3">
        <Link to="/signup" className="fs-3 border border-black m-3 p-2">
          Sign Up
        </Link>
        <Link to="/signin" className="fs-3 border border-black m-3 p-2">
          Sign In
        </Link>
      </div>
    </>
  );
}

export default Home;
