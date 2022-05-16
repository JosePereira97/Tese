import Accordion from './Accordion'
import LabelledCheckbox from "./LabelledCheckbox"

const UniprotAccordion = ({ uniprotList, onChange, uniprotPossibilities }) => {

  const handleCheck = value => {
    const newList = [...uniprotList]

    const index = newList.indexOf(value)
    if (index > -1) {
      newList.splice(index, 1)
    } else {
      newList.push(value)
    }

    onChange(newList)
  }

  return (
    <div style={{margin:'0.5rem'}}>
    {
      Object.entries(uniprotPossibilities).map(([section, columns_list], index) => (
        <Accordion key={index} title={section}>
          {
            columns_list.map(( pair , index) => (
              <LabelledCheckbox
                key={index}
                label={pair[0]}
                checked={uniprotList.indexOf(pair[0]) > -1}
                setChecked={() => handleCheck(pair[0])}
              />
              )
            )
          }
        </Accordion>
      ))
    }
  </div>
  )
}

export default UniprotAccordion
