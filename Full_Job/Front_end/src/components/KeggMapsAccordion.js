import Accordion from './Accordion'
import LabelledCheckbox from "./LabelledCheckbox"
import { keggMaps } from '../utils/keggMaps'
import React from "react";

const KeggMapsAccordion = ({ keggMapList, onChange }) => {
  const handleCheck = value => {
    const newList = [...keggMapList]

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
        keggMaps.children.map((category, index) => (
          <Accordion key={index} title={category.name}>
            {
              category.children.map((subCategory, index) => (
                <Accordion key={index} title={subCategory.name}>
                  {
                    subCategory.children.map(({ name }, index) => (
                      <LabelledCheckbox
                        key={index}
                        label={name[1]}
                        checked={keggMapList.indexOf(name[0]) > -1}
                        setChecked={() => handleCheck(name[0])}
                      />)
                    )
                  }
                </Accordion>
              ))
            }
          </Accordion>
        ))
      }
    </div>
  )
}

export default KeggMapsAccordion
