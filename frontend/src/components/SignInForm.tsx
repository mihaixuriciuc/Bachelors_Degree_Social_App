import SubmitAction from "../helpers/SubmitAction";

function SignInForm() {
  const apiUrl = import.meta.env.API_URL;
  return (
    <form
      action="post"
      onSubmit={(e) => SubmitAction(e, "http://127.0.0.1:8000/api/v1/signin/")}
      className="d-flex flex-column m-3"
    >
      <input
        type="text"
        name="username"
        placeholder="User Name"
        className="m-1"
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        className="m-1"
      />
      <label className="d-flex justify-content-center">
        <button type="reset">Try again</button>
        <button type="submit">Submit</button>
      </label>
    </form>
  );
}

export default SignInForm;
