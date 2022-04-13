import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import { API_BASE_URL } from "../Config";
import Block from "./Block";
import { Link } from "react-router-dom";

const PAGE_RANGE = 3;

function Blockchain() {
  const [blockchain, setBlockchain] = useState([]);
  const [blockchainLength, setBlockchainLenth] = useState(0);

  const fetchBlockchainPage = ({ start, end }) => {
    fetch(`${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
      .then((response) => response.json())
      .then((json) => setBlockchain(json));
  };

  useEffect(() => {
    fetchBlockchainPage({ start: 0, end: PAGE_RANGE });

    fetch(`${API_BASE_URL}/blockchain/length`)
      .then((response) => response.json())
      .then((json) => setBlockchainLenth(json));
  }, []);

  const buttonNumbers = [];
  for (let i = 0; i < Math.ceil(blockchainLength / PAGE_RANGE); i++) {
    buttonNumbers.push(i);
  }

  return (
    <div className="Blockchain">
      <Link to="/">Home</Link>
      <hr />
      <h3>Blockchain</h3>
      <div>
        {blockchain.map((block) => (
          <Block key={block.hash_} block={block} />
        ))}
      </div>
      <div>
        {buttonNumbers.map((number) => {
          const start = number * PAGE_RANGE;
          const end = (number + 1) * PAGE_RANGE;
          return (
            <span key={number}>
              <Button
                size="sm"
                variant="danger"
                onClick={() => fetchBlockchainPage({ start, end })}
              >
                {number + 1}
              </Button>{" "}
            </span>
          );
        })}
      </div>
    </div>
  );
}

export default Blockchain;
