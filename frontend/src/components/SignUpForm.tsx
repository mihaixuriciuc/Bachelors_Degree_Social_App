import React from "react";
import SubmitAction from "../helpers/SubmitAction";

function SignUpForm() {
  const apiUrl = import.meta.env.API_URL;
  return (
    <form
      method="post"
      onSubmit={(e) => SubmitAction(e, "http://127.0.0.1:8000/api/v1/signup")}
      className="d-flex flex-column m-3"
    >
      <input
        type="text"
        name="username"
        placeholder="User Name"
        className="m-1"
      ></input>
      <input
        type="email"
        name="email"
        placeholder="Email"
        className="m-1"
      ></input>
      <input
        type="password"
        name="password"
        placeholder="Password"
        className="m-1"
      ></input>
      <input
        type="text"
        name="first_name"
        placeholder="First Name"
        className="m-1"
      ></input>
      <input
        type="text"
        name="last_name"
        placeholder="Last name"
        className="m-1"
      ></input>
      <label className="d-flex justify-content-center">
        <button type="reset">Try again</button>
        <button type="submit">Submit</button>
      </label>
    </form>
  );
}

export default SignUpForm;
