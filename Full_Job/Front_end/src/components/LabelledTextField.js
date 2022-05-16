import {TextField} from '@material-ui/core'

const LabelledTextField = ({ label, value, onChange, placeholder }) => {
  return <div className="container">
    <div className='left'>
      <span>{label}</span>
    </div>
    <div className='right'>
      <TextField
        type='text'
        fullWidth
        value={value}
        onChange={onChange}
        placeholder={placeholder}
      />
    </div>
  </div>
}

export default LabelledTextField