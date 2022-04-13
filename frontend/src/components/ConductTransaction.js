import React, { useState, useEffect } from "react";
import { FormGroup, FormControl, Button } from "react-bootstrap";
import { API_BASE_URL } from "../Config";
import { Link } from "react-router-dom";

function ConductTransaction() {
  const [amount, setAmount] = useState(0);
  const [recipient, setRecipient] = useState("");
  const [knownAddresses, setKnownAddresses] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/known-addresses`)
      .then((response) => response.json())
      .then((json) => setKnownAddresses(json))
      .catch((err) => {
        console.log("Error Getting Known Addresses", err);
      });
  }, []);

  const updateRecipient = (event) => {
    setRecipient(event.target.value);
  };

  const updateAmount = (event) => {
    setAmount(Number(event.target.value));
  };

  const selectWalletAddress = ({ address }) => {
    setRecipient(JSON.stringify(address).replace(/"/g, ""));
  };

  const submitTransaction = () => {
    if (amount > 0) {
      fetch(`${API_BASE_URL}/wallet/transact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient, amount }),
      })
        .then((response) => response.json())
        .then((json) => {
          console.log("submitTransaction json: ", json);
          alert("Success!");
        });
    } else {
      alert("Error: Amount has to be greater than zero");
    }
  };

  return (
    <div className="ConductTransaction">
      <Link to="/">Home</Link>
      <hr />
      <h3>Conduct a Transaction</h3>
      <br />
      <FormGroup>
        <FormControl
          imput="text"
          placeholder="recipient"
          value={recipient}
          onChange={updateRecipient}
        />
      </FormGroup>
      <br />
      <FormGroup>
        <FormControl
          input="numeric"
          placeholder="amount"
          value={amount}
          onChange={updateAmount}
        />
      </FormGroup>
      <br />
      <Button variant="danger" onClick={submitTransaction}>
        Submit
      </Button>
      <br />
      <h4>Known Addresses</h4>
      <h5>Click to select.</h5>
      <div>
        {knownAddresses.map((knownAddress, i) => {
          const address = knownAddress;
          return (
            <Button
              className="textButton"
              key={knownAddress}
              variant="link"
              onClick={() => selectWalletAddress({ address })}
            >
              {knownAddress}
              {i !== knownAddresses.length - 1 ? ", " : ""}
            </Button>
          );
        })}
      </div>
    </div>
  );
}

export default ConductTransaction;
