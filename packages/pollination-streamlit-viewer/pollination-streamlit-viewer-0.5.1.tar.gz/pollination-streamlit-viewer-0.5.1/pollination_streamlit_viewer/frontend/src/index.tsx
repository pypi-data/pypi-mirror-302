import React from "react"
import ReactDOM from "react-dom"
import VTKStreamlit from "./VTKStreamlit"

import 'antd/dist/antd.css';

ReactDOM.render(
  <React.StrictMode>
    <VTKStreamlit />
  </React.StrictMode>,
  document.getElementById("root")
)
