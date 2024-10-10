import React, { useState } from "react";
import "./App.css";
const uuid = require("uuid");

function App() {
  const [image, setImage] = useState("");
  const [uploadResultMessage, setUploadResultMessage] = useState(
    "Please upload an image to authenticate."
  );
  const [visitorName, setVisitorName] = useState("placeholder.png");
  const [isAuth, setIsAuth] = useState(false);

  function sendImage(e) {
    e.preventDefault();
    if (!image) {
      setUploadResultMessage("Please select an image before submitting.");
      return;
    }

    setVisitorName(image.name);
    const visitorImageName = uuid.v4();

    fetch(
      `https://tvg65ficag.execute-api.us-east-1.amazonaws.com/Development/fictional-vistors-images/${visitorImageName}.jpeg`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "image/jpeg",
        },
        body: image,
      }
    )
      .then(async () => {
        const response = await authenticate(visitorImageName);
        if (response === "success") {
          setIsAuth(true);
          setUploadResultMessage(
            `Hi ${response["firstName"]} ${response["lastName"]}, Nice to see you`
          );
        } else {
          setIsAuth(false);
          setUploadResultMessage("Sorry, we could not verify your identity.");
        }
      })
      .catch((error) => {
        setIsAuth(false);
        setUploadResultMessage(
          "There is an error during the authentication process. Try again"
        );
        console.error(error);
      });
  }

  async function authenticate(visitorImageName) {
    const requestUrl =
      `https://tvg65ficag.execute-api.us-east-1.amazonaws.com/Development/employee?` +
      new URLSearchParams({
        objectKey: `${visitorImageName}.jpeg`,
      });

    return await fetch(requestUrl, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => data)
      .catch((error) => console.error(error));
  }

  return (
    <div className="App">
      <h2> Fortune Facial Recognition System</h2>
      <form onSubmit={sendImage}>
        <input
          type="file"
          name="image"
          onChange={(e) => setImage(e.target.files[0])}
        />
        <button type="submit">Upload Image</button>
      </form>
      <div className={isAuth ? "success" : "failure"}>
        {uploadResultMessage}
      </div>
      <img
        src={require(`./vistors/${visitorName}`)}
        alt="Visitor"
        height={250}
        width={250}
      />
    </div>
  );
}

export default App;
