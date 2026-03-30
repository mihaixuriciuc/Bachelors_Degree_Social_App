import SubmitAction from "./SubmitAction";

function SignInForm() {
  return (
    <form
      action="post"
      onSubmit={SubmitAction}
      className="d-flex flex-column m-1"
    >
      <input
        type="text"
        name="username"
        placeholder="User Name"
        className="m-2"
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        className="m-2"
      />
      <label className="d-flex justify-content-center">
        <button type="reset">Try again</button>
        <button type="submit">Submit</button>
      </label>
    </form>
  );
}

export default SignInForm;
