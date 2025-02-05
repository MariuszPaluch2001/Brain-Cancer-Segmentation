import React, { Fragment } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "../components/home/home"
const RoutesComponent = () => {

  return (
    <Fragment>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>} />
      </Routes>
      </BrowserRouter>
    </Fragment>
  );
};

export default RoutesComponent;
