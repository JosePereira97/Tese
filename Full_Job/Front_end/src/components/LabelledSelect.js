import {MenuItem, Select} from "@material-ui/core";
import React from "react";

const LabelledSelect = ({ label, value, onChange, options }) => {
  return <div className="container" >
    <div className="left">
      <span>{label}</span>
    </div>
    <div className="right">
      <Select
        value={value}
        onChange={onChange}
      >
        {
          options.map((option) => {
            return (
              <MenuItem
                key={option}
                value={option}
              >
                {option}
              </MenuItem>
            )
          })
        }
      </Select>
    </div>
  </div>
}

export default LabelledSelect