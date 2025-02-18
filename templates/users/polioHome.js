import React, { useState } from "react";
import "./PolioHome.css";

function PolioHome() {
  const [userName, setUserName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    // Perform any actions needed when the form is submitted
    // For example, you can send this data to a server
  };

  return (
    <div className="polio-home">
      <header>
        <h1>POLIO VACCINATION SYSTEM</h1>
      </header>
      <div id="main">
        <div id="body1">
          <img src={process.env.PUBLIC_URL + "/phome2.png"} alt="Image Loading" width="80%" />
          <div className="content">
            <h2>Do Boond Zindagi Ke</h2>
            <h2>Spare The Children, Give The Vaccine</h2>
            <h2>Life With Polio Is Full Of Challenges</h2>
            <h2>Let Us Kick Out Polio From Our Lives</h2>
          </div>
          <marquee direction="right">POLIO</marquee>
        </div>
        <div id="body2">
          <img src={process.env.PUBLIC_URL + "/india.svg"} alt="Image Loading" width="550px" />
          {/* ... Rest of the content ... */}
        </div>
        <div id="body3">
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Phone Number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <input type="submit" value="Save" />
          </form>
          {/* ... Rest of the content ... */}
        </div>
      </div>
    </div>
  );
}

export default PolioHome;
