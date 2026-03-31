async function SubmitAction(e: React.FormEvent<HTMLFormElement>, url: string) {
  e.preventDefault();

  const form = e.currentTarget as HTMLFormElement;
  const formData = new FormData(form); // get the data from the form

  const formJson = Object.fromEntries(formData.entries()); // create the json format
  console.log(formJson);
  try {
    const jsonString = JSON.stringify(formJson); //this is used so i can send the data as a web string
    const requestData = {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // aparently this is the standard, it has to be in woutoes because it has the line
      },
      body: jsonString,
    };

    const connection = await fetch(url, requestData);

    const responseData = await connection.json();

    if (connection.ok) {
      console.log("Conection is good:", responseData);
    } else {
      console.log("Soemthing happened");
    }
  } catch (error) {
    console.error("Connection failed:", error);
  }
}
export default SubmitAction;
