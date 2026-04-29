import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home/Home";
import SignUp from "./pages/SignUp/SignUp";
import SignIn from "./pages/SignIn/SignIn";
import { AuthProvider } from "./context/AuthContext";
import Feed from "./pages/Feed/Feed";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        {/*so the best practice is to leave only the one with "/" if you dont have text */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/signin" element={<SignIn></SignIn>} />
          <Route path="/feed" element={<Feed />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
export default App;
