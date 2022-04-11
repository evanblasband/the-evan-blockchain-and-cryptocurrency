import React, { useState, useEffect } from "react";
import logo from "../assets/logo.png";
import { API_BASE_URL } from "../Config";
import Blockchain from "./Blockchain";

function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
      .then((response) => response.json())
      .then((json) => setWalletInfo(json));
  }, []);

  const { address, balance } = walletInfo;

  return (
    <div className="App">
      <img className="logo" src={logo} alt="application-logo" />
      <h2>Welcome to the Evan Blockchain</h2>
      <h3>
        This project was created as a way for mydlef to learn how blockchains
        and cryptocurrencies work at the low level.
      </h3>
      <br />
      <div className="walletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
      <br />
      <Blockchain />
    </div>
  );
}

export default App;
