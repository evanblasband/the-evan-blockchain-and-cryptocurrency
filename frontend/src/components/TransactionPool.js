import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Transaction from "./Transaction";
import { API_BASE_URL, SECONDS_JS } from "../Config";

const POLL_INTERVAL = 10 * SECONDS_JS;

function TransactionPool() {
  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = () =>
    fetch(`${API_BASE_URL}/transactions`)
      .then((response) => response.json())
      .then((json) => {
        console.log("transactions json", json);
        setTransactions(json);
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
    </div>
  );
}

export default TransactionPool;
