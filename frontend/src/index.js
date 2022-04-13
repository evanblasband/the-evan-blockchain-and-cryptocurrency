import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./components/App";
import reportWebVitals from "./reportWebVitals";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Blockchain from "./components/Blockchain";
import ConductTransaction from "./components/ConductTransaction";
import TransactionPool from "./components/TransactionPool";

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" exact={true} element={<App />} />
        <Route path="/blockchain" element={<Blockchain />} />
        <Route path="/conduct-transaction" element={<ConductTransaction />} />
        <Route path="/transaction-pool" element={<TransactionPool />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
