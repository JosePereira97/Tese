import {Checkbox} from '@material-ui/core'
import React from "react";

const LabelledCheckbox = ({ label, checked, setChecked }) => {
  return <div className="container">
    <div className="left">
      <span>{label}</span>
    </div>
    <div className="right">
      <Checkbox
        checked={checked}
        onChange={setChecked}
      />
    </div>
  </div>
}

export default LabelledCheckbox