// src/helpers/SubmitAction.ts
import api from "../api/api";

export default async function SubmitAction(
  e: React.FormEvent,
  endpoint: string,
  navigate: any,
  redirectPath: string = "/feed",
) {
  e.preventDefault();

  // Extract data from your form
  const formData = new FormData(e.target as HTMLFormElement);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await api.post(endpoint, data);

    // If Django returns success (200 OK or 201 Created)
    if (response.status === 200 || response.status === 201) {
      // 🚀 Redirect the user to the Feed!
      navigate(redirectPath);
    }
  } catch (error) {
    console.error("Authentication failed:", error);
    // Here you could later add an alert or error state to show the user
    alert("Something went wrong. Check your credentials.");
  }
}
