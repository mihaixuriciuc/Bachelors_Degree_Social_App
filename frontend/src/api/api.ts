import axios from "axios";

// 1. Helper function to find a specific cookie by its name
function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`; // document.cookie returns cookies in a string, puts : at the beggining (document is the whole page)
  const parts = value.split(`; ${name}=`);  // take the value and split it where the content is found, but the content is removed
  //for example it will be split when ;crsftoken= is found, and ill have the value " ", "13515; nextoken=3235r23532" there will be always two parts
  //if the token was found, the next statement will be true
  if (parts.length === 2) {
    return parts[1]?.split(";").shift() || null;
    // parts has exactly two parts, and im interested in the second one because it contains the value of the token at the beggining
    // then i split again at ";" and get the first element that remained after, and its exactly the value of the token alone
    //it returns the token exactly without the specification, it returns null otherwise
  }
  return null;
}

// 2. Create the central Axios instance
const api = axios.create({  // axios.create() is a preconfigured axios instance
  baseURL: "http://localhost:8000/api/v1", // basurl of the backend 
  withCredentials: true, // This tells the browser to always send/receive cookies
  headers: {
    "Content-Type": "application/json", // tells the backend that json is sent
  },
});


api.interceptors.request.use( // interceptors are functions that run before every request is sent
  (config) => {
    // Django only needs CSRF tokens for "unsafe" methods that change data
    const unsafeMethods = ["post", "put", "patch", "delete"];

    if (config.method && unsafeMethods.includes(config.method.toLowerCase())) { // checks to see if the api method called is valid, and then to see if the specific method is unsafe
      const csrfToken = getCookie("csrftoken"); // we get onlu the token from the string with the method used above
      if (csrfToken) { //check if the token exists
        config.headers["X-CSRFToken"] = csrfToken; // Attach the token!
      }
    }
    return config; // if the method is safe (get) skip dirrectly here
  },
  (error) => {
    return Promise.reject(error); // error block
  },
);

export default api;
