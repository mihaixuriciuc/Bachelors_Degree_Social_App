function SubmitAction(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();

  const form = e.target as HTMLFormElement;
  const formData = new FormData(form);

  const formjson = Object.fromEntries(formData.entries());
  console.log(formData);
}

export default SubmitAction;
