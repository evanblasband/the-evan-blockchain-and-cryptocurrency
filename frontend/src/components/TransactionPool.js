import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Transaction from "./Transaction";
import { API_BASE_URL, SECONDS_JS } from "../Config";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router";

const POLL_INTERVAL = 10 * SECONDS_JS;

function TransactionPool() {
  let navigate = useNavigate();
  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = () =>
    fetch(`${API_BASE_URL}/transactions`)
      .then((response) => response.json())
      .then((json) => {
        console.log("transactions json", json);
        setTransactions(json);
      });

  const mineTransaction = () =>
    fetch(`${API_BASE_URL}/blockchain/mine`)
      .then((response) => {
        console.log(response.status);
        if (response.status === 200) {
          return response.json();
        } else {
          alert("Error: ", response.body);
        }
      })
      .then((json) => {
        console.log(json);
        alert("Successfully mined the block");
        navigate("/blockchain");
      });

  useEffect(() => {
    fetchTransactions();
    const intervalId = setInterval(fetchTransactions, POLL_INTERVAL);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="TransactionPool">
      <Link to={"/"}>Home</Link>
      <hr />
      <h3>Transactions</h3>
      <div>
        {transactions.map((transaction) => (
          <div key={transaction.id}>
            <hr />
            <Transaction transaction={transaction} />
          </div>
        ))}
      </div>
      <hr />
      <Button variant="danger" onClick={mineTransaction}>
        Mine a block of these transactions
      </Button>
    </div>
  );
}

export default TransactionPool;
