import { useState } from 'react'
import {
  Accordion as MuiAccordion,
  AccordionDetails,
  AccordionSummary
} from '@material-ui/core'
import ExpandMoreIcon from '@material-ui/icons/ExpandMore'

const Accordion = ({ title, style, children }) => {
    const [isOpen, setIsOpen] = useState(false)
    const toggleIsOpen = () => setIsOpen(!isOpen)
    return (<MuiAccordion
        expanded={isOpen}
        onChange={toggleIsOpen}
        style={style || {width: '100%'}}
    >
        <AccordionSummary
            expandIcon={<ExpandMoreIcon/>}
        >
          {title}
        </AccordionSummary>
        <AccordionDetails>
          {children}
        </AccordionDetails>
    </MuiAccordion>
  )
}

export default Accordion
