import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home/Home";
import SignUp from "./pages/SignUp/SignUp";
import SignIn from "./pages/SignIn/SignIn";
import { AuthProvider } from "./context/AuthContext";
import Feed from "./pages/Feed/Feed";
import Profile from "./pages/Profile/Profile";
import CreatePost from "./pages/CreatePost/CreatePost";
import ActivateAccount from "./pages/ActivateAccount/ActivateAccount";
import CheckEmail from "./pages/CheckEmail/CheckEmail";
import EditProfile from "./pages/EditProfile/EditProfile";
import Security from "./pages/Security/Security";
import ForgotPassword from "./pages/ForgotPassword/ForgotPassword";
import ResetPassword from "./pages/ResetPassword/ResetPassword";

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
          <Route path="/profile" element={<Profile />} />
          <Route path="/create-post" element={<CreatePost />} />
          <Route path="/activate/:uid/:token" element={<ActivateAccount />} />
          <Route path="/check-email" element={<CheckEmail />} />
          <Route path="/edit-profile" element={<EditProfile />} />
          <Route path="/security" element={<Security />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route
            path="/reset-password/:uid/:token"
            element={<ResetPassword />}
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
export default App;
