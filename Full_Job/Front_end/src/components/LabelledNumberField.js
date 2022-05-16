import {TextField} from "@material-ui/core";

const LabelledNumberField = ({ label, value, onChange, minimum=1, step=1 }) => {
  const inputProps = {
    min: minimum,
    step: step,
  };

  return <div className="container">
    <div className="left">
      <span>{label}</span>
    </div>
    <div className="right">
      <TextField
        type='number'
        fullWidth
        value={value}
        onChange={onChange}
        inputProps={inputProps}
      />
    </div>
  </div>
}

export default LabelledNumberField