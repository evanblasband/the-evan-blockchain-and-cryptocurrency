import React, { useState } from "react";
import { Button } from "react-bootstrap";
import { MILLISECONDS_PY } from "../Config";
import Transaction from "./Transaction";

function ToggleTransactionDisplay({ block }) {
  const [displayTransaction, setDisplayTransaction] = useState(false);
  const { data } = block;

  const toggleDisplayTransaction = () => {
    setDisplayTransaction(!displayTransaction);
  };

  if (displayTransaction) {
    return (
      <div>
        {data.map((transaction) => (
          <div key={transaction.id}>
            <hr />
            <Transaction transaction={transaction} />
          </div>
        ))}
        <br />
        <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
          Hide Data
        </Button>
      </div>
    );
  }

  return (
    <div>
      <br />
      <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
        Show Data
      </Button>
    </div>
  );
}

function Block({ block }) {
  const { timestamp, hash_ } = block;
  const displayHash = `${hash_.substring(0, 15)}...`;
  const displayTimestamp = new Date(
    timestamp / MILLISECONDS_PY
  ).toLocaleString();

  return (
    <div className="Block">
      <div>Hash: {displayHash}</div>
      <div>Timestamp: {displayTimestamp}</div>
      <ToggleTransactionDisplay block={block} />
    </div>
  );
}

export default Block;
